# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from pathlib import Path

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
from .writer import ExportError, export_custom, save_classic

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

    def _context(self) -> RenderContext:
        return RenderContext(
            settings=self._settings,
            player=self._player,
            build_info=self._build_info,
            comments=self._comments,
        )

    def generate_file_path_proposal(self) -> Path:
        if raw_path := self._player.path:
            path = Path(raw_path)
            video_directory = str(path.parent)
            video_name = path.stem
        else:
            video_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.MoviesLocation)
            video_name = QCoreApplication.translate("FileInteractionDialogs", "untitled")

        nickname = self._settings.nickname
        file_name = f"[QC]_{video_name}_{nickname}.txt" if nickname else f"[QC]_{video_name}.txt"

        return Path(video_directory).joinpath(file_name).absolute()

    def save(self, document: Path) -> None:
        context = self._context()

        def _job() -> None:
            with QMutexLocker(self._mutex):
                try:
                    save_classic(document, self._resources, context)
                    self._state.record_save(document)
                except ExportError as e:
                    self.export_error_occurred.emit(e.message, e.lineno)

        QThreadPool.globalInstance().start(_job)

    def export_classic(self, document: Path) -> None:
        context = self._context()

        def _job() -> None:
            with QMutexLocker(self._mutex):
                try:
                    save_classic(document, self._resources, context)
                except ExportError as e:
                    self.export_error_occurred.emit(e.message, e.lineno)

        QThreadPool.globalInstance().start(_job)

    def export_custom(self, document: Path, template: Path) -> None:
        context = self._context()

        def _job() -> None:
            with QMutexLocker(self._mutex):
                try:
                    export_custom(document, template, context)
                except ExportError as e:
                    self.export_error_occurred.emit(e.message, e.lineno)

        QThreadPool.globalInstance().start(_job)

    def backup(self) -> None:
        context = self._context()

        def _job() -> None:
            try:
                create_backup(self._paths, self._resources, context)
            except Exception:
                logger.exception("Failed to create backup")

        QThreadPool.globalInstance().start(_job)
