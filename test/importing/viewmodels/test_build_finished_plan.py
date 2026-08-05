# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import TYPE_CHECKING, NamedTuple

import pytest
from PySide6.QtCore import QObject

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
)
from mpvqc.importing.viewmodels import (
    build_finished_plan,
    build_session_step,
    build_subtitles_step,
    build_video_step,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from mpvqc.importing.viewmodels import (
        MpvqcImportWizardSessionStepViewModel,
        MpvqcImportWizardSubtitlesStepViewModel,
        MpvqcImportWizardVideoStepViewModel,
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


class _Steps(NamedTuple):
    session: MpvqcImportWizardSessionStepViewModel | None
    video: MpvqcImportWizardVideoStepViewModel | None
    subtitles: MpvqcImportWizardSubtitlesStepViewModel | None

    def choose_replace(self) -> None:
        assert self.session is not None
        self.session.resolved = SessionReplace()

    def select_skip_video(self) -> None:
        assert self.video is not None
        # pyrefly: ignore [missing-attribute]
        skip_index = self.video.candidates.rowCount() - 1
        # pyrefly: ignore [bad-assignment]
        self.video.selectedIndex = skip_index

    def uncheck_all_subtitles(self) -> None:
        assert self.subtitles is not None
        self.subtitles.toggleSelectAll()


class CommitCase(NamedTuple):
    name: str
    plan: UnfinishedPlan
    configure: Callable[[_Steps], None] | None
    expected: FinishedPlan


BUILD_FINISHED_PLAN_CASES = [
    CommitCase(
        name="resolved concerns pass through untouched",
        plan=replace(
            ALL_RESOLVED,
            comments=(COMMENT,),
            session=SessionReplace(),
            video=VideoLoad(path=VIDEO_A),
            subtitles=SubtitlesLoad(paths=(SUB_A,)),
        ),
        configure=None,
        expected=FinishedPlan(
            comments=(COMMENT,),
            session=SessionReplace(),
            video=VideoLoad(path=VIDEO_A),
            subtitles=SubtitlesLoad(paths=(SUB_A,)),
        ),
    ),
    CommitCase(
        name="unresolved session defaults to merge",
        plan=replace(ALL_RESOLVED, session=SessionUnresolved(incoming_comment_count=1)),
        configure=None,
        expected=FinishedPlan(comments=(), session=SessionMerge(), video=VideoSkip(), subtitles=SubtitlesSkip()),
    ),
    CommitCase(
        name="session step switched to replace",
        plan=replace(ALL_RESOLVED, session=SessionUnresolved(incoming_comment_count=1)),
        configure=_Steps.choose_replace,
        expected=FinishedPlan(comments=(), session=SessionReplace(), video=VideoSkip(), subtitles=SubtitlesSkip()),
    ),
    CommitCase(
        name="unresolved video defaults to first candidate",
        plan=replace(ALL_RESOLVED, video=VideoUnresolved(candidates=(VID_A_DOC,))),
        configure=None,
        expected=FinishedPlan(
            comments=(),
            session=SessionMerge(),
            video=VideoLoad(path=VIDEO_A),
            subtitles=SubtitlesSkip(),
        ),
    ),
    CommitCase(
        name="video step skip entry selected",
        plan=replace(ALL_RESOLVED, video=VideoUnresolved(candidates=(VID_A_DOC,))),
        configure=_Steps.select_skip_video,
        expected=FinishedPlan(comments=(), session=SessionMerge(), video=VideoSkip(), subtitles=SubtitlesSkip()),
    ),
    CommitCase(
        name="unresolved subtitles default to all checked",
        plan=replace(ALL_RESOLVED, subtitles=SubtitlesUnresolved(candidates=(SUB_A,))),
        configure=None,
        expected=FinishedPlan(
            comments=(),
            session=SessionMerge(),
            video=VideoSkip(),
            subtitles=SubtitlesLoad(paths=(SUB_A,)),
        ),
    ),
    CommitCase(
        name="subtitles step all unchecked",
        plan=replace(ALL_RESOLVED, subtitles=SubtitlesUnresolved(candidates=(SUB_A,))),
        configure=_Steps.uncheck_all_subtitles,
        expected=FinishedPlan(comments=(), session=SessionMerge(), video=VideoSkip(), subtitles=SubtitlesSkip()),
    ),
]


@pytest.mark.parametrize("case", BUILD_FINISHED_PLAN_CASES, ids=lambda c: c.name)
def test_build_finished_plan(case: CommitCase, qt_app) -> None:
    parent = QObject()
    steps = _Steps(
        session=build_session_step(parent, case.plan.session),
        video=build_video_step(parent, case.plan.video),
        subtitles=build_subtitles_step(parent, case.plan.subtitles),
    )
    if case.configure is not None:
        case.configure(steps)

    assert build_finished_plan(case.plan, *steps) == case.expected


def test_build_finished_plan_requires_step_viewmodels() -> None:
    plan = replace(ALL_RESOLVED, session=SessionUnresolved(incoming_comment_count=1))
    with pytest.raises(RuntimeError):
        build_finished_plan(plan, None, None, None)
