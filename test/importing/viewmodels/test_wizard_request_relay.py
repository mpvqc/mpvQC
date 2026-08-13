# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gc
import weakref
from unittest.mock import MagicMock

import inject
import pytest
from PySide6.QtCore import QCoreApplication, QEvent, QObject, Signal

from mpvqc.importing.services import ImportService, PendingImport
from mpvqc.importing.viewmodels import MpvqcImportWizardRequestRelayViewModel, MpvqcImportWizardViewModel
from test.importing.pending import record_pending
from test.importing.plans import PRESENT_ERRORS, plan_with

NEEDS_A_DECISION = plan_with(errors=PRESENT_ERRORS)


class ImporterSignals(QObject):
    # A MagicMock cannot carry a Qt signal, so the substituted importer borrows a real one from here.
    pending_import_ready = Signal(PendingImport)


@pytest.fixture
def importer_signals(qt_app) -> ImporterSignals:
    return ImporterSignals()


@pytest.fixture
def importer_service_mock(importer_signals) -> MagicMock:
    service = MagicMock(spec_set=ImportService)
    service.pending_import_ready = importer_signals.pending_import_ready
    return service


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, importer_service_mock):
    def custom(binder: inject.Binder):
        binder.bind(ImportService, importer_service_mock)

    common_bindings_with(custom)


@pytest.fixture
def relay(qt_app) -> MpvqcImportWizardRequestRelayViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcImportWizardRequestRelayViewModel()


def _assert_view_model_collected(ref: weakref.ref) -> None:
    QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
    gc.collect()
    assert ref() is None


def test_requests_a_wizard_for_a_pending_import(relay, importer_service_mock, make_spy):
    setup = record_pending(NEEDS_A_DECISION)
    spy = make_spy(relay.importWizardRequested)

    importer_service_mock.pending_import_ready.emit(setup.pending)

    assert spy.count() == 1
    assert isinstance(spy.at(invocation=0, argument=0), MpvqcImportWizardViewModel)
    assert setup.dismissals == []


def test_releases_the_wizard_view_model(relay, importer_service_mock):
    # A spy would keep the view model alive, so the weak reference is taken as the signal passes it on.
    captured: list[weakref.ref] = []
    relay.importWizardRequested.connect(lambda view_model: captured.append(weakref.ref(view_model)))

    importer_service_mock.pending_import_ready.emit(record_pending(NEEDS_A_DECISION).pending)
    relay.releaseWizardViewModel()

    _assert_view_model_collected(captured[0])


def test_release_dismisses_the_pending_import(relay, importer_service_mock):
    setup = record_pending(NEEDS_A_DECISION)
    importer_service_mock.pending_import_ready.emit(setup.pending)

    relay.releaseWizardViewModel()

    assert setup.dismissals == [True]


def test_a_second_release_forwards_nothing(relay, importer_service_mock):
    # The app shell releases from a close handler every dialog shares, so most releases meet no wizard.
    setup = record_pending(NEEDS_A_DECISION)
    importer_service_mock.pending_import_ready.emit(setup.pending)

    relay.releaseWizardViewModel()
    relay.releaseWizardViewModel()

    assert setup.dismissals == [True]
