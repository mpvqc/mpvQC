# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.services import ExportService, SettingsService
from mpvqc.viewmodels import MpvqcBackupTimerViewModel


@pytest.fixture
def export_service_mock() -> MagicMock:
    return MagicMock(spec_set=ExportService)


@pytest.fixture
def view_model() -> MpvqcBackupTimerViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcBackupTimerViewModel()


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, export_service_mock, settings_service):
    def custom_bindings(binder: inject.Binder):
        binder.bind(ExportService, export_service_mock)
        binder.bind(SettingsService, settings_service)

    common_bindings_with(custom_bindings)


def test_backup_backend(qt_app, view_model, export_service_mock):
    view_model.backup()
    assert export_service_mock.backup.called
