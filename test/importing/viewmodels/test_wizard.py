# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple

import pytest
from PySide6.QtCore import QObject

from mpvqc.importing.domain import (
    FinishedPlan,
    SessionMerge,
    SessionReplace,
    SubtitlesLoad,
    SubtitlesSkip,
    SubtitlesUnresolved,
    UnfinishedPlan,
    VideoLoad,
    VideoSource,
    VideoUnresolved,
)
from mpvqc.importing.enums import (
    MpvqcImportWizardNavigationDirection,
    MpvqcImportWizardSessionMode,
    MpvqcImportWizardStepKind,
)
from mpvqc.importing.viewmodels import (
    MpvqcImportWizardErrorsStepViewModel,
    MpvqcImportWizardSessionStepViewModel,
    MpvqcImportWizardSubtitlesStepViewModel,
    MpvqcImportWizardVideoStepViewModel,
    MpvqcImportWizardViewModel,
)
from test.importing.pending import record_pending
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
StepKind = MpvqcImportWizardStepKind.StepKind

ERRORS_ONLY = plan_with(errors=PRESENT_ERRORS)
ERRORS_THEN_VIDEO = plan_with(errors=PRESENT_ERRORS, video=UNRESOLVED_VIDEO)
VIDEO_ONLY = plan_with(video=UNRESOLVED_VIDEO)
VIDEO_WITH_COMMENTS = plan_with(comments=(COMMENT,), video=UNRESOLVED_VIDEO)
THREE_STEPS = plan_with(errors=PRESENT_ERRORS, session=UNRESOLVED_SESSION, video=UNRESOLVED_VIDEO)


class WizardSetup(NamedTuple):
    view_model: MpvqcImportWizardViewModel
    finished: list[FinishedPlan]
    dismissals: list[bool]


def make_wizard(plan: UnfinishedPlan) -> WizardSetup:
    recorded = record_pending(plan)
    return WizardSetup(MpvqcImportWizardViewModel(None, recorded.pending), recorded.finished, recorded.dismissals)


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
    assert make_wizard(case.plan).view_model.primaryLabel == case.expected


def test_the_title_follows_close_only(qt_app) -> None:
    assert make_wizard(ERRORS_ONLY).view_model.title == "Import Error"
    assert make_wizard(VIDEO_ONLY).view_model.title == "Confirm Import"


def test_the_footer_follows_the_current_step(qt_app) -> None:
    view_model = make_wizard(ERRORS_THEN_VIDEO).view_model
    assert view_model.primaryLabel == "Next"
    assert view_model.showBack is False
    assert view_model.showCancel is True

    view_model.next()

    assert view_model.primaryLabel == "Confirm"
    assert view_model.showBack is True


STEP_VIEW_MODEL_BY_KIND = {
    StepKind.ERRORS: MpvqcImportWizardErrorsStepViewModel,
    StepKind.SESSION: MpvqcImportWizardSessionStepViewModel,
    StepKind.VIDEO: MpvqcImportWizardVideoStepViewModel,
    StepKind.SUBTITLES: MpvqcImportWizardSubtitlesStepViewModel,
}


class StepsCase(NamedTuple):
    name: str
    plan: UnfinishedPlan
    expected_kinds: list[StepKind]


STEPS_CASES = [
    StepsCase(
        name="every step appears as its own view model, in step order",
        plan=ALL_UNRESOLVED,
        expected_kinds=[StepKind.ERRORS, StepKind.SESSION, StepKind.VIDEO, StepKind.SUBTITLES],
    ),
    StepsCase(
        name="a step the wizard does not show is absent from the list",
        plan=ERRORS_ONLY,
        expected_kinds=[StepKind.ERRORS],
    ),
]


@pytest.mark.parametrize("case", STEPS_CASES, ids=lambda c: c.name)
def test_steps_hold_one_view_model_per_wizard_step(qt_app, case: StepsCase) -> None:
    # Held for the whole test: the steps are parented to the wizard, and a collected wizard takes them with it.
    view_model = make_wizard(case.plan).view_model
    steps = view_model.property("steps")

    assert [step.kind for step in steps] == case.expected_kinds
    assert [type(step) for step in steps] == [STEP_VIEW_MODEL_BY_KIND[kind] for kind in case.expected_kinds]


def test_every_step_is_named_in_canonical_order(qt_app) -> None:
    view_model = make_wizard(ALL_UNRESOLVED).view_model

    assert view_model.stepNames == [
        "Errors",
        "Session",
        "Video",
        "Subtitles",
    ]


def test_primary_click_advances_while_steps_remain(qt_app, make_spy) -> None:
    setup = make_wizard(ERRORS_THEN_VIDEO)
    accept_spy = make_spy(setup.view_model.acceptRequested)
    reject_spy = make_spy(setup.view_model.rejectRequested)

    setup.view_model.primaryClicked()

    assert setup.view_model.currentStepIndex == 1
    assert accept_spy.count() == 0
    assert reject_spy.count() == 0
    assert setup.finished == []


def test_primary_click_accepts_on_the_last_step(qt_app, make_spy) -> None:
    setup = make_wizard(VIDEO_WITH_COMMENTS)
    accept_spy = make_spy(setup.view_model.acceptRequested)
    reject_spy = make_spy(setup.view_model.rejectRequested)

    setup.view_model.primaryClicked()

    assert accept_spy.count() == 1
    assert reject_spy.count() == 0
    # The dialog's accepted handler reports the outcome, so the click itself delivers nothing.
    assert setup.finished == []
    assert setup.dismissals == []


def test_finish_delivers_the_resolved_plan(qt_app) -> None:
    setup = make_wizard(VIDEO_WITH_COMMENTS)

    setup.view_model.finish()

    assert setup.finished == [
        FinishedPlan(
            comments=(COMMENT,),
            session=SessionMerge(),
            video=VideoLoad(path=VIDEO_A),
            subtitles=SubtitlesSkip(),
        )
    ]
    assert setup.dismissals == []


def test_dismiss_delivers_the_dismissal(qt_app) -> None:
    setup = make_wizard(VIDEO_WITH_COMMENTS)

    setup.view_model.dismiss()

    assert setup.finished == []
    assert setup.dismissals == [True]


def test_primary_click_rejects_when_the_wizard_only_closes(qt_app, make_spy) -> None:
    setup = make_wizard(ERRORS_ONLY)
    accept_spy = make_spy(setup.view_model.acceptRequested)
    reject_spy = make_spy(setup.view_model.rejectRequested)

    setup.view_model.primaryClicked()

    assert reject_spy.count() == 1
    assert accept_spy.count() == 0
    assert setup.finished == []


def test_cancel_click_rejects(qt_app, make_spy) -> None:
    setup = make_wizard(VIDEO_WITH_COMMENTS)
    reject_spy = make_spy(setup.view_model.rejectRequested)

    setup.view_model.cancelClicked()

    assert reject_spy.count() == 1
    # The dialog's rejected handler reports the dismissal, so the click itself delivers nothing.
    assert setup.finished == []
    assert setup.dismissals == []


def test_multi_step_follows_the_step_count(qt_app) -> None:
    assert make_wizard(ERRORS_THEN_VIDEO).view_model.multiStep is True
    assert make_wizard(ERRORS_ONLY).view_model.multiStep is False


def test_current_step_name_follows_navigation(qt_app) -> None:
    view_model = make_wizard(ERRORS_THEN_VIDEO).view_model

    assert view_model.currentStepName == "Errors"

    view_model.next()

    assert view_model.currentStepName == "Video"


def test_back_returns_to_the_previous_step(qt_app, make_spy) -> None:
    view_model = make_wizard(ERRORS_THEN_VIDEO).view_model
    view_model.next()
    spy = make_spy(view_model.currentStepChanged)

    view_model.back()

    assert view_model.currentStepIndex == 0
    assert spy.count() == 1


def test_back_on_the_first_step_stays_put(qt_app, make_spy) -> None:
    view_model = make_wizard(ERRORS_THEN_VIDEO).view_model
    spy = make_spy(view_model.currentStepChanged)

    view_model.back()

    assert view_model.currentStepIndex == 0
    assert spy.count() == 0


def test_next_navigates_forward(qt_app, make_spy) -> None:
    view_model = make_wizard(ERRORS_THEN_VIDEO).view_model
    spy = make_spy(view_model.navigated)

    view_model.next()

    assert spy.count() == 1
    assert spy.at(0, 0) == NavigationDirection.FORWARD


def test_back_navigates_back(qt_app, make_spy) -> None:
    view_model = make_wizard(ERRORS_THEN_VIDEO).view_model
    view_model.next()
    spy = make_spy(view_model.navigated)

    view_model.back()

    assert spy.count() == 1
    assert spy.at(0, 0) == NavigationDirection.BACK


def test_jump_ahead_navigates_forward_once(qt_app, make_spy) -> None:
    view_model = make_wizard(THREE_STEPS).view_model
    spy = make_spy(view_model.navigated)

    view_model.setProperty("currentStepIndex", 2)

    assert spy.count() == 1
    assert spy.at(0, 0) == NavigationDirection.FORWARD


def test_jump_back_navigates_back_once(qt_app, make_spy) -> None:
    view_model = make_wizard(THREE_STEPS).view_model
    view_model.setProperty("currentStepIndex", 2)
    spy = make_spy(view_model.navigated)

    view_model.setProperty("currentStepIndex", 0)

    assert spy.count() == 1
    assert spy.at(0, 0) == NavigationDirection.BACK


def test_staying_put_emits_no_navigation(qt_app, make_spy) -> None:
    view_model = make_wizard(ERRORS_THEN_VIDEO).view_model
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


def test_finish_reports_the_step_answers(qt_app) -> None:
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
    setup = make_wizard(plan)

    # Every answer differs from the step's default, so no value below can come from anywhere but the step.
    step_view_model(setup.view_model, MpvqcImportWizardSessionStepViewModel).setProperty(
        "mode", SessionMode.REPLACE.value
    )
    step_view_model(setup.view_model, MpvqcImportWizardVideoStepViewModel).setProperty("selectedIndex", 1)
    step_view_model(setup.view_model, MpvqcImportWizardSubtitlesStepViewModel).toggle(0)

    setup.view_model.finish()

    assert setup.finished == [
        FinishedPlan(
            comments=(COMMENT,),
            session=SessionReplace(),
            video=VideoLoad(path=VIDEO_B),
            subtitles=SubtitlesLoad(paths=(SUB_B,)),
        )
    ]
