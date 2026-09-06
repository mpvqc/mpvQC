# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Literal

import inject
from PySide6.QtCore import QObject, QStandardPaths, Signal

from mpvqc.build import get_build_info
from mpvqc.comments.services import CommentsService
from mpvqc.jobs import Err, Ok, SerialJobRunner
from mpvqc.player.services import PlayerService
from mpvqc.services import ApplicationPathsService, StateService

from .backup import backup as create_backup
from .errors import ExportError
from .file_names import propose_document_path
from .render_template import render_template, render_template_file
from .render_v1 import render_v1
from .resource import read_shipped_export_template
from .settings import ExportSettingsService
from .snapshot import ExportSnapshot
from .writer import write

if TYPE_CHECKING:
    from collections.abc import Callable

    from mpvqc.jobs import JobExecutor, Result

logger = logging.getLogger(__name__)


class ExportService(QObject):
    _paths = inject.attr(ApplicationPathsService)
    _player = inject.attr(PlayerService)
    _settings = inject.attr(ExportSettingsService)
    _state = inject.attr(StateService)
    _comments = inject.attr(CommentsService)

    export_error_occurred = Signal(str, int)

    def __init__(self, executor: JobExecutor | None = None) -> None:
        super().__init__()
        self._jobs = SerialJobRunner(executor)

    @property
    def is_idle(self) -> bool:
        return self._jobs.is_idle

    def _capture(self) -> ExportSnapshot:
        build = get_build_info()
        return ExportSnapshot(
            captured_at=datetime.now(UTC).astimezone(),
            write_header_date=self._settings.write_header_date,
            write_header_generator=self._settings.write_header_generator,
            write_header_nickname=self._settings.write_header_nickname,
            write_header_video_path=self._settings.write_header_video_path,
            write_header_subtitles=self._settings.write_header_subtitles,
            nickname=self._settings.nickname,
            video_path=self._player.path,
            external_subtitles=tuple(self._player.external_subtitles),
            generator=f"{build.name} {build.version}",
            comments=self._comments.comments(),
        )

    def generate_file_path_proposal(self, suffix: Literal["json", "txt"]) -> Path:
        movies = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.MoviesLocation)
        return propose_document_path(
            video_path=self._player.path,
            nickname=self._settings.nickname,
            suffix=suffix,
            fallback_directory=Path(movies),
        )

    def save(self, document: Path) -> None:
        snapshot = self._capture()
        self._run_export(
            work=lambda: write(document, render_v1(snapshot)),
            failure="Failed to save document",
            on_success=lambda: self._state.record_save(document),
        )

    def export_classic(self, document: Path) -> None:
        snapshot = self._capture()
        template = read_shipped_export_template()
        self._run_export(
            work=lambda: write(document, render_template(template, snapshot)),
            failure="Failed to export document",
        )

    def export_custom(self, document: Path, template: Path) -> None:
        snapshot = self._capture()
        self._run_export(
            work=lambda: write(document, render_template_file(template, snapshot)),
            failure="Failed to export document",
        )

    def _run_export(
        self,
        work: Callable[[], None],
        *,
        failure: str,
        on_success: Callable[[], None] | None = None,
    ) -> None:
        def on_result(result: Result[None]) -> None:
            match result:
                case Ok():
                    if on_success is not None:
                        on_success()
                case Err(ExportError(message, lineno)):
                    # Qt signals carry no optional int, so the absent line becomes -1 at this seam
                    self.export_error_occurred.emit(message, -1 if lineno is None else lineno)
                case Err(error):
                    logger.error(failure, exc_info=error)

        self._jobs.run(work=work, on_result=on_result)

    def backup(self) -> None:
        def on_result(result: Result[None]) -> None:
            match result:
                case Ok():
                    pass
                case Err(error):
                    logger.error("Failed to create backup", exc_info=error)

        backup_dir = self._paths.dir_backup
        snapshot = self._capture()
        self._jobs.run(
            work=lambda: create_backup(backup_dir, snapshot),
            on_result=on_result,
        )
