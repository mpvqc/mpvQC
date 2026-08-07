# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import IntEnum, auto
from typing import TYPE_CHECKING, ClassVar

from mpvqc.importing.domain import (
    ErrorsPresent,
    SessionUnresolved,
    SubtitlesLoad,
    SubtitlesUnresolved,
    VideoLoad,
    VideoUnresolved,
)
from mpvqc.importing.enums import MpvqcImportWizardStepKind

if TYPE_CHECKING:
    from mpvqc.importing.domain import UnfinishedPlan


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


@dataclass(frozen=True, slots=True)
class ErrorsStep:
    kind: ClassVar[MpvqcImportWizardStepKind.StepKind] = MpvqcImportWizardStepKind.StepKind.ERRORS
    errors: ErrorsPresent


@dataclass(frozen=True, slots=True)
class SessionStep:
    kind: ClassVar[MpvqcImportWizardStepKind.StepKind] = MpvqcImportWizardStepKind.StepKind.SESSION
    session: SessionUnresolved


@dataclass(frozen=True, slots=True)
class VideoStep:
    kind: ClassVar[MpvqcImportWizardStepKind.StepKind] = MpvqcImportWizardStepKind.StepKind.VIDEO
    video: VideoUnresolved


@dataclass(frozen=True, slots=True)
class SubtitlesStep:
    kind: ClassVar[MpvqcImportWizardStepKind.StepKind] = MpvqcImportWizardStepKind.StepKind.SUBTITLES
    subtitles: SubtitlesUnresolved


type WizardStep = ErrorsStep | SessionStep | VideoStep | SubtitlesStep


@dataclass(frozen=True, slots=True)
class WizardState:
    plan: UnfinishedPlan
    steps: tuple[WizardStep, ...]
    current_index: int

    @property
    def current_step(self) -> WizardStep:
        return self.steps[self.current_index]

    @property
    def step_kinds(self) -> tuple[MpvqcImportWizardStepKind.StepKind, ...]:
        return tuple(step.kind for step in self.steps)

    @property
    def multi_step(self) -> bool:
        return len(self.steps) > 1

    @property
    def close_only(self) -> bool:
        return _is_close_only(self)

    @property
    def footer(self) -> FooterState:
        return _compute_footer_state(self)

    def advance(self) -> WizardState:
        return self.jump_to(self.current_index + 1)

    def back(self) -> WizardState:
        return self.jump_to(self.current_index - 1)

    def jump_to(self, index: int) -> WizardState:
        if not 0 <= index < len(self.steps):
            return self
        return replace(self, current_index=index)


def make_wizard_state(unfinished_plan: UnfinishedPlan) -> WizardState:
    return WizardState(plan=unfinished_plan, steps=_derive_steps(unfinished_plan), current_index=0)


def _derive_steps(unfinished_plan: UnfinishedPlan) -> tuple[WizardStep, ...]:
    steps: list[WizardStep] = []
    if isinstance(unfinished_plan.errors, ErrorsPresent):
        steps.append(ErrorsStep(unfinished_plan.errors))
    if isinstance(unfinished_plan.session, SessionUnresolved):
        steps.append(SessionStep(unfinished_plan.session))
    if isinstance(unfinished_plan.video, VideoUnresolved):
        steps.append(VideoStep(unfinished_plan.video))
    if isinstance(unfinished_plan.subtitles, SubtitlesUnresolved):
        steps.append(SubtitlesStep(unfinished_plan.subtitles))
    return tuple(steps)


def _is_close_only(state: WizardState) -> bool:
    return state.step_kinds == (MpvqcImportWizardStepKind.StepKind.ERRORS,) and not _has_valid_content(state.plan)


def _compute_footer_state(state: WizardState) -> FooterState:
    has_content = _has_valid_content(state.plan)
    is_last = state.current_index == len(state.steps) - 1

    if _is_close_only(state):
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
        show_cancel=has_content or state.multi_step,
        show_back=state.current_index > 0,
    )


def _has_valid_content(unfinished_plan: UnfinishedPlan) -> bool:
    return (
        bool(unfinished_plan.comments)
        or isinstance(unfinished_plan.video, VideoLoad)
        or isinstance(unfinished_plan.subtitles, SubtitlesLoad)
    )
