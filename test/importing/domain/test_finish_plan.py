# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any, NamedTuple

import pytest

from mpvqc.datamodels import Comment
from mpvqc.importing.domain import (
    ErrorsAbsent,
    FinishedPlan,
    SessionMerge,
    SessionReplace,
    SessionUnresolved,
    SubtitlesLoad,
    SubtitlesSkip,
    SubtitlesUnresolved,
    UnfinishedPlan,
    VideoLoad,
    VideoSkip,
    VideoSource,
    VideoUnresolved,
    finish_plan,
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


class FinishPlanCase(NamedTuple):
    name: str
    plan: UnfinishedPlan
    answers: dict[str, Any]
    expected: FinishedPlan


FINISH_PLAN_CASES = [
    FinishPlanCase(
        name="already resolved concerns pass through untouched",
        plan=replace(
            ALL_RESOLVED,
            comments=(COMMENT,),
            session=SessionReplace(),
            video=VideoLoad(path=VIDEO_A),
            subtitles=SubtitlesLoad(paths=(SUB_A,)),
        ),
        answers={},
        expected=FinishedPlan(
            comments=(COMMENT,),
            session=SessionReplace(),
            video=VideoLoad(path=VIDEO_A),
            subtitles=SubtitlesLoad(paths=(SUB_A,)),
        ),
    ),
    FinishPlanCase(
        name="an answer is ignored when the concern is already resolved",
        plan=replace(ALL_RESOLVED, session=SessionReplace()),
        answers={"session": SessionMerge()},
        expected=FinishedPlan(comments=(), session=SessionReplace(), video=VideoSkip(), subtitles=SubtitlesSkip()),
    ),
    FinishPlanCase(
        name="unresolved session takes the given answer",
        plan=replace(ALL_RESOLVED, session=SessionUnresolved(incoming_comment_count=1)),
        answers={"session": SessionReplace()},
        expected=FinishedPlan(comments=(), session=SessionReplace(), video=VideoSkip(), subtitles=SubtitlesSkip()),
    ),
    FinishPlanCase(
        name="unresolved video takes the given answer",
        plan=replace(ALL_RESOLVED, video=VideoUnresolved(candidates=(VID_A_DOC,))),
        answers={"video": VideoLoad(path=VIDEO_A)},
        expected=FinishedPlan(
            comments=(),
            session=SessionMerge(),
            video=VideoLoad(path=VIDEO_A),
            subtitles=SubtitlesSkip(),
        ),
    ),
    FinishPlanCase(
        name="unresolved subtitles takes the given answer",
        plan=replace(ALL_RESOLVED, subtitles=SubtitlesUnresolved(candidates=(SUB_A,))),
        answers={"subtitles": SubtitlesLoad(paths=(SUB_A,))},
        expected=FinishedPlan(
            comments=(),
            session=SessionMerge(),
            video=VideoSkip(),
            subtitles=SubtitlesLoad(paths=(SUB_A,)),
        ),
    ),
]


@pytest.mark.parametrize("case", FINISH_PLAN_CASES, ids=lambda c: c.name)
def test_finish_plan(case: FinishPlanCase) -> None:
    assert finish_plan(case.plan, **case.answers) == case.expected


class UnresolvedCase(NamedTuple):
    name: str
    plan: UnfinishedPlan


UNRESOLVED_WITHOUT_ANSWER_CASES = [
    UnresolvedCase("session", replace(ALL_RESOLVED, session=SessionUnresolved(incoming_comment_count=1))),
    UnresolvedCase("video", replace(ALL_RESOLVED, video=VideoUnresolved(candidates=(VID_A_DOC,)))),
    UnresolvedCase("subtitles", replace(ALL_RESOLVED, subtitles=SubtitlesUnresolved(candidates=(SUB_A,)))),
]


@pytest.mark.parametrize("case", UNRESOLVED_WITHOUT_ANSWER_CASES, ids=lambda c: c.name)
def test_finish_plan_raises_when_a_concern_is_unresolved_without_an_answer(case: UnresolvedCase) -> None:
    with pytest.raises(RuntimeError):
        finish_plan(case.plan)
