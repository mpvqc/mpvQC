# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
import re
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING, Literal

import inject
from PySide6.QtCore import QCoreApplication, QObject, QStandardPaths, Signal

from mpvqc.jobs import Err, Ok, SerialJobRunner
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

if TYPE_CHECKING:
    from mpvqc.jobs import JobExecutor, Result

logger = logging.getLogger(__name__)


_INVALID_FILENAME_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


def _sanitize_filename_component(value: str) -> str:
    return _INVALID_FILENAME_CHARS.sub("_", value)


class ExportService(QObject):
    _paths = inject.attr(ApplicationPathsService)
    _player = inject.attr(PlayerService)
    _resources = inject.attr(ResourceService)
    _settings = inject.attr(SettingsService)
    _state = inject.attr(StateService)
    _build_info = inject.attr(BuildInfoService)
    _comments = inject.attr(CommentsService)

    export_error_occurred = Signal(str, int)

    def __init__(self, executor: JobExecutor | None = None) -> None:
        super().__init__()
        self._jobs = SerialJobRunner(executor)

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
            comments=self._comments.comments(),
        )

    def generate_file_path_proposal(self, suffix: Literal["json", "txt"]) -> Path:
        if raw_path := self._player.path:
            path = Path(raw_path)
            video_directory = str(path.parent)
            video_name = path.stem
        else:
            video_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.MoviesLocation)
            video_name = QCoreApplication.translate("FileInteractionDialogs", "untitled")

        nickname = _sanitize_filename_component(self._settings.nickname or "")
        file_name = f"[QC]_{video_name}_{nickname}.{suffix}" if nickname else f"[QC]_{video_name}.{suffix}"

        return Path(video_directory).joinpath(file_name).absolute()

    def save(self, document: Path) -> None:
        def on_result(result: Result[None]) -> None:
            match result:
                case Ok():
                    self._state.record_save(document)
                case Err(ExportError(message, lineno)):
                    self.export_error_occurred.emit(message, lineno)
                case Err(error):
                    logger.error("Failed to save document", exc_info=error)

        self._jobs.run(work=partial(save, document, self._capture()), on_result=on_result)

    def export_classic(self, document: Path) -> None:
        self._jobs.run(
            work=partial(export_classic, document, self._resources, self._capture()),
            on_result=self._on_exported,
        )

    def export_custom(self, document: Path, template: Path) -> None:
        self._jobs.run(
            work=partial(export_custom, document, template, self._capture()),
            on_result=self._on_exported,
        )

    def _on_exported(self, result: Result[None]) -> None:
        match result:
            case Ok():
                pass
            case Err(ExportError(message, lineno)):
                self.export_error_occurred.emit(message, lineno)
            case Err(error):
                logger.error("Failed to export document", exc_info=error)

    def backup(self) -> None:
        def on_result(result: Result[None]) -> None:
            match result:
                case Ok():
                    pass
                case Err(error):
                    logger.error("Failed to create backup", exc_info=error)

        self._jobs.run(
            work=partial(create_backup, self._paths.dir_backup, self._capture()),
            on_result=on_result,
        )
