# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import inject
from PySide6.QtCore import Property, QObject, Qt, QThreadPool, Signal, Slot

from mpvqc.enums import ImportFoundVideo
from mpvqc.services.comments import CommentsService
from mpvqc.services.player import PlayerService
from mpvqc.services.resetter import ResetService
from mpvqc.services.settings import SettingsService
from mpvqc.services.state import StateService

from .concerns import session, subtitles, video
from .plan import FinishedPlan, UnfinishedPlan, make_plan
from .scanner import scan

if TYPE_CHECKING:
    from pathlib import Path


logger = logging.getLogger(__name__)


class ImporterService(QObject):
    _player = inject.attr(PlayerService)
    _settings = inject.attr(SettingsService)
    _state = inject.attr(StateService)
    _comments = inject.attr(CommentsService)
    _resetter = inject.attr(ResetService)

    unfinished_plan_ready = Signal(UnfinishedPlan)
    _finished_plan_ready = Signal(FinishedPlan)
    _scan_failed = Signal()
    busy_changed = Signal(bool)

    def __init__(self) -> None:
        super().__init__()
        self._busy = False
        self._finished_plan_ready.connect(self.execute, Qt.ConnectionType.QueuedConnection)
        self._scan_failed.connect(self.cancel_pending, Qt.ConnectionType.QueuedConnection)

    @Property(bool, notify=busy_changed)
    def busy(self) -> bool:
        return self._busy

    def _set_busy(self, value: bool) -> None:
        if self._busy != value:
            self._busy = value
            self.busy_changed.emit(value)

    def open(self, document_paths: list[Path], video_paths: list[Path], subtitle_paths: list[Path]) -> None:
        if self._busy:
            logger.debug(
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

        def scan_and_dispatch() -> None:
            try:
                scan_result = scan(document_paths, video_paths, subtitle_paths)
                plan = make_plan(
                    scan_result,
                    found_video_setting=found_video_setting,
                    has_existing_comments=has_existing_comments,
                    any_candidate_loaded=PlayerService.is_video_path_loaded(
                        current_video, (v.path for v in scan_result.videos)
                    ),
                )
            except Exception:
                logger.exception("Import scan failed")
                self._scan_failed.emit()
                return

            match plan:
                case FinishedPlan():
                    self._finished_plan_ready.emit(plan)
                case UnfinishedPlan():
                    self.unfinished_plan_ready.emit(plan)

        QThreadPool.globalInstance().start(scan_and_dispatch)

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
