# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from enum import IntEnum, auto
from typing import TYPE_CHECKING

from .plan import ErrorsPresent, SessionUnresolved, SubtitlesLoad, SubtitlesUnresolved, VideoLoad, VideoUnresolved

if TYPE_CHECKING:
    from .plan import UnfinishedPlan


class StepKind(IntEnum):
    ERRORS = auto()
    SESSION = auto()
    VIDEO = auto()
    SUBTITLES = auto()


def compute_steps(unfinished_plan: UnfinishedPlan) -> tuple[StepKind, ...]:
    steps: list[StepKind] = []
    if isinstance(unfinished_plan.errors, ErrorsPresent):
        steps.append(StepKind.ERRORS)
    if isinstance(unfinished_plan.session, SessionUnresolved):
        steps.append(StepKind.SESSION)
    if isinstance(unfinished_plan.video, VideoUnresolved):
        steps.append(StepKind.VIDEO)
    if isinstance(unfinished_plan.subtitles, SubtitlesUnresolved):
        steps.append(StepKind.SUBTITLES)
    return tuple(steps)


def has_valid_content(unfinished_plan: UnfinishedPlan) -> bool:
    return (
        bool(unfinished_plan.comments)
        or isinstance(unfinished_plan.video, VideoLoad)
        or isinstance(unfinished_plan.subtitles, SubtitlesLoad)
    )
