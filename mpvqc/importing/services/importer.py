# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Protocol

import inject
from PySide6.QtCore import QObject, Signal

from mpvqc.jobs import Err, Ok, SerialJobRunner
from mpvqc.services import CommentsService, PlayerService, ResetService, StateService

from .concerns import SessionMerge, SessionReplace, SubtitlesLoad, SubtitlesSkip, VideoLoad, VideoSkip
from .pending import PendingImport
from .plan import FinishedPlan, UnfinishedPlan, make_plan
from .scan import scan
from .settings import ImportSettingsService

if TYPE_CHECKING:
    from pathlib import Path

    from mpvqc.jobs import JobExecutor, Result

    from .scan import ScanResult


logger = logging.getLogger(__name__)


class Scanning(Protocol):
    def __call__(
        self, documents: tuple[Path, ...], videos: tuple[Path, ...], subtitles: tuple[Path, ...], /
    ) -> ScanResult: ...


class ImportService(QObject):
    _player = inject.attr(PlayerService)
    _settings = inject.attr(ImportSettingsService)
    _state = inject.attr(StateService)
    _comments = inject.attr(CommentsService)
    _resetter = inject.attr(ResetService)

    pending_import_ready = Signal(PendingImport)

    def __init__(self, executor: JobExecutor | None = None, scan: Scanning = scan) -> None:
        super().__init__()
        self._busy = False
        self._scan = scan
        self._jobs = SerialJobRunner(executor)

    def open(
        self, document_paths: tuple[Path, ...], video_paths: tuple[Path, ...], subtitle_paths: tuple[Path, ...]
    ) -> None:
        if self._busy:
            logger.warning(
                "Skipping import while another is in progress; documents=%s videos=%s subtitles=%s",
                document_paths,
                video_paths,
                subtitle_paths,
            )
            return

        self._busy = True

        # Capture on the GUI thread
        has_existing_comments = self._comments.count > 0
        found_video_setting = self._settings.import_found_video
        current_video = self._player.path

        def build_plan() -> FinishedPlan | UnfinishedPlan:
            scan_result = self._scan(document_paths, video_paths, subtitle_paths)
            return make_plan(
                scan_result,
                found_video_setting=found_video_setting,
                has_existing_comments=has_existing_comments,
                any_candidate_loaded=PlayerService.is_video_path_loaded(
                    current_video, (v.path for v in scan_result.videos)
                ),
            )

        def on_result(result: Result[FinishedPlan | UnfinishedPlan]) -> None:
            match result:
                case Ok(FinishedPlan() as plan):
                    self._execute(plan)
                case Ok(UnfinishedPlan() as plan):
                    self.pending_import_ready.emit(
                        PendingImport(plan, on_finished=self._execute, on_dismissed=self._abandon)
                    )
                case Err(error):
                    self._busy = False
                    logger.error("Import scan failed", exc_info=error)

        self._jobs.run(work=build_plan, on_result=on_result)

    def _abandon(self) -> None:
        self._busy = False

    def _execute(self, plan: FinishedPlan) -> None:
        self._busy = False

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

    def _notify_state(self, plan: FinishedPlan, *, is_new_video: bool) -> None:
        if plan.comments or is_new_video:
            self._state.record_import()
