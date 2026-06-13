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

from mpvqc.datamodels import DocumentRejectionReason, RejectedDocument
from mpvqc.dialogs import MpvqcDialogLoaderViewModel
from mpvqc.services import ImporterService, SettingsService
from mpvqc.services.importer import UnfinishedPlan, errors, session, subtitles, video


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
def loader(qt_app) -> MpvqcDialogLoaderViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcDialogLoaderViewModel()


def _assert_view_model_collected(ref: weakref.ref) -> None:
    QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
    gc.collect()
    assert ref() is None


def test_releases_view_model_after_wizard(loader):
    captured: list[weakref.ref] = []
    loader.importWizardDialogRequested.connect(lambda vm: captured.append(weakref.ref(vm)))

    unfinished_plan = UnfinishedPlan(
        comments=(),
        session=session.Merge(),
        video=video.Skip(),
        subtitles=subtitles.Skip(),
        errors=errors.Present(
            rejected_documents=(RejectedDocument(Path("/broken.qc"), DocumentRejectionReason.INVALID),)
        ),
    )

    loader._request_import_wizard(unfinished_plan)
    loader.releaseActiveDialog()

    _assert_view_model_collected(captured[0])


def test_does_not_request_wizard_when_plan_has_no_steps(loader, importer_service_mock):
    requested: list[QObject] = []
    loader.importWizardDialogRequested.connect(lambda vm: requested.append(vm))

    unfinished_plan = UnfinishedPlan(
        comments=(),
        session=session.Merge(),
        video=video.Skip(),
        subtitles=subtitles.Skip(),
        errors=errors.Absent(),
    )

    loader._request_import_wizard(unfinished_plan)

    assert requested == []
    assert loader._active_dialog_vm is None
    importer_service_mock.cancel_pending.assert_called_once_with()


def test_release_cancels_pending_when_importer_busy(loader, importer_service_mock):
    importer_service_mock.busy = True
    loader._active_dialog_vm = QObject()

    loader.releaseActiveDialog()

    importer_service_mock.cancel_pending.assert_called_once_with()


def test_release_does_not_cancel_pending_when_importer_idle(loader, importer_service_mock):
    importer_service_mock.busy = False
    loader._active_dialog_vm = QObject()

    loader.releaseActiveDialog()

    importer_service_mock.cancel_pending.assert_not_called()
