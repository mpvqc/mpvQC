# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

import pytest

from mpvqc.importing.domain import ErrorsPresent, SubtitlesLoad, UnfinishedPlan, VideoLoad
from mpvqc.importing.enums import MpvqcImportWizardStepKind
from mpvqc.importing.viewmodels import (
    ErrorsStep,
    FooterState,
    PrimaryAction,
    PrimaryLabel,
    SessionStep,
    SubtitlesStep,
    VideoStep,
    WizardState,
    make_wizard_state,
)
from test.importing.plans import (
    ALL_UNRESOLVED,
    COMMENT,
    PRESENT_ERRORS,
    SUB_A,
    UNRESOLVED_SESSION,
    UNRESOLVED_SUBTITLES,
    UNRESOLVED_VIDEO,
    VIDEO_A,
    plan_with,
)

if TYPE_CHECKING:
    from collections.abc import Callable

StepKind = MpvqcImportWizardStepKind.StepKind


def test_steps_carry_the_unresolved_data_in_canonical_order() -> None:
    state = make_wizard_state(ALL_UNRESOLVED)

    assert state.steps == (
        ErrorsStep(PRESENT_ERRORS),
        SessionStep(UNRESOLVED_SESSION),
        VideoStep(UNRESOLVED_VIDEO),
        SubtitlesStep(UNRESOLVED_SUBTITLES),
    )


class StepCase(NamedTuple):
    name: str
    plan: UnfinishedPlan
    expected: tuple[StepKind, ...]


STEP_CASES = [
    StepCase(
        name="errors only",
        plan=plan_with(errors=ErrorsPresent(rejected_documents=())),
        expected=(StepKind.ERRORS,),
    ),
    StepCase(
        name="session only",
        plan=plan_with(session=UNRESOLVED_SESSION),
        expected=(StepKind.SESSION,),
    ),
    StepCase(
        name="video only",
        plan=plan_with(video=UNRESOLVED_VIDEO),
        expected=(StepKind.VIDEO,),
    ),
    StepCase(
        name="subtitles only",
        plan=plan_with(subtitles=UNRESOLVED_SUBTITLES),
        expected=(StepKind.SUBTITLES,),
    ),
    StepCase(
        name="canonical order across all four",
        plan=ALL_UNRESOLVED,
        expected=(StepKind.ERRORS, StepKind.SESSION, StepKind.VIDEO, StepKind.SUBTITLES),
    ),
]


@pytest.mark.parametrize("case", STEP_CASES, ids=lambda c: c.name)
def test_step_kinds(case: StepCase) -> None:
    assert make_wizard_state(case.plan).step_kinds == case.expected


def test_a_new_wizard_starts_on_its_first_step() -> None:
    state = make_wizard_state(ALL_UNRESOLVED)

    assert state.current_index == 0
    assert state.current_step == ErrorsStep(PRESENT_ERRORS)


def test_current_step_follows_the_index() -> None:
    state = make_wizard_state(ALL_UNRESOLVED)

    assert state.advance().current_step == SessionStep(UNRESOLVED_SESSION)
    assert state.jump_to(3).current_step == SubtitlesStep(UNRESOLVED_SUBTITLES)


class TransitionCase(NamedTuple):
    name: str
    start: int
    move: Callable[[WizardState], WizardState]
    expected: int


TRANSITION_CASES = [
    TransitionCase(name="advance", start=0, move=lambda s: s.advance(), expected=1),
    TransitionCase(name="advance off the last step clamps", start=3, move=lambda s: s.advance(), expected=3),
    TransitionCase(name="back", start=2, move=lambda s: s.back(), expected=1),
    TransitionCase(name="back off the first step clamps", start=0, move=lambda s: s.back(), expected=0),
    TransitionCase(name="jump forward", start=0, move=lambda s: s.jump_to(3), expected=3),
    TransitionCase(name="jump backward", start=3, move=lambda s: s.jump_to(1), expected=1),
    TransitionCase(name="jump to the current step", start=2, move=lambda s: s.jump_to(2), expected=2),
    TransitionCase(name="jump below the first step clamps", start=2, move=lambda s: s.jump_to(-1), expected=2),
    TransitionCase(name="jump past the last step clamps", start=2, move=lambda s: s.jump_to(4), expected=2),
]


@pytest.mark.parametrize("case", TRANSITION_CASES, ids=lambda c: c.name)
def test_transitions(case: TransitionCase) -> None:
    start = make_wizard_state(ALL_UNRESOLVED).jump_to(case.start)
    assert start.current_index == case.start

    assert case.move(start).current_index == case.expected


class MultiStepCase(NamedTuple):
    name: str
    plan: UnfinishedPlan
    expected: bool


MULTI_STEP_CASES = [
    MultiStepCase(name="one step", plan=plan_with(errors=PRESENT_ERRORS), expected=False),
    MultiStepCase(name="two steps", plan=plan_with(errors=PRESENT_ERRORS, video=UNRESOLVED_VIDEO), expected=True),
    MultiStepCase(name="four steps", plan=ALL_UNRESOLVED, expected=True),
]


@pytest.mark.parametrize("case", MULTI_STEP_CASES, ids=lambda c: c.name)
def test_multi_step(case: MultiStepCase) -> None:
    assert make_wizard_state(case.plan).multi_step is case.expected


class CloseOnlyCase(NamedTuple):
    name: str
    plan: UnfinishedPlan
    expected: bool


CLOSE_ONLY_CASES = [
    CloseOnlyCase(
        name="errors-only, nothing valid survives -> close-only",
        plan=plan_with(errors=PRESENT_ERRORS),
        expected=True,
    ),
    CloseOnlyCase(
        name="errors-only, comments present -> not close-only",
        plan=plan_with(errors=PRESENT_ERRORS, comments=(COMMENT,)),
        expected=False,
    ),
    CloseOnlyCase(
        name="errors-only, VideoLoad resolved -> not close-only",
        plan=plan_with(errors=PRESENT_ERRORS, video=VideoLoad(path=VIDEO_A)),
        expected=False,
    ),
    CloseOnlyCase(
        name="errors-only, SubtitlesLoad resolved -> not close-only",
        plan=plan_with(errors=PRESENT_ERRORS, subtitles=SubtitlesLoad(paths=(SUB_A,))),
        expected=False,
    ),
    CloseOnlyCase(
        name="errors+video, nothing valid -> not close-only, more than one step",
        plan=plan_with(errors=PRESENT_ERRORS, video=UNRESOLVED_VIDEO),
        expected=False,
    ),
]


@pytest.mark.parametrize("case", CLOSE_ONLY_CASES, ids=lambda c: c.name)
def test_close_only(case: CloseOnlyCase) -> None:
    assert make_wizard_state(case.plan).close_only is case.expected


class FooterCase(NamedTuple):
    name: str
    plan: UnfinishedPlan
    index: int
    expected: FooterState


FOOTER_CASES = [
    FooterCase(
        name="errors-only, no content -> Close + reject, no cancel",
        plan=plan_with(errors=PRESENT_ERRORS),
        index=0,
        expected=FooterState(PrimaryLabel.CLOSE, PrimaryAction.REJECT, show_cancel=False, show_back=False),
    ),
    FooterCase(
        name="errors-only, valid content survives -> Confirm import, cancel shown",
        plan=plan_with(errors=PRESENT_ERRORS, video=VideoLoad(path=VIDEO_A)),
        index=0,
        expected=FooterState(PrimaryLabel.CONFIRM_IMPORT, PrimaryAction.ACCEPT, show_cancel=True, show_back=False),
    ),
    FooterCase(
        name="video-only, no content -> Confirm + accept, no cancel",
        plan=plan_with(video=UNRESOLVED_VIDEO),
        index=0,
        expected=FooterState(PrimaryLabel.CONFIRM, PrimaryAction.ACCEPT, show_cancel=False, show_back=False),
    ),
    FooterCase(
        name="video-only, comments present -> Confirm import, cancel shown",
        plan=plan_with(video=UNRESOLVED_VIDEO, comments=(COMMENT,)),
        index=0,
        expected=FooterState(PrimaryLabel.CONFIRM_IMPORT, PrimaryAction.ACCEPT, show_cancel=True, show_back=False),
    ),
    FooterCase(
        name="errors+video, no content, on errors step -> Next, cancel shown (multi-step exit)",
        plan=plan_with(errors=PRESENT_ERRORS, video=UNRESOLVED_VIDEO),
        index=0,
        expected=FooterState(PrimaryLabel.NEXT, PrimaryAction.ADVANCE, show_cancel=True, show_back=False),
    ),
    FooterCase(
        name="errors+video, no content, on video (terminal) -> Confirm + accept, cancel shown",
        plan=plan_with(errors=PRESENT_ERRORS, video=UNRESOLVED_VIDEO),
        index=1,
        expected=FooterState(PrimaryLabel.CONFIRM, PrimaryAction.ACCEPT, show_cancel=True, show_back=True),
    ),
    FooterCase(
        name="errors+video, with comments, on errors step -> Next, cancel shown",
        plan=plan_with(errors=PRESENT_ERRORS, video=UNRESOLVED_VIDEO, comments=(COMMENT,)),
        index=0,
        expected=FooterState(PrimaryLabel.NEXT, PrimaryAction.ADVANCE, show_cancel=True, show_back=False),
    ),
    FooterCase(
        name="errors+video, with comments, on video step -> Confirm import",
        plan=plan_with(errors=PRESENT_ERRORS, video=UNRESOLVED_VIDEO, comments=(COMMENT,)),
        index=1,
        expected=FooterState(PrimaryLabel.CONFIRM_IMPORT, PrimaryAction.ACCEPT, show_cancel=True, show_back=True),
    ),
    FooterCase(
        name="session+video+subs with comments, on session step -> Next + cancel",
        plan=plan_with(
            session=UNRESOLVED_SESSION,
            video=UNRESOLVED_VIDEO,
            subtitles=UNRESOLVED_SUBTITLES,
            comments=(COMMENT,),
        ),
        index=0,
        expected=FooterState(PrimaryLabel.NEXT, PrimaryAction.ADVANCE, show_cancel=True, show_back=False),
    ),
    FooterCase(
        name="session+video+subs, on subtitles (last) step -> Confirm import",
        plan=plan_with(
            session=UNRESOLVED_SESSION,
            video=UNRESOLVED_VIDEO,
            subtitles=UNRESOLVED_SUBTITLES,
            comments=(COMMENT,),
        ),
        index=2,
        expected=FooterState(PrimaryLabel.CONFIRM_IMPORT, PrimaryAction.ACCEPT, show_cancel=True, show_back=True),
    ),
    FooterCase(
        name="video+subs unresolved, no comments, on subtitles (last) -> Confirm, cancel shown",
        plan=plan_with(video=UNRESOLVED_VIDEO, subtitles=UNRESOLVED_SUBTITLES),
        index=1,
        expected=FooterState(PrimaryLabel.CONFIRM, PrimaryAction.ACCEPT, show_cancel=True, show_back=True),
    ),
]


@pytest.mark.parametrize("case", FOOTER_CASES, ids=lambda c: c.name)
def test_footer(case: FooterCase) -> None:
    state = make_wizard_state(case.plan).jump_to(case.index)
    assert state.current_index == case.index

    assert state.footer == case.expected
