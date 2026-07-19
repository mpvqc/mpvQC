# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import inject
from PySide6.QtCore import Property, QObject, Signal, Slot

from mpvqc.enums import ImportFoundVideo
from mpvqc.jobs import Err, Ok, SerialJobRunner
from mpvqc.services.comments import CommentsService
from mpvqc.services.player import PlayerService
from mpvqc.services.resetter import ResetService
from mpvqc.services.settings import SettingsService
from mpvqc.services.state import StateService

from .concerns import session, subtitles, video
from .plan import FinishedPlan, UnfinishedPlan, plan_import

if TYPE_CHECKING:
    from pathlib import Path

    from mpvqc.jobs import JobExecutor, Result


logger = logging.getLogger(__name__)


class ImporterService(QObject):
    _player = inject.attr(PlayerService)
    _settings = inject.attr(SettingsService)
    _state = inject.attr(StateService)
    _comments = inject.attr(CommentsService)
    _resetter = inject.attr(ResetService)

    unfinished_plan_ready = Signal(UnfinishedPlan)
    busy_changed = Signal(bool)

    def __init__(self, executor: JobExecutor | None = None) -> None:
        super().__init__()
        self._busy = False
        self._jobs = SerialJobRunner(executor)

    @Property(bool, notify=busy_changed)
    def busy(self) -> bool:
        return self._busy

    def _set_busy(self, value: bool) -> None:
        if self._busy != value:
            self._busy = value
            self.busy_changed.emit(value)

    def open(self, document_paths: list[Path], video_paths: list[Path], subtitle_paths: list[Path]) -> None:
        if self._busy:
            logger.warning(
                "Skipping import while another is in progress; documents=%s videos=%s subtitles=%s",
                document_paths,
                video_paths,
                subtitle_paths,
            )
            return
        self._set_busy(True)

        # Capture on the GUI thread
        has_existing_comments = self._comments.count > 0
        found_video_setting = ImportFoundVideo(self._settings.import_found_video)
        current_video = self._player.path

        def build_plan() -> FinishedPlan | UnfinishedPlan:
            return plan_import(
                document_paths,
                video_paths,
                subtitle_paths,
                found_video_setting=found_video_setting,
                has_existing_comments=has_existing_comments,
                is_any_candidate_loaded=lambda paths: PlayerService.is_video_path_loaded(current_video, paths),
            )

        def on_result(result: Result[FinishedPlan | UnfinishedPlan]) -> None:
            match result:
                case Ok(FinishedPlan() as plan):
                    self.execute(plan)
                case Ok(UnfinishedPlan() as plan):
                    self.unfinished_plan_ready.emit(plan)
                case Err(error):
                    logger.error("Import scan failed", exc_info=error)
                    self.cancel_pending()

        self._jobs.run(work=build_plan, on_result=on_result)

    @Slot(FinishedPlan)
    def execute(self, plan: FinishedPlan) -> None:
        is_new_video = isinstance(plan.video, video.Load) and not self._player.is_any_video_loaded([plan.video.path])

        match plan.session:
            case session.Replace():
                self._resetter.reset()
            case session.Merge():
                pass

        if plan.comments:
            self._comments.import_comments(plan.comments)

        match (plan.video, plan.subtitles):
            case (video.Load(path=v), subtitles.Load(paths=s)):
                self._player.open_media(video=v, subtitles=s)
            case (video.Load(path=v), subtitles.Skip()):
                self._player.open_media(video=v, subtitles=())
            case (video.Skip(), subtitles.Load(paths=s)):
                self._player.open_media(video=None, subtitles=s)
            case (video.Skip(), subtitles.Skip()):
                pass

        self._notify_state(plan, is_new_video=is_new_video)
        self._set_busy(False)

    @Slot()
    def cancel_pending(self) -> None:
        self._set_busy(False)

    def _notify_state(self, plan: FinishedPlan, *, is_new_video: bool) -> None:
        if plan.comments or is_new_video:
            self._state.record_import()
