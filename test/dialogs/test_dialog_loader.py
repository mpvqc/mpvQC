# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gc
import weakref
from pathlib import Path
from unittest.mock import MagicMock

import inject
import pytest
from PySide6.QtCore import QCoreApplication, QEvent

from mpvqc.dialogs import MpvqcDialogLoaderViewModel
from mpvqc.services import ImporterService, SettingsService
from mpvqc.services.importer import UnfinishedPlan
from mpvqc.services.importer.concerns import errors, session, subtitles, video


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
        errors=errors.Unresolved(invalid_documents=(Path("/broken.qc"),)),
    )

    loader._request_import_wizard(unfinished_plan)
    loader.releaseActiveDialog()

    _assert_view_model_collected(captured[0])
