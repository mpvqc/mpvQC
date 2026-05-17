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
from mpvqc.services.settings import SettingsService
from mpvqc.services.state import StateService

from .concerns import session, subtitles, video
from .plan import FinishedPlan, UnfinishedPlan, make_plan
from .scanner import ResourceScanner

if TYPE_CHECKING:
    from pathlib import Path


logger = logging.getLogger(__name__)


class ImporterService(QObject):
    _player = inject.attr(PlayerService)
    _settings = inject.attr(SettingsService)
    _state = inject.attr(StateService)
    _comments = inject.attr(CommentsService)

    unfinished_plan_ready = Signal(UnfinishedPlan)
    _finished_plan_ready = Signal(FinishedPlan)
    busy_changed = Signal(bool)

    def __init__(self) -> None:
        super().__init__()
        self._scanner = ResourceScanner()
        self._busy = False
        self._finished_plan_ready.connect(self.execute, Qt.ConnectionType.QueuedConnection)

    @Property(bool, notify=busy_changed)
    def busy(self) -> bool:
        return self._busy

    def _set_busy(self, value: bool) -> None:
        if self._busy != value:
            self._busy = value
            self.busy_changed.emit(value)

    def open(self, documents: list[Path], videos: list[Path], subtitles: list[Path]) -> None:
        if self._busy:
            logger.debug(
                "Skipping import while another is in progress; documents=%s videos=%s subtitles=%s",
                documents,
                videos,
                subtitles,
            )
            return
        self._set_busy(True)

        # Capture on the GUI thread
        has_existing_comments = self._comments.count > 0

        def scan_and_dispatch() -> None:
            scan = self._scanner.scan(documents, videos, subtitles)
            match make_plan(
                scan,
                found_video_setting=ImportFoundVideo(self._settings.import_found_video),
                has_existing_comments=has_existing_comments,
                any_candidate_loaded=self._player.is_any_video_loaded(v.path for v in scan.videos),
            ):
                case FinishedPlan() as plan:
                    self._finished_plan_ready.emit(plan)
                case UnfinishedPlan() as unfinished_plan:
                    self.unfinished_plan_ready.emit(unfinished_plan)

        QThreadPool.globalInstance().start(scan_and_dispatch)

    @Slot(FinishedPlan)
    def execute(self, plan: FinishedPlan) -> None:
        match plan.session:
            case session.Replace():
                self._comments.reset()
                self._state.reset()
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

        self._notify_state(plan)
        self._set_busy(False)

    @Slot()
    def cancel_pending(self) -> None:
        self._set_busy(False)

    def _notify_state(self, plan: FinishedPlan) -> None:
        video_path = plan.video.path if isinstance(plan.video, video.Load) else None
        if not plan.comments and video_path is None:
            return
        self._state.apply_import(video=video_path, has_comments=bool(plan.comments))
