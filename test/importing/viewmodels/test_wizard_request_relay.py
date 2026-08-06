# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gc
import weakref
from dataclasses import replace
from unittest.mock import MagicMock

import inject
import pytest
from PySide6.QtCore import QCoreApplication, QEvent, QObject, Signal

from mpvqc.importing.domain import UnfinishedPlan
from mpvqc.importing.services import ImporterService
from mpvqc.importing.viewmodels import MpvqcImportWizardRequestRelayViewModel, MpvqcImportWizardViewModel
from test.importing.viewmodels.plans import ALL_RESOLVED, PRESENT_ERRORS

NOTHING_TO_DECIDE = ALL_RESOLVED

NEEDS_A_DECISION = replace(NOTHING_TO_DECIDE, errors=PRESENT_ERRORS)


class ImporterSignals(QObject):
    # A MagicMock cannot carry a Qt signal, so the substituted importer borrows a real one from here.
    unfinished_plan_ready = Signal(UnfinishedPlan)


@pytest.fixture
def importer_signals(qt_app) -> ImporterSignals:
    return ImporterSignals()


@pytest.fixture
def importer_service_mock(importer_signals) -> MagicMock:
    service = MagicMock(spec_set=ImporterService)
    service.unfinished_plan_ready = importer_signals.unfinished_plan_ready
    service.busy = False
    return service


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, importer_service_mock):
    def custom(binder: inject.Binder):
        binder.bind(ImporterService, importer_service_mock)

    common_bindings_with(custom)


@pytest.fixture
def relay(qt_app) -> MpvqcImportWizardRequestRelayViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcImportWizardRequestRelayViewModel()


def _assert_view_model_collected(ref: weakref.ref) -> None:
    QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
    gc.collect()
    assert ref() is None


def test_requests_a_wizard_for_a_plan_with_decisions(relay, importer_service_mock, make_spy):
    spy = make_spy(relay.importWizardRequested)

    importer_service_mock.unfinished_plan_ready.emit(NEEDS_A_DECISION)

    assert spy.count() == 1
    assert isinstance(spy.at(invocation=0, argument=0), MpvqcImportWizardViewModel)
    importer_service_mock.cancel_pending.assert_not_called()


def test_does_not_request_a_wizard_when_the_plan_has_no_steps(relay, importer_service_mock, make_spy):
    spy = make_spy(relay.importWizardRequested)

    importer_service_mock.unfinished_plan_ready.emit(NOTHING_TO_DECIDE)

    assert spy.count() == 0
    importer_service_mock.cancel_pending.assert_called_once_with()


def test_releases_the_wizard_view_model(relay, importer_service_mock):
    # A spy would keep the view model alive, so the weak reference is taken as the signal passes it on.
    captured: list[weakref.ref] = []
    relay.importWizardRequested.connect(lambda view_model: captured.append(weakref.ref(view_model)))

    importer_service_mock.unfinished_plan_ready.emit(NEEDS_A_DECISION)
    relay.releaseWizardViewModel()

    _assert_view_model_collected(captured[0])


def test_release_cancels_a_pending_import(relay, importer_service_mock):
    importer_service_mock.busy = True
    importer_service_mock.unfinished_plan_ready.emit(NEEDS_A_DECISION)

    relay.releaseWizardViewModel()

    importer_service_mock.cancel_pending.assert_called_once_with()


def test_release_does_not_cancel_when_the_importer_is_idle(relay, importer_service_mock):
    importer_service_mock.busy = False
    importer_service_mock.unfinished_plan_ready.emit(NEEDS_A_DECISION)

    relay.releaseWizardViewModel()

    importer_service_mock.cancel_pending.assert_not_called()


def test_release_with_no_wizard_open_does_nothing(relay, importer_service_mock):
    # Busy, so a release that skipped the no-wizard guard would cancel the import.
    importer_service_mock.busy = True

    relay.releaseWizardViewModel()

    importer_service_mock.cancel_pending.assert_not_called()
