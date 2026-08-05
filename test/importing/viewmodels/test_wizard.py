# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

import pytest

from mpvqc.datamodels import Comment
from mpvqc.importing.domain import (
    DocumentRejectionReason,
    ErrorsAbsent,
    ErrorsPresent,
    RejectedDocument,
    SessionMerge,
    SubtitlesSkip,
    UnfinishedPlan,
    VideoSkip,
    VideoSource,
    VideoUnresolved,
)
from mpvqc.importing.viewmodels import MpvqcImportWizardViewModel

VIDEO_A = Path("/movies/a.mp4")
COMMENT = Comment(time=0, comment_type="", comment="")

PRESENT_ERRORS = ErrorsPresent(
    rejected_documents=(RejectedDocument(Path("/broken.qc"), DocumentRejectionReason.INVALID),)
)
UNRESOLVED_VIDEO = VideoUnresolved(candidates=(VideoSource(path=VIDEO_A, found_in_document=True),))


class LabelCase(NamedTuple):
    name: str
    plan: UnfinishedPlan
    title: str
    primary_label: str
    show_back: bool
    show_cancel: bool


LABEL_CASES = [
    LabelCase(
        name="errors-only, no content -> close-only",
        plan=UnfinishedPlan(
            comments=(),
            session=SessionMerge(),
            video=VideoSkip(),
            subtitles=SubtitlesSkip(),
            errors=PRESENT_ERRORS,
        ),
        title="Import Error",
        primary_label="Close",
        show_back=False,
        show_cancel=False,
    ),
    LabelCase(
        name="video-only, no content -> Confirm",
        plan=UnfinishedPlan(
            comments=(),
            session=SessionMerge(),
            video=UNRESOLVED_VIDEO,
            subtitles=SubtitlesSkip(),
            errors=ErrorsAbsent(),
        ),
        title="Confirm Import",
        primary_label="Confirm",
        show_back=False,
        show_cancel=False,
    ),
    LabelCase(
        name="video-only, comments present -> Confirm import",
        plan=UnfinishedPlan(
            comments=(COMMENT,),
            session=SessionMerge(),
            video=UNRESOLVED_VIDEO,
            subtitles=SubtitlesSkip(),
            errors=ErrorsAbsent(),
        ),
        title="Confirm Import",
        primary_label="Confirm import",
        show_back=False,
        show_cancel=True,
    ),
    LabelCase(
        name="errors+video, no content, on the first (errors) step -> Next",
        plan=UnfinishedPlan(
            comments=(),
            session=SessionMerge(),
            video=UNRESOLVED_VIDEO,
            subtitles=SubtitlesSkip(),
            errors=PRESENT_ERRORS,
        ),
        title="Confirm Import",
        primary_label="Next",
        show_back=False,
        show_cancel=True,
    ),
]


@pytest.mark.parametrize("case", LABEL_CASES, ids=lambda c: c.name)
def test_title_and_primary_label(qt_app, case: LabelCase) -> None:
    view_model = MpvqcImportWizardViewModel(None, case.plan)

    assert view_model.title == case.title
    assert view_model.primaryLabel == case.primary_label
    assert view_model.showBack is case.show_back
    assert view_model.showCancel is case.show_cancel


def test_primary_label_tracks_the_current_step(qt_app) -> None:
    plan = UnfinishedPlan(
        comments=(),
        session=SessionMerge(),
        video=UNRESOLVED_VIDEO,
        subtitles=SubtitlesSkip(),
        errors=PRESENT_ERRORS,
    )
    view_model = MpvqcImportWizardViewModel(None, plan)
    assert view_model.primaryLabel == "Next"

    view_model.next()

    assert view_model.primaryLabel == "Confirm"
    assert view_model.showBack is True
