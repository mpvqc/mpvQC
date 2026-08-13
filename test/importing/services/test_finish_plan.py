# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import NamedTuple

import pytest

from mpvqc.importing.services import (
    FinishedPlan,
    NotAsked,
    SessionMerge,
    SessionReplace,
    SessionResolved,
    SubtitlesLoad,
    SubtitlesResolved,
    SubtitlesSkip,
    UnfinishedPlan,
    VideoLoad,
    VideoResolved,
    VideoSkip,
    finish_plan,
)
from test.importing.plans import (
    COMMENT,
    SUB_A,
    UNRESOLVED_SESSION,
    UNRESOLVED_SUBTITLES,
    UNRESOLVED_VIDEO,
    VIDEO_A,
    plan_with,
)

ASKS_ABOUT_SESSION = plan_with(session=UNRESOLVED_SESSION)
ASKS_ABOUT_VIDEO = plan_with(video=UNRESOLVED_VIDEO)
ASKS_ABOUT_SUBTITLES = plan_with(subtitles=UNRESOLVED_SUBTITLES)


class FinishPlanCase(NamedTuple):
    name: str
    plan: UnfinishedPlan
    expected: FinishedPlan
    session: SessionResolved | NotAsked = NotAsked()
    video: VideoResolved | NotAsked = NotAsked()
    subtitles: SubtitlesResolved | NotAsked = NotAsked()


FINISH_PLAN_CASES = [
    FinishPlanCase(
        name="already resolved concerns pass through untouched",
        plan=plan_with(
            comments=(COMMENT,),
            session=UNRESOLVED_SESSION,
            video=VideoLoad(path=VIDEO_A),
            subtitles=SubtitlesLoad(paths=(SUB_A,)),
        ),
        session=SessionReplace(),
        expected=FinishedPlan(
            comments=(COMMENT,),
            session=SessionReplace(),
            video=VideoLoad(path=VIDEO_A),
            subtitles=SubtitlesLoad(paths=(SUB_A,)),
        ),
    ),
    FinishPlanCase(
        name="an answer is ignored when the concern is already resolved",
        plan=plan_with(session=SessionReplace(), video=UNRESOLVED_VIDEO),
        session=SessionMerge(),
        video=VideoSkip(),
        expected=FinishedPlan(comments=(), session=SessionReplace(), video=VideoSkip(), subtitles=SubtitlesSkip()),
    ),
    FinishPlanCase(
        name="unresolved session takes the given answer",
        plan=ASKS_ABOUT_SESSION,
        session=SessionReplace(),
        expected=FinishedPlan(comments=(), session=SessionReplace(), video=VideoSkip(), subtitles=SubtitlesSkip()),
    ),
    FinishPlanCase(
        name="unresolved video takes the given answer",
        plan=ASKS_ABOUT_VIDEO,
        video=VideoLoad(path=VIDEO_A),
        expected=FinishedPlan(
            comments=(),
            session=SessionMerge(),
            video=VideoLoad(path=VIDEO_A),
            subtitles=SubtitlesSkip(),
        ),
    ),
    FinishPlanCase(
        name="unresolved subtitles takes the given answer",
        plan=ASKS_ABOUT_SUBTITLES,
        subtitles=SubtitlesLoad(paths=(SUB_A,)),
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
    finished = finish_plan(case.plan, session=case.session, video=case.video, subtitles=case.subtitles)

    assert finished == case.expected


class UnresolvedCase(NamedTuple):
    name: str
    plan: UnfinishedPlan


UNRESOLVED_WITHOUT_ANSWER_CASES = [
    UnresolvedCase("session", ASKS_ABOUT_SESSION),
    UnresolvedCase("video", ASKS_ABOUT_VIDEO),
    UnresolvedCase("subtitles", ASKS_ABOUT_SUBTITLES),
]


@pytest.mark.parametrize("case", UNRESOLVED_WITHOUT_ANSWER_CASES, ids=lambda c: c.name)
def test_finish_plan_raises_when_a_concern_is_unresolved_without_an_answer(case: UnresolvedCase) -> None:
    with pytest.raises(RuntimeError):
        finish_plan(case.plan, session=NotAsked(), video=NotAsked(), subtitles=NotAsked())
