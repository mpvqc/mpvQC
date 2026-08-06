# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Protocol

import inject
from PySide6.QtCore import Property, QObject, Signal, Slot

from mpvqc.importing.domain import (
    FinishedPlan,
    SessionMerge,
    SessionReplace,
    SubtitlesLoad,
    SubtitlesSkip,
    UnfinishedPlan,
    VideoLoad,
    VideoSkip,
)
from mpvqc.jobs import Err, Ok, SerialJobRunner
from mpvqc.services.comments import CommentsService
from mpvqc.services.player import PlayerService
from mpvqc.services.resetter import ResetService
from mpvqc.services.state import StateService

from .plan import plan_import
from .settings import ImportSettingsService

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable
    from pathlib import Path

    from mpvqc.importing.domain import LoadFoundVideo
    from mpvqc.jobs import JobExecutor, Result


logger = logging.getLogger(__name__)


class PlanImport(Protocol):
    def __call__(
        self,
        document_paths: list[Path],
        video_paths: list[Path],
        subtitle_paths: list[Path],
        *,
        found_video_setting: LoadFoundVideo,
        has_existing_comments: bool,
        is_any_candidate_loaded: Callable[[Iterable[Path]], bool],
    ) -> FinishedPlan | UnfinishedPlan: ...


class ImporterService(QObject):
    _player = inject.attr(PlayerService)
    _settings = inject.attr(ImportSettingsService)
    _state = inject.attr(StateService)
    _comments = inject.attr(CommentsService)
    _resetter = inject.attr(ResetService)

    unfinished_plan_ready = Signal(UnfinishedPlan)
    busy_changed = Signal(bool)

    def __init__(self, executor: JobExecutor | None = None, plan: PlanImport = plan_import) -> None:
        super().__init__()
        self._busy = False
        self._plan = plan
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
        found_video_setting = self._settings.import_found_video
        current_video = self._player.path

        def build_plan() -> FinishedPlan | UnfinishedPlan:
            return self._plan(
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
        is_new_video = isinstance(plan.video, VideoLoad) and not self._player.is_any_video_loaded([plan.video.path])

        match plan.session:
            case SessionReplace():
                self._resetter.reset()
            case SessionMerge():
                pass

        if plan.comments:
            self._comments.import_comments(plan.comments)

        match (plan.video, plan.subtitles):
            case (VideoLoad(path=v), SubtitlesLoad(paths=s)):
                self._player.open_media(video=v, subtitles=s)
            case (VideoLoad(path=v), SubtitlesSkip()):
                self._player.open_media(video=v, subtitles=())
            case (VideoSkip(), SubtitlesLoad(paths=s)):
                self._player.open_media(video=None, subtitles=s)
            case (VideoSkip(), SubtitlesSkip()):
                pass

        self._notify_state(plan, is_new_video=is_new_video)
        self._set_busy(False)

    @Slot()
    def cancel_pending(self) -> None:
        self._set_busy(False)

    def _notify_state(self, plan: FinishedPlan, *, is_new_video: bool) -> None:
        if plan.comments or is_new_video:
            self._state.record_import()
