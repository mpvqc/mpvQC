# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

from .plan import finish_plan

if TYPE_CHECKING:
    from collections.abc import Callable

    from .plan import FinishedPlan, UnfinishedPlan
    from .session import SessionResolved
    from .subtitles import SubtitlesResolved
    from .video import VideoResolved


class PendingImport:
    def __init__(
        self,
        plan: UnfinishedPlan,
        *,
        on_finished: Callable[[FinishedPlan], None],
        on_dismissed: Callable[[], None],
    ) -> None:
        self.plan = plan
        self._on_finished = on_finished
        self._on_dismissed = on_dismissed
        self._spent = False

    def finish(
        self,
        *,
        session: SessionResolved | None = None,
        video: VideoResolved | None = None,
        subtitles: SubtitlesResolved | None = None,
    ) -> None:
        if self._spent:
            return
        # Resolve before spending: a finish the plan rejects leaves the import
        # dismissible instead of spent with no outcome delivered.
        finished = finish_plan(self.plan, session=session, video=video, subtitles=subtitles)
        self._spent = True
        self._on_finished(finished)

    def dismiss(self) -> None:
        if self._spent:
            return
        self._spent = True
        self._on_dismissed()
