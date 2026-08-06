# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple
from unittest.mock import MagicMock

import inject
import pytest
from PySide6.QtCore import QObject

from mpvqc.importing.domain import (
    SessionReplace,
    SubtitlesLoad,
    SubtitlesUnresolved,
    UnfinishedPlan,
    VideoLoad,
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
from test.importing.plans import (
    ALL_UNRESOLVED,
    COMMENT,
    PRESENT_ERRORS,
    SUB_A,
    SUB_B,
    UNRESOLVED_SESSION,
    UNRESOLVED_VIDEO,
    VIDEO_A,
    VIDEO_A_FROM_DOCUMENT,
    VIDEO_B,
    plan_with,
)

NavigationDirection = MpvqcImportWizardNavigationDirection.NavigationDirection
SessionMode = MpvqcImportWizardSessionMode.SessionMode

ERRORS_ONLY = plan_with(errors=PRESENT_ERRORS)
ERRORS_THEN_VIDEO = plan_with(errors=PRESENT_ERRORS, video=UNRESOLVED_VIDEO)
VIDEO_ONLY = plan_with(video=UNRESOLVED_VIDEO)
VIDEO_WITH_COMMENTS = plan_with(comments=(COMMENT,), video=UNRESOLVED_VIDEO)
THREE_STEPS = plan_with(errors=PRESENT_ERRORS, session=UNRESOLVED_SESSION, video=UNRESOLVED_VIDEO)


@pytest.fixture
def importer_service_mock() -> MagicMock:
    return MagicMock(spec_set=ImporterService)


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, importer_service_mock):
    def custom(binder: inject.Binder):
        binder.bind(ImporterService, importer_service_mock)

    common_bindings_with(custom)


class PrimaryLabelCase(NamedTuple):
    name: str
    plan: UnfinishedPlan
    expected: str


PRIMARY_LABEL_CASES = [
    PrimaryLabelCase(
        name="close-only wizard -> Close",
        plan=ERRORS_ONLY,
        expected="Close",
    ),
    PrimaryLabelCase(
        name="last step, no content -> Confirm",
        plan=VIDEO_ONLY,
        expected="Confirm",
    ),
    PrimaryLabelCase(
        name="last step, content -> Confirm import",
        plan=VIDEO_WITH_COMMENTS,
        expected="Confirm import",
    ),
    PrimaryLabelCase(
        name="steps remain -> Next",
        plan=ERRORS_THEN_VIDEO,
        expected="Next",
    ),
]


@pytest.mark.parametrize("case", PRIMARY_LABEL_CASES, ids=lambda c: c.name)
def test_each_primary_label_maps_to_its_text(qt_app, case: PrimaryLabelCase) -> None:
    assert MpvqcImportWizardViewModel(None, case.plan).primaryLabel == case.expected


def test_the_title_follows_close_only(qt_app) -> None:
    assert MpvqcImportWizardViewModel(None, ERRORS_ONLY).title == "Import Error"
    assert MpvqcImportWizardViewModel(None, VIDEO_ONLY).title == "Confirm Import"


def test_the_footer_follows_the_current_step(qt_app) -> None:
    view_model = MpvqcImportWizardViewModel(None, ERRORS_THEN_VIDEO)
    assert view_model.primaryLabel == "Next"
    assert view_model.showBack is False
    assert view_model.showCancel is True

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
        name="every step routes to its own view model",
        plan=ALL_UNRESOLVED,
        expected=BuiltSteps(errors=True, session=True, video=True, subtitles=True),
    ),
    StepViewModelCase(
        name="a step the wizard does not show stays unbuilt",
        plan=ERRORS_ONLY,
        expected=BuiltSteps(errors=True, session=False, video=False, subtitles=False),
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


def test_primary_click_advances_while_steps_remain(qt_app, importer_service_mock, make_spy) -> None:
    view_model = MpvqcImportWizardViewModel(None, ERRORS_THEN_VIDEO)
    accept_spy = make_spy(view_model.acceptRequested)
    reject_spy = make_spy(view_model.rejectRequested)

    view_model.primaryClicked()

    assert view_model.currentStepIndex == 1
    assert accept_spy.count() == 0
    assert reject_spy.count() == 0
    importer_service_mock.finish_pending.assert_not_called()


def test_primary_click_accepts_on_the_last_step(qt_app, importer_service_mock, make_spy) -> None:
    view_model = MpvqcImportWizardViewModel(None, VIDEO_WITH_COMMENTS)
    accept_spy = make_spy(view_model.acceptRequested)
    reject_spy = make_spy(view_model.rejectRequested)

    view_model.primaryClicked()

    assert accept_spy.count() == 1
    assert reject_spy.count() == 0
    # Session and subtitles never got a step, so the wizard has no answer to report for them.
    importer_service_mock.finish_pending.assert_called_once_with(
        session=None,
        video=VideoLoad(path=VIDEO_A),
        subtitles=None,
    )


def test_accepting_reports_before_it_asks_the_dialog_to_close(qt_app, importer_service_mock) -> None:
    # The close runs the app shell's dismissal, and on Windows it runs inside this emit: a report that came
    # afterwards would meet an importer with nothing pending, and the confirmed import would be dropped.
    view_model = MpvqcImportWizardViewModel(None, VIDEO_WITH_COMMENTS)
    reported_by_close: list[bool] = []
    view_model.acceptRequested.connect(lambda: reported_by_close.append(importer_service_mock.finish_pending.called))

    view_model.primaryClicked()

    assert reported_by_close == [True]


def test_primary_click_rejects_when_the_wizard_only_closes(qt_app, importer_service_mock, make_spy) -> None:
    view_model = MpvqcImportWizardViewModel(None, ERRORS_ONLY)
    accept_spy = make_spy(view_model.acceptRequested)
    reject_spy = make_spy(view_model.rejectRequested)

    view_model.primaryClicked()

    assert reject_spy.count() == 1
    assert accept_spy.count() == 0
    importer_service_mock.finish_pending.assert_not_called()


def test_cancel_click_rejects(qt_app, importer_service_mock, make_spy) -> None:
    view_model = MpvqcImportWizardViewModel(None, VIDEO_WITH_COMMENTS)
    reject_spy = make_spy(view_model.rejectRequested)

    view_model.cancelClicked()

    assert reject_spy.count() == 1
    importer_service_mock.finish_pending.assert_not_called()


def test_show_step_indicator_follows_the_step_count(qt_app) -> None:
    assert MpvqcImportWizardViewModel(None, ERRORS_THEN_VIDEO).showStepIndicator is True
    assert MpvqcImportWizardViewModel(None, ERRORS_ONLY).showStepIndicator is False


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


def test_accepting_reports_the_step_answers_to_the_importer(qt_app, importer_service_mock) -> None:
    plan = plan_with(
        comments=(COMMENT,),
        session=UNRESOLVED_SESSION,
        video=VideoUnresolved(
            candidates=(
                VIDEO_A_FROM_DOCUMENT,
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

    importer_service_mock.finish_pending.assert_called_once_with(
        session=SessionReplace(),
        video=VideoLoad(path=VIDEO_B),
        subtitles=SubtitlesLoad(paths=(SUB_B,)),
    )
