# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import NamedTuple

import pytest

from mpvqc.datamodels import Comment, VideoSource
from mpvqc.dialogs.import_wizard import FooterState, PrimaryAction, WizardFooterPolicy
from mpvqc.enums import StepKind
from mpvqc.services.importer import UnfinishedPlan
from mpvqc.services.importer.concerns import errors, session, subtitles, video

VIDEO_A = Path("/movies/a.mp4")
SUB_A = Path("/work/a.en.srt")
VID_A_DOC = VideoSource(path=VIDEO_A, found_in_document=True)
COMMENT = Comment(time=0, comment_type="", comment="")

EMPTY = UnfinishedPlan(
    comments=(),
    session=session.Merge(),
    video=video.Skip(),
    subtitles=subtitles.Skip(),
    errors=errors.Absent(),
)

UNRESOLVED_ERRORS = errors.Unresolved(invalid_documents=(Path("/broken.qc"),))
UNRESOLVED_VIDEO = video.Unresolved(candidates=(VID_A_DOC,))
UNRESOLVED_SUBS = subtitles.Unresolved(candidates=(SUB_A,))
UNRESOLVED_SESSION = session.Unresolved(incoming_comment_count=1)


class FooterCase(NamedTuple):
    name: str
    plan: UnfinishedPlan
    steps: tuple[StepKind, ...]
    index: int
    expected: FooterState


CASES = [
    FooterCase(
        name="errors-only, no content -> Close + reject, no cancel",
        plan=replace(EMPTY, errors=UNRESOLVED_ERRORS),
        steps=(StepKind.ERRORS,),
        index=0,
        expected=FooterState("Close", PrimaryAction.REJECT, show_cancel=False, show_back=False),
    ),
    FooterCase(
        name="errors-only, valid content survives -> Confirm import, cancel shown",
        plan=replace(EMPTY, errors=UNRESOLVED_ERRORS, video=video.Load(path=VIDEO_A)),
        steps=(StepKind.ERRORS,),
        index=0,
        expected=FooterState("Confirm import", PrimaryAction.ACCEPT, show_cancel=True, show_back=False),
    ),
    FooterCase(
        name="video-only, no content -> Confirm + accept, no cancel",
        plan=replace(EMPTY, video=UNRESOLVED_VIDEO),
        steps=(StepKind.VIDEO,),
        index=0,
        expected=FooterState("Confirm", PrimaryAction.ACCEPT, show_cancel=False, show_back=False),
    ),
    FooterCase(
        name="video-only, comments present -> Confirm import, cancel shown",
        plan=replace(EMPTY, video=UNRESOLVED_VIDEO, comments=(COMMENT,)),
        steps=(StepKind.VIDEO,),
        index=0,
        expected=FooterState("Confirm import", PrimaryAction.ACCEPT, show_cancel=True, show_back=False),
    ),
    FooterCase(
        name="errors+video, no content, on errors step -> Next, cancel shown (multi-step exit)",
        plan=replace(EMPTY, errors=UNRESOLVED_ERRORS, video=UNRESOLVED_VIDEO),
        steps=(StepKind.ERRORS, StepKind.VIDEO),
        index=0,
        expected=FooterState("Next", PrimaryAction.ADVANCE, show_cancel=True, show_back=False),
    ),
    FooterCase(
        name="errors+video, no content, on video (terminal) -> Confirm + accept, cancel shown",
        plan=replace(EMPTY, errors=UNRESOLVED_ERRORS, video=UNRESOLVED_VIDEO),
        steps=(StepKind.ERRORS, StepKind.VIDEO),
        index=1,
        expected=FooterState("Confirm", PrimaryAction.ACCEPT, show_cancel=True, show_back=True),
    ),
    FooterCase(
        name="errors+video, with comments, on errors step -> Next, cancel shown",
        plan=replace(EMPTY, errors=UNRESOLVED_ERRORS, video=UNRESOLVED_VIDEO, comments=(COMMENT,)),
        steps=(StepKind.ERRORS, StepKind.VIDEO),
        index=0,
        expected=FooterState("Next", PrimaryAction.ADVANCE, show_cancel=True, show_back=False),
    ),
    FooterCase(
        name="errors+video, with comments, on video step -> Confirm import",
        plan=replace(EMPTY, errors=UNRESOLVED_ERRORS, video=UNRESOLVED_VIDEO, comments=(COMMENT,)),
        steps=(StepKind.ERRORS, StepKind.VIDEO),
        index=1,
        expected=FooterState("Confirm import", PrimaryAction.ACCEPT, show_cancel=True, show_back=True),
    ),
    FooterCase(
        name="session+video+subs with comments, on session step -> Next + cancel",
        plan=replace(
            EMPTY,
            session=UNRESOLVED_SESSION,
            video=UNRESOLVED_VIDEO,
            subtitles=UNRESOLVED_SUBS,
            comments=(COMMENT,),
        ),
        steps=(StepKind.SESSION, StepKind.VIDEO, StepKind.SUBTITLES),
        index=0,
        expected=FooterState("Next", PrimaryAction.ADVANCE, show_cancel=True, show_back=False),
    ),
    FooterCase(
        name="session+video+subs, on subtitles (last) step -> Confirm import",
        plan=replace(
            EMPTY,
            session=UNRESOLVED_SESSION,
            video=UNRESOLVED_VIDEO,
            subtitles=UNRESOLVED_SUBS,
            comments=(COMMENT,),
        ),
        steps=(StepKind.SESSION, StepKind.VIDEO, StepKind.SUBTITLES),
        index=2,
        expected=FooterState("Confirm import", PrimaryAction.ACCEPT, show_cancel=True, show_back=True),
    ),
    FooterCase(
        name="video+subs unresolved, no comments, on subtitles (last) -> Confirm, cancel shown",
        plan=replace(EMPTY, video=UNRESOLVED_VIDEO, subtitles=UNRESOLVED_SUBS),
        steps=(StepKind.VIDEO, StepKind.SUBTITLES),
        index=1,
        expected=FooterState("Confirm", PrimaryAction.ACCEPT, show_cancel=True, show_back=True),
    ),
]


@pytest.mark.parametrize("case", CASES, ids=lambda c: c.name)
def test_footer_state(case: FooterCase) -> None:
    policy = WizardFooterPolicy(case.plan, case.steps)
    assert policy.state_for(case.index) == case.expected
