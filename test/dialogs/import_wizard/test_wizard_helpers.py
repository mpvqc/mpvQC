# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import TYPE_CHECKING, NamedTuple

import pytest
from PySide6.QtCore import QObject

from mpvqc.datamodels import Comment, VideoSource
from mpvqc.dialogs.import_wizard import build_finished_plan, compute_steps, has_valid_content
from mpvqc.dialogs.import_wizard.steps import build_session_step, build_subtitles_step, build_video_step
from mpvqc.enums import SessionMode, StepKind
from mpvqc.services.importer import FinishedPlan, UnfinishedPlan, errors, session, subtitles, video

if TYPE_CHECKING:
    from collections.abc import Callable

    from mpvqc.dialogs.import_wizard.steps import (
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
    session=session.Merge(),
    video=video.Skip(),
    subtitles=subtitles.Skip(),
    errors=errors.Absent(),
)


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
        plan=replace(ALL_RESOLVED, errors=errors.Present(rejected_documents=())),
        expected=(StepKind.ERRORS,),
    ),
    StepCase(
        name="session only",
        plan=replace(ALL_RESOLVED, session=session.Unresolved(incoming_comment_count=1)),
        expected=(StepKind.SESSION,),
    ),
    StepCase(
        name="video only",
        plan=replace(ALL_RESOLVED, video=video.Unresolved(candidates=(VID_A_DOC,))),
        expected=(StepKind.VIDEO,),
    ),
    StepCase(
        name="subtitles only",
        plan=replace(ALL_RESOLVED, subtitles=subtitles.Unresolved(candidates=(SUB_A,))),
        expected=(StepKind.SUBTITLES,),
    ),
    StepCase(
        name="canonical order across all four",
        plan=UnfinishedPlan(
            comments=(),
            session=session.Unresolved(incoming_comment_count=1),
            video=video.Unresolved(candidates=(VID_A_DOC,)),
            subtitles=subtitles.Unresolved(candidates=(SUB_A,)),
            errors=errors.Present(rejected_documents=()),
        ),
        expected=(StepKind.ERRORS, StepKind.SESSION, StepKind.VIDEO, StepKind.SUBTITLES),
    ),
]


@pytest.mark.parametrize("case", COMPUTE_STEPS_CASES, ids=lambda c: c.name)
def test_compute_steps(case: StepCase) -> None:
    assert compute_steps(case.plan) == case.expected


class ContentCase(NamedTuple):
    name: str
    plan: UnfinishedPlan
    expected: bool


HAS_VALID_CONTENT_CASES = [
    ContentCase(
        name="nothing valid",
        plan=ALL_RESOLVED,
        expected=False,
    ),
    ContentCase(
        name="comments present",
        plan=replace(ALL_RESOLVED, comments=(COMMENT,)),
        expected=True,
    ),
    ContentCase(
        name="video.Load resolved",
        plan=replace(ALL_RESOLVED, video=video.Load(path=VIDEO_A)),
        expected=True,
    ),
    ContentCase(
        name="subtitles.Load with paths",
        plan=replace(ALL_RESOLVED, subtitles=subtitles.Load(paths=(SUB_A,))),
        expected=True,
    ),
    ContentCase(
        name="video.Unresolved does not count",
        plan=replace(ALL_RESOLVED, video=video.Unresolved(candidates=(VID_A_DOC,))),
        expected=False,
    ),
    ContentCase(
        name="subtitles.Unresolved does not count",
        plan=replace(ALL_RESOLVED, subtitles=subtitles.Unresolved(candidates=(SUB_A,))),
        expected=False,
    ),
    ContentCase(
        name="subtitles.Skip does not count",
        plan=ALL_RESOLVED,
        expected=False,
    ),
]


@pytest.mark.parametrize("case", HAS_VALID_CONTENT_CASES, ids=lambda c: c.name)
def test_has_valid_content(case: ContentCase) -> None:
    assert has_valid_content(case.plan) is case.expected


class _Steps(NamedTuple):
    session: MpvqcImportWizardSessionStepViewModel | None
    video: MpvqcImportWizardVideoStepViewModel | None
    subtitles: MpvqcImportWizardSubtitlesStepViewModel | None

    def choose_replace(self) -> None:
        assert self.session is not None
        # pyrefly: ignore [bad-assignment]
        self.session.mode = SessionMode.REPLACE.value

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
            session=session.Replace(),
            video=video.Load(path=VIDEO_A),
            subtitles=subtitles.Load(paths=(SUB_A,)),
        ),
        configure=None,
        expected=FinishedPlan(
            comments=(COMMENT,),
            session=session.Replace(),
            video=video.Load(path=VIDEO_A),
            subtitles=subtitles.Load(paths=(SUB_A,)),
        ),
    ),
    CommitCase(
        name="unresolved session defaults to merge",
        plan=replace(ALL_RESOLVED, session=session.Unresolved(incoming_comment_count=1)),
        configure=None,
        expected=FinishedPlan(comments=(), session=session.Merge(), video=video.Skip(), subtitles=subtitles.Skip()),
    ),
    CommitCase(
        name="session step switched to replace",
        plan=replace(ALL_RESOLVED, session=session.Unresolved(incoming_comment_count=1)),
        configure=_Steps.choose_replace,
        expected=FinishedPlan(comments=(), session=session.Replace(), video=video.Skip(), subtitles=subtitles.Skip()),
    ),
    CommitCase(
        name="unresolved video defaults to first candidate",
        plan=replace(ALL_RESOLVED, video=video.Unresolved(candidates=(VID_A_DOC,))),
        configure=None,
        expected=FinishedPlan(
            comments=(),
            session=session.Merge(),
            video=video.Load(path=VIDEO_A),
            subtitles=subtitles.Skip(),
        ),
    ),
    CommitCase(
        name="video step skip entry selected",
        plan=replace(ALL_RESOLVED, video=video.Unresolved(candidates=(VID_A_DOC,))),
        configure=_Steps.select_skip_video,
        expected=FinishedPlan(comments=(), session=session.Merge(), video=video.Skip(), subtitles=subtitles.Skip()),
    ),
    CommitCase(
        name="unresolved subtitles default to all checked",
        plan=replace(ALL_RESOLVED, subtitles=subtitles.Unresolved(candidates=(SUB_A,))),
        configure=None,
        expected=FinishedPlan(
            comments=(),
            session=session.Merge(),
            video=video.Skip(),
            subtitles=subtitles.Load(paths=(SUB_A,)),
        ),
    ),
    CommitCase(
        name="subtitles step all unchecked",
        plan=replace(ALL_RESOLVED, subtitles=subtitles.Unresolved(candidates=(SUB_A,))),
        configure=_Steps.uncheck_all_subtitles,
        expected=FinishedPlan(comments=(), session=session.Merge(), video=video.Skip(), subtitles=subtitles.Skip()),
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
    plan = replace(ALL_RESOLVED, session=session.Unresolved(incoming_comment_count=1))
    with pytest.raises(RuntimeError):
        build_finished_plan(plan, None, None, None)
