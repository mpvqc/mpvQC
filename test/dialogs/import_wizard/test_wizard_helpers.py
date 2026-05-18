# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import NamedTuple

import pytest

from mpvqc.datamodels import Comment, VideoSource
from mpvqc.dialogs.import_wizard import compute_steps, has_valid_content
from mpvqc.enums import StepKind
from mpvqc.services.importer import UnfinishedPlan, errors, session, subtitles, video

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
        plan=replace(ALL_RESOLVED, errors=errors.Unresolved(invalid_documents=())),
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
            errors=errors.Unresolved(invalid_documents=()),
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
