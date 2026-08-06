# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import replace
from pathlib import Path
from typing import NamedTuple
from unittest.mock import MagicMock

import inject
import pytest
from PySide6.QtCore import QObject

from mpvqc.datamodels import Comment
from mpvqc.importing.domain import (
    DocumentRejectionReason,
    ErrorsAbsent,
    ErrorsPresent,
    FinishedPlan,
    RejectedDocument,
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
from mpvqc.importing.enums import MpvqcImportWizardNavigationDirection, MpvqcImportWizardSessionMode
from mpvqc.importing.services import ImporterService
from mpvqc.importing.viewmodels import (
    MpvqcImportWizardSessionStepViewModel,
    MpvqcImportWizardSubtitlesStepViewModel,
    MpvqcImportWizardVideoStepViewModel,
    MpvqcImportWizardViewModel,
)

NavigationDirection = MpvqcImportWizardNavigationDirection.NavigationDirection
SessionMode = MpvqcImportWizardSessionMode.SessionMode

VIDEO_A = Path("/movies/a.mp4")
VIDEO_B = Path("/movies/b.mp4")
SUB_A = Path("/work/a.en.srt")
SUB_B = Path("/work/b.en.srt")
COMMENT = Comment(time=0, comment_type="", comment="")

PRESENT_ERRORS = ErrorsPresent(
    rejected_documents=(RejectedDocument(Path("/broken.qc"), DocumentRejectionReason.INVALID),)
)
UNRESOLVED_SESSION = SessionUnresolved(incoming_comment_count=1)
UNRESOLVED_VIDEO = VideoUnresolved(candidates=(VideoSource(path=VIDEO_A, found_in_document=True),))
UNRESOLVED_SUBTITLES = SubtitlesUnresolved(candidates=(SUB_A,))

ALL_RESOLVED = UnfinishedPlan(
    comments=(),
    session=SessionMerge(),
    video=VideoSkip(),
    subtitles=SubtitlesSkip(),
    errors=ErrorsAbsent(),
)


@pytest.fixture
def importer_service_mock() -> MagicMock:
    return MagicMock(spec_set=ImporterService)


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, importer_service_mock):
    def custom(binder: inject.Binder):
        binder.bind(ImporterService, importer_service_mock)

    common_bindings_with(custom)


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


ERRORS_THEN_VIDEO = replace(ALL_RESOLVED, errors=PRESENT_ERRORS, video=UNRESOLVED_VIDEO)
VIDEO_WITH_COMMENTS = replace(ALL_RESOLVED, comments=(COMMENT,), video=UNRESOLVED_VIDEO)
ERRORS_ONLY = replace(ALL_RESOLVED, errors=PRESENT_ERRORS)


def test_primary_click_advances_while_steps_remain(qt_app, importer_service_mock, make_spy) -> None:
    view_model = MpvqcImportWizardViewModel(None, ERRORS_THEN_VIDEO)
    accept_spy = make_spy(view_model.acceptRequested)
    reject_spy = make_spy(view_model.rejectRequested)

    view_model.primaryClicked()

    assert view_model.currentStepIndex == 1
    assert accept_spy.count() == 0
    assert reject_spy.count() == 0
    importer_service_mock.execute.assert_not_called()


def test_primary_click_accepts_on_the_last_step(qt_app, importer_service_mock, make_spy) -> None:
    view_model = MpvqcImportWizardViewModel(None, VIDEO_WITH_COMMENTS)
    accept_spy = make_spy(view_model.acceptRequested)
    reject_spy = make_spy(view_model.rejectRequested)

    view_model.primaryClicked()

    assert accept_spy.count() == 1
    assert reject_spy.count() == 0
    importer_service_mock.execute.assert_called_once()


def test_primary_click_rejects_when_the_wizard_only_closes(qt_app, importer_service_mock, make_spy) -> None:
    view_model = MpvqcImportWizardViewModel(None, ERRORS_ONLY)
    accept_spy = make_spy(view_model.acceptRequested)
    reject_spy = make_spy(view_model.rejectRequested)

    view_model.primaryClicked()

    assert reject_spy.count() == 1
    assert accept_spy.count() == 0
    importer_service_mock.execute.assert_not_called()


def test_cancel_click_rejects(qt_app, importer_service_mock, make_spy) -> None:
    view_model = MpvqcImportWizardViewModel(None, VIDEO_WITH_COMMENTS)
    reject_spy = make_spy(view_model.rejectRequested)

    view_model.cancelClicked()

    assert reject_spy.count() == 1
    importer_service_mock.execute.assert_not_called()


def test_back_returns_to_the_previous_step(qt_app, make_spy) -> None:
    view_model = MpvqcImportWizardViewModel(None, ERRORS_THEN_VIDEO)
    view_model.next()
    spy = make_spy(view_model.currentStepChanged)

    view_model.back()

    assert view_model.currentStepIndex == 0
    assert spy.count() == 1


def test_back_on_the_first_step_stays_put(qt_app, make_spy) -> None:
    view_model = MpvqcImportWizardViewModel(None, ERRORS_THEN_VIDEO)
    spy = make_spy(view_model.currentStepChanged)

    view_model.back()

    assert view_model.currentStepIndex == 0
    assert spy.count() == 0


THREE_STEPS = replace(ALL_RESOLVED, errors=PRESENT_ERRORS, session=UNRESOLVED_SESSION, video=UNRESOLVED_VIDEO)


def test_next_navigates_forward(qt_app, make_spy) -> None:
    view_model = MpvqcImportWizardViewModel(None, ERRORS_THEN_VIDEO)
    spy = make_spy(view_model.navigated)

    view_model.next()

    assert spy.count() == 1
    assert spy.at(0, 0) == NavigationDirection.FORWARD


def test_back_navigates_back(qt_app, make_spy) -> None:
    view_model = MpvqcImportWizardViewModel(None, ERRORS_THEN_VIDEO)
    view_model.next()
    spy = make_spy(view_model.navigated)

    view_model.back()

    assert spy.count() == 1
    assert spy.at(0, 0) == NavigationDirection.BACK


def test_jump_ahead_navigates_forward_once(qt_app, make_spy) -> None:
    view_model = MpvqcImportWizardViewModel(None, THREE_STEPS)
    spy = make_spy(view_model.navigated)

    view_model.setProperty("currentStepIndex", 2)

    assert spy.count() == 1
    assert spy.at(0, 0) == NavigationDirection.FORWARD


def test_jump_back_navigates_back_once(qt_app, make_spy) -> None:
    view_model = MpvqcImportWizardViewModel(None, THREE_STEPS)
    view_model.setProperty("currentStepIndex", 2)
    spy = make_spy(view_model.navigated)

    view_model.setProperty("currentStepIndex", 0)

    assert spy.count() == 1
    assert spy.at(0, 0) == NavigationDirection.BACK


def test_staying_put_emits_no_navigation(qt_app, make_spy) -> None:
    view_model = MpvqcImportWizardViewModel(None, ERRORS_THEN_VIDEO)
    spy = make_spy(view_model.navigated)

    view_model.back()
    view_model.setProperty("currentStepIndex", 0)

    assert spy.count() == 0


def step_view_model[T: QObject](wizard: MpvqcImportWizardViewModel, step_type: type[T]) -> T:
    # Read off the wizard, a step property has the static type Property, and nothing can be called on that. The steps
    # are children of the wizard, so the object tree hands them over with their type intact.
    step = wizard.findChild(step_type)
    assert step is not None
    return step


def test_accepting_hands_the_step_answers_to_the_importer(qt_app, importer_service_mock) -> None:
    plan = replace(
        ALL_RESOLVED,
        comments=(COMMENT,),
        session=UNRESOLVED_SESSION,
        video=VideoUnresolved(
            candidates=(
                VideoSource(path=VIDEO_A, found_in_document=True),
                VideoSource(path=VIDEO_B, found_in_document=False),
            )
        ),
        subtitles=SubtitlesUnresolved(candidates=(SUB_A, SUB_B)),
    )
    view_model = MpvqcImportWizardViewModel(None, plan)

    # Every answer differs from the step's default, so no value below can come from anywhere but the step.
    step_view_model(view_model, MpvqcImportWizardSessionStepViewModel).setProperty("mode", SessionMode.REPLACE.value)
    step_view_model(view_model, MpvqcImportWizardVideoStepViewModel).setProperty("selectedIndex", 1)
    step_view_model(view_model, MpvqcImportWizardSubtitlesStepViewModel).toggle(0)

    view_model.next()
    view_model.next()
    view_model.primaryClicked()

    importer_service_mock.execute.assert_called_once_with(
        FinishedPlan(
            comments=(COMMENT,),
            session=SessionReplace(),
            video=VideoLoad(path=VIDEO_B),
            subtitles=SubtitlesLoad(paths=(SUB_B,)),
        )
    )
