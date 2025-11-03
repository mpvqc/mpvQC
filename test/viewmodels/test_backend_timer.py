# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest
from PySide6.QtCore import QThreadPool

from mpvqc.services import DocumentBackupService, SettingsService
from mpvqc.viewmodels import MpvqcBackupTimerViewModel


@pytest.fixture
def backup_service_mock() -> MagicMock:
    return MagicMock(spec_set=DocumentBackupService)


@pytest.fixture
def view_model() -> MpvqcBackupTimerViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcBackupTimerViewModel()


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, backup_service_mock, settings_service):
    def custom_bindings(binder: inject.Binder):
        binder.bind(DocumentBackupService, backup_service_mock)
        binder.bind(SettingsService, settings_service)

    common_bindings_with(custom_bindings)


def test_backup_backend(view_model, backup_service_mock):
    view_model.backup()
    QThreadPool.globalInstance().waitForDone(100)
    assert backup_service_mock.backup.called
