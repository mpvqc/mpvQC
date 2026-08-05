# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gc
import weakref
from pathlib import Path
from unittest.mock import MagicMock

import inject
import pytest
from PySide6.QtCore import QCoreApplication, QEvent, QObject

from mpvqc.importing.domain import (
    DocumentRejectionReason,
    RejectedDocument,
    UnfinishedPlan,
    errors,
    session,
    subtitles,
    video,
)
from mpvqc.importing.services import ImporterService
from mpvqc.importing.viewmodels import MpvqcImportWizardRequestRelayViewModel
from mpvqc.services import SettingsService


@pytest.fixture
def importer_service_mock() -> MagicMock:
    service = MagicMock(spec_set=ImporterService)
    service.unfinished_plan_ready = MagicMock()
    return service


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, importer_service_mock, settings_service):
    def custom(binder: inject.Binder):
        binder.bind(ImporterService, importer_service_mock)
        binder.bind(SettingsService, settings_service)

    common_bindings_with(custom)


@pytest.fixture
def relay(qt_app) -> MpvqcImportWizardRequestRelayViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcImportWizardRequestRelayViewModel()


def _assert_view_model_collected(ref: weakref.ref) -> None:
    QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
    gc.collect()
    assert ref() is None


def test_releases_view_model_after_wizard(relay):
    captured: list[weakref.ref] = []
    relay.importWizardRequested.connect(lambda vm: captured.append(weakref.ref(vm)))

    unfinished_plan = UnfinishedPlan(
        comments=(),
        session=session.Merge(),
        video=video.Skip(),
        subtitles=subtitles.Skip(),
        errors=errors.Present(
            rejected_documents=(RejectedDocument(Path("/broken.qc"), DocumentRejectionReason.INVALID),)
        ),
    )

    relay._request_import_wizard(unfinished_plan)
    relay.releaseWizardViewModel()

    _assert_view_model_collected(captured[0])


def test_does_not_request_wizard_when_plan_has_no_steps(relay, importer_service_mock):
    requested: list[QObject] = []
    relay.importWizardRequested.connect(lambda vm: requested.append(vm))

    unfinished_plan = UnfinishedPlan(
        comments=(),
        session=session.Merge(),
        video=video.Skip(),
        subtitles=subtitles.Skip(),
        errors=errors.Absent(),
    )

    relay._request_import_wizard(unfinished_plan)

    assert requested == []
    assert relay._wizard_vm is None
    importer_service_mock.cancel_pending.assert_called_once_with()


def test_release_cancels_pending_when_importer_busy(relay, importer_service_mock):
    importer_service_mock.busy = True
    relay._wizard_vm = QObject()

    relay.releaseWizardViewModel()

    importer_service_mock.cancel_pending.assert_called_once_with()


def test_release_does_not_cancel_pending_when_importer_idle(relay, importer_service_mock):
    importer_service_mock.busy = False
    relay._wizard_vm = QObject()

    relay.releaseWizardViewModel()

    importer_service_mock.cancel_pending.assert_not_called()
