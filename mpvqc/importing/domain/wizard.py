# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
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


class PrimaryLabel(IntEnum):
    CLOSE = auto()
    CONFIRM = auto()
    CONFIRM_IMPORT = auto()
    NEXT = auto()


class PrimaryAction(IntEnum):
    ADVANCE = auto()
    ACCEPT = auto()
    REJECT = auto()


@dataclass(frozen=True, slots=True)
class FooterState:
    primary_label: PrimaryLabel
    primary_action: PrimaryAction
    show_cancel: bool
    show_back: bool


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


def is_close_only(unfinished_plan: UnfinishedPlan, steps: tuple[StepKind, ...]) -> bool:
    return steps == (StepKind.ERRORS,) and not _has_valid_content(unfinished_plan)


def compute_footer_state(
    unfinished_plan: UnfinishedPlan,
    steps: tuple[StepKind, ...],
    current_index: int,
) -> FooterState:
    has_content = _has_valid_content(unfinished_plan)
    is_last = current_index == len(steps) - 1

    if is_close_only(unfinished_plan, steps):
        label = PrimaryLabel.CLOSE
        action = PrimaryAction.REJECT
    elif is_last and not has_content:
        label = PrimaryLabel.CONFIRM
        action = PrimaryAction.ACCEPT
    elif is_last:
        label = PrimaryLabel.CONFIRM_IMPORT
        action = PrimaryAction.ACCEPT
    else:
        label = PrimaryLabel.NEXT
        action = PrimaryAction.ADVANCE

    return FooterState(
        primary_label=label,
        primary_action=action,
        show_cancel=has_content or len(steps) > 1,
        show_back=current_index > 0,
    )


def _has_valid_content(unfinished_plan: UnfinishedPlan) -> bool:
    return (
        bool(unfinished_plan.comments)
        or isinstance(unfinished_plan.video, VideoLoad)
        or isinstance(unfinished_plan.subtitles, SubtitlesLoad)
    )
