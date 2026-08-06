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
    RejectedDocument,
    SessionMerge,
    SessionUnresolved,
    SubtitlesSkip,
    SubtitlesUnresolved,
    UnfinishedPlan,
    VideoLoad,
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
UNRESOLVED_SESSION = SessionUnresolved(incoming_comment_count=1)
UNRESOLVED_VIDEO = VideoUnresolved(candidates=(VideoSource(path=VIDEO_A, found_in_document=True),))
UNRESOLVED_SUBTITLES = SubtitlesUnresolved(candidates=(Path("/work/a.en.srt"),))

ALL_RESOLVED = UnfinishedPlan(
    comments=(),
    session=SessionMerge(),
    video=VideoSkip(),
    subtitles=SubtitlesSkip(),
    errors=ErrorsAbsent(),
)


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
        plan=replace(ALL_RESOLVED, errors=PRESENT_ERRORS),
        title="Import Error",
        primary_label="Close",
        show_back=False,
        show_cancel=False,
    ),
    LabelCase(
        name="video-only, no content -> Confirm",
        plan=replace(ALL_RESOLVED, video=UNRESOLVED_VIDEO),
        title="Confirm Import",
        primary_label="Confirm",
        show_back=False,
        show_cancel=False,
    ),
    LabelCase(
        name="video-only, comments present -> Confirm import",
        plan=replace(ALL_RESOLVED, video=UNRESOLVED_VIDEO, comments=(COMMENT,)),
        title="Confirm Import",
        primary_label="Confirm import",
        show_back=False,
        show_cancel=True,
    ),
    LabelCase(
        name="errors+video, no content, on the first (errors) step -> Next",
        plan=replace(ALL_RESOLVED, errors=PRESENT_ERRORS, video=UNRESOLVED_VIDEO),
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
    plan = replace(ALL_RESOLVED, errors=PRESENT_ERRORS, video=UNRESOLVED_VIDEO)
    view_model = MpvqcImportWizardViewModel(None, plan)
    assert view_model.primaryLabel == "Next"

    view_model.next()

    assert view_model.primaryLabel == "Confirm"
    assert view_model.showBack is True


class BuiltSteps(NamedTuple):
    errors: bool
    session: bool
    video: bool
    subtitles: bool


class StepViewModelCase(NamedTuple):
    name: str
    plan: UnfinishedPlan
    expected: BuiltSteps


STEP_VIEW_MODEL_CASES = [
    StepViewModelCase(
        name="errors only",
        plan=replace(ALL_RESOLVED, errors=PRESENT_ERRORS),
        expected=BuiltSteps(errors=True, session=False, video=False, subtitles=False),
    ),
    StepViewModelCase(
        name="session only",
        plan=replace(ALL_RESOLVED, session=UNRESOLVED_SESSION),
        expected=BuiltSteps(errors=False, session=True, video=False, subtitles=False),
    ),
    StepViewModelCase(
        name="video only",
        plan=replace(ALL_RESOLVED, video=UNRESOLVED_VIDEO),
        expected=BuiltSteps(errors=False, session=False, video=True, subtitles=False),
    ),
    StepViewModelCase(
        name="subtitles only",
        plan=replace(ALL_RESOLVED, subtitles=UNRESOLVED_SUBTITLES),
        expected=BuiltSteps(errors=False, session=False, video=False, subtitles=True),
    ),
    StepViewModelCase(
        name="a resolved concern alongside errors builds no step of its own",
        plan=replace(ALL_RESOLVED, errors=PRESENT_ERRORS, video=VideoLoad(path=VIDEO_A)),
        expected=BuiltSteps(errors=True, session=False, video=False, subtitles=False),
    ),
    StepViewModelCase(
        name="everything unresolved",
        plan=replace(
            ALL_RESOLVED,
            errors=PRESENT_ERRORS,
            session=UNRESOLVED_SESSION,
            video=UNRESOLVED_VIDEO,
            subtitles=UNRESOLVED_SUBTITLES,
        ),
        expected=BuiltSteps(errors=True, session=True, video=True, subtitles=True),
    ),
]


@pytest.mark.parametrize("case", STEP_VIEW_MODEL_CASES, ids=lambda c: c.name)
def test_builds_only_the_step_view_models_the_wizard_shows(qt_app, case: StepViewModelCase) -> None:
    view_model = MpvqcImportWizardViewModel(None, case.plan)

    built = BuiltSteps(
        errors=view_model.errorsStepViewModel is not None,
        session=view_model.sessionStepViewModel is not None,
        video=view_model.videoStepViewModel is not None,
        subtitles=view_model.subtitlesStepViewModel is not None,
    )

    assert built == case.expected


def test_a_plan_with_nothing_to_decide_cannot_open_a_wizard(qt_app) -> None:
    with pytest.raises(ValueError, match="nothing to decide"):
        MpvqcImportWizardViewModel(None, ALL_RESOLVED)
