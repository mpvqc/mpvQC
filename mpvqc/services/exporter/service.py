# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from pathlib import Path
from typing import Literal

import inject
from PySide6.QtCore import QCoreApplication, QMutex, QMutexLocker, QObject, QStandardPaths, QThreadPool, Signal

from mpvqc.services.application_paths import ApplicationPathsService
from mpvqc.services.build_info import BuildInfoService
from mpvqc.services.comments import CommentsService
from mpvqc.services.player import PlayerService
from mpvqc.services.resource import ResourceService
from mpvqc.services.settings import SettingsService
from mpvqc.services.state import StateService

from .backup import backup as create_backup
from .context import RenderContext
from .writer import ExportError, export_classic, export_custom, save

logger = logging.getLogger(__name__)


class ExportService(QObject):
    _paths = inject.attr(ApplicationPathsService)
    _player = inject.attr(PlayerService)
    _resources = inject.attr(ResourceService)
    _settings = inject.attr(SettingsService)
    _state = inject.attr(StateService)
    _build_info = inject.attr(BuildInfoService)
    _comments = inject.attr(CommentsService)

    export_error_occurred = Signal(str, int)

    def __init__(self) -> None:
        super().__init__()
        self._mutex = QMutex()

    def _capture(self) -> RenderContext:
        return RenderContext(
            write_header_date=self._settings.write_header_date,
            write_header_generator=self._settings.write_header_generator,
            write_header_nickname=self._settings.write_header_nickname,
            write_header_video_path=self._settings.write_header_video_path,
            write_header_subtitles=self._settings.write_header_subtitles,
            nickname=self._settings.nickname,
            video_path=self._player.path,
            external_subtitles=tuple(self._player.external_subtitles),
            generator=f"{self._build_info.name} {self._build_info.version}",
            comments=tuple(self._comments.comments()),
        )

    def generate_file_path_proposal(self, suffix: Literal["json", "txt"]) -> Path:
        if raw_path := self._player.path:
            path = Path(raw_path)
            video_directory = str(path.parent)
            video_name = path.stem
        else:
            video_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.MoviesLocation)
            video_name = QCoreApplication.translate("FileInteractionDialogs", "untitled")

        nickname = self._settings.nickname
        file_name = f"[QC]_{video_name}_{nickname}.{suffix}" if nickname else f"[QC]_{video_name}.{suffix}"

        return Path(video_directory).joinpath(file_name).absolute()

    def save(self, document: Path) -> None:
        context = self._capture()

        def _job() -> None:
            with QMutexLocker(self._mutex):
                try:
                    save(document, context)
                    self._state.record_save(document)
                except ExportError as e:
                    self.export_error_occurred.emit(e.message, e.lineno)

        QThreadPool.globalInstance().start(_job)

    def export_classic(self, document: Path) -> None:
        context = self._capture()

        def _job() -> None:
            with QMutexLocker(self._mutex):
                try:
                    export_classic(document, self._resources, context)
                except ExportError as e:
                    self.export_error_occurred.emit(e.message, e.lineno)

        QThreadPool.globalInstance().start(_job)

    def export_custom(self, document: Path, template: Path) -> None:
        context = self._capture()

        def _job() -> None:
            with QMutexLocker(self._mutex):
                try:
                    export_custom(document, template, context)
                except ExportError as e:
                    self.export_error_occurred.emit(e.message, e.lineno)

        QThreadPool.globalInstance().start(_job)

    def backup(self) -> None:
        backup_dir = self._paths.dir_backup
        context = self._capture()

        def _job() -> None:
            try:
                create_backup(backup_dir, context)
            except Exception:
                logger.exception("Failed to create backup")

        QThreadPool.globalInstance().start(_job)
