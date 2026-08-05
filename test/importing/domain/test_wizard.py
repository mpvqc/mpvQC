# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import NamedTuple

import pytest

from mpvqc.datamodels import Comment
from mpvqc.importing.domain import (
    DocumentRejectionReason,
    ErrorsAbsent,
    ErrorsPresent,
    FooterState,
    PrimaryAction,
    PrimaryLabel,
    RejectedDocument,
    SessionMerge,
    SessionUnresolved,
    StepKind,
    SubtitlesLoad,
    SubtitlesSkip,
    SubtitlesUnresolved,
    UnfinishedPlan,
    VideoLoad,
    VideoSkip,
    VideoSource,
    VideoUnresolved,
    compute_footer_state,
    compute_steps,
    is_close_only,
)

VIDEO_A = Path("/movies/a.mp4")
SUB_A = Path("/work/a.en.srt")
VID_A_DOC = VideoSource(path=VIDEO_A, found_in_document=True)
COMMENT = Comment(time=0, comment_type="", comment="")

ALL_RESOLVED = UnfinishedPlan(
    comments=(),
    session=SessionMerge(),
    video=VideoSkip(),
    subtitles=SubtitlesSkip(),
    errors=ErrorsAbsent(),
)

PRESENT_ERRORS = ErrorsPresent(
    rejected_documents=(RejectedDocument(Path("/broken.qc"), DocumentRejectionReason.INVALID),)
)
UNRESOLVED_VIDEO = VideoUnresolved(candidates=(VID_A_DOC,))
UNRESOLVED_SUBS = SubtitlesUnresolved(candidates=(SUB_A,))
UNRESOLVED_SESSION = SessionUnresolved(incoming_comment_count=1)


class StepCase(NamedTuple):
    name: str
    plan: UnfinishedPlan
    expected: tuple[StepKind, ...]


COMPUTE_STEPS_CASES = [
    StepCase(
        name="all resolved",
        plan=ALL_RESOLVED,
        expected=(),
    ),
    StepCase(
        name="errors only",
        plan=replace(ALL_RESOLVED, errors=ErrorsPresent(rejected_documents=())),
        expected=(StepKind.ERRORS,),
    ),
    StepCase(
        name="session only",
        plan=replace(ALL_RESOLVED, session=SessionUnresolved(incoming_comment_count=1)),
        expected=(StepKind.SESSION,),
    ),
    StepCase(
        name="video only",
        plan=replace(ALL_RESOLVED, video=UNRESOLVED_VIDEO),
        expected=(StepKind.VIDEO,),
    ),
    StepCase(
        name="subtitles only",
        plan=replace(ALL_RESOLVED, subtitles=UNRESOLVED_SUBS),
        expected=(StepKind.SUBTITLES,),
    ),
    StepCase(
        name="canonical order across all four",
        plan=UnfinishedPlan(
            comments=(),
            session=UNRESOLVED_SESSION,
            video=UNRESOLVED_VIDEO,
            subtitles=UNRESOLVED_SUBS,
            errors=ErrorsPresent(rejected_documents=()),
        ),
        expected=(StepKind.ERRORS, StepKind.SESSION, StepKind.VIDEO, StepKind.SUBTITLES),
    ),
]


@pytest.mark.parametrize("case", COMPUTE_STEPS_CASES, ids=lambda c: c.name)
def test_compute_steps(case: StepCase) -> None:
    assert compute_steps(case.plan) == case.expected


class CloseOnlyCase(NamedTuple):
    name: str
    plan: UnfinishedPlan
    steps: tuple[StepKind, ...]
    expected: bool


CLOSE_ONLY_CASES = [
    CloseOnlyCase(
        name="errors-only, nothing valid survives -> close-only",
        plan=replace(ALL_RESOLVED, errors=PRESENT_ERRORS),
        steps=(StepKind.ERRORS,),
        expected=True,
    ),
    CloseOnlyCase(
        name="errors-only, comments present -> not close-only",
        plan=replace(ALL_RESOLVED, errors=PRESENT_ERRORS, comments=(COMMENT,)),
        steps=(StepKind.ERRORS,),
        expected=False,
    ),
    CloseOnlyCase(
        name="errors-only, VideoLoad resolved -> not close-only",
        plan=replace(ALL_RESOLVED, errors=PRESENT_ERRORS, video=VideoLoad(path=VIDEO_A)),
        steps=(StepKind.ERRORS,),
        expected=False,
    ),
    CloseOnlyCase(
        name="errors-only, SubtitlesLoad resolved -> not close-only",
        plan=replace(ALL_RESOLVED, errors=PRESENT_ERRORS, subtitles=SubtitlesLoad(paths=(SUB_A,))),
        steps=(StepKind.ERRORS,),
        expected=False,
    ),
    CloseOnlyCase(
        name="errors+video, nothing valid -> not close-only, more than one step",
        plan=replace(ALL_RESOLVED, errors=PRESENT_ERRORS, video=UNRESOLVED_VIDEO),
        steps=(StepKind.ERRORS, StepKind.VIDEO),
        expected=False,
    ),
]


@pytest.mark.parametrize("case", CLOSE_ONLY_CASES, ids=lambda c: c.name)
def test_is_close_only(case: CloseOnlyCase) -> None:
    assert is_close_only(case.plan, case.steps) is case.expected


class FooterCase(NamedTuple):
    name: str
    plan: UnfinishedPlan
    steps: tuple[StepKind, ...]
    index: int
    expected: FooterState


FOOTER_STATE_CASES = [
    FooterCase(
        name="errors-only, no content -> Close + reject, no cancel",
        plan=replace(ALL_RESOLVED, errors=PRESENT_ERRORS),
        steps=(StepKind.ERRORS,),
        index=0,
        expected=FooterState(PrimaryLabel.CLOSE, PrimaryAction.REJECT, show_cancel=False, show_back=False),
    ),
    FooterCase(
        name="errors-only, valid content survives -> Confirm import, cancel shown",
        plan=replace(ALL_RESOLVED, errors=PRESENT_ERRORS, video=VideoLoad(path=VIDEO_A)),
        steps=(StepKind.ERRORS,),
        index=0,
        expected=FooterState(PrimaryLabel.CONFIRM_IMPORT, PrimaryAction.ACCEPT, show_cancel=True, show_back=False),
    ),
    FooterCase(
        name="video-only, no content -> Confirm + accept, no cancel",
        plan=replace(ALL_RESOLVED, video=UNRESOLVED_VIDEO),
        steps=(StepKind.VIDEO,),
        index=0,
        expected=FooterState(PrimaryLabel.CONFIRM, PrimaryAction.ACCEPT, show_cancel=False, show_back=False),
    ),
    FooterCase(
        name="video-only, comments present -> Confirm import, cancel shown",
        plan=replace(ALL_RESOLVED, video=UNRESOLVED_VIDEO, comments=(COMMENT,)),
        steps=(StepKind.VIDEO,),
        index=0,
        expected=FooterState(PrimaryLabel.CONFIRM_IMPORT, PrimaryAction.ACCEPT, show_cancel=True, show_back=False),
    ),
    FooterCase(
        name="errors+video, no content, on errors step -> Next, cancel shown (multi-step exit)",
        plan=replace(ALL_RESOLVED, errors=PRESENT_ERRORS, video=UNRESOLVED_VIDEO),
        steps=(StepKind.ERRORS, StepKind.VIDEO),
        index=0,
        expected=FooterState(PrimaryLabel.NEXT, PrimaryAction.ADVANCE, show_cancel=True, show_back=False),
    ),
    FooterCase(
        name="errors+video, no content, on video (terminal) -> Confirm + accept, cancel shown",
        plan=replace(ALL_RESOLVED, errors=PRESENT_ERRORS, video=UNRESOLVED_VIDEO),
        steps=(StepKind.ERRORS, StepKind.VIDEO),
        index=1,
        expected=FooterState(PrimaryLabel.CONFIRM, PrimaryAction.ACCEPT, show_cancel=True, show_back=True),
    ),
    FooterCase(
        name="errors+video, with comments, on errors step -> Next, cancel shown",
        plan=replace(ALL_RESOLVED, errors=PRESENT_ERRORS, video=UNRESOLVED_VIDEO, comments=(COMMENT,)),
        steps=(StepKind.ERRORS, StepKind.VIDEO),
        index=0,
        expected=FooterState(PrimaryLabel.NEXT, PrimaryAction.ADVANCE, show_cancel=True, show_back=False),
    ),
    FooterCase(
        name="errors+video, with comments, on video step -> Confirm import",
        plan=replace(ALL_RESOLVED, errors=PRESENT_ERRORS, video=UNRESOLVED_VIDEO, comments=(COMMENT,)),
        steps=(StepKind.ERRORS, StepKind.VIDEO),
        index=1,
        expected=FooterState(PrimaryLabel.CONFIRM_IMPORT, PrimaryAction.ACCEPT, show_cancel=True, show_back=True),
    ),
    FooterCase(
        name="session+video+subs with comments, on session step -> Next + cancel",
        plan=replace(
            ALL_RESOLVED,
            session=UNRESOLVED_SESSION,
            video=UNRESOLVED_VIDEO,
            subtitles=UNRESOLVED_SUBS,
            comments=(COMMENT,),
        ),
        steps=(StepKind.SESSION, StepKind.VIDEO, StepKind.SUBTITLES),
        index=0,
        expected=FooterState(PrimaryLabel.NEXT, PrimaryAction.ADVANCE, show_cancel=True, show_back=False),
    ),
    FooterCase(
        name="session+video+subs, on subtitles (last) step -> Confirm import",
        plan=replace(
            ALL_RESOLVED,
            session=UNRESOLVED_SESSION,
            video=UNRESOLVED_VIDEO,
            subtitles=UNRESOLVED_SUBS,
            comments=(COMMENT,),
        ),
        steps=(StepKind.SESSION, StepKind.VIDEO, StepKind.SUBTITLES),
        index=2,
        expected=FooterState(PrimaryLabel.CONFIRM_IMPORT, PrimaryAction.ACCEPT, show_cancel=True, show_back=True),
    ),
    FooterCase(
        name="video+subs unresolved, no comments, on subtitles (last) -> Confirm, cancel shown",
        plan=replace(ALL_RESOLVED, video=UNRESOLVED_VIDEO, subtitles=UNRESOLVED_SUBS),
        steps=(StepKind.VIDEO, StepKind.SUBTITLES),
        index=1,
        expected=FooterState(PrimaryLabel.CONFIRM, PrimaryAction.ACCEPT, show_cancel=True, show_back=True),
    ),
]


@pytest.mark.parametrize("case", FOOTER_STATE_CASES, ids=lambda c: c.name)
def test_footer_state(case: FooterCase) -> None:
    assert compute_footer_state(case.plan, case.steps, case.index) == case.expected
