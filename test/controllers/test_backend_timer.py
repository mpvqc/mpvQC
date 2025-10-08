# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest
from PySide6.QtCore import QThreadPool

from mpvqc.controllers import MpvqcBackupTimerViewModel
from mpvqc.services import DocumentBackupService, SettingsService


@pytest.fixture
def backup_service_mock() -> MagicMock:
    return MagicMock(spec_set=DocumentBackupService)


@pytest.fixture
def controller() -> MpvqcBackupTimerViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcBackupTimerViewModel()


@pytest.fixture(autouse=True)
def configure_injections(backup_service_mock, settings_service):
    def config(binder: inject.Binder):
        binder.bind(DocumentBackupService, backup_service_mock)
        binder.bind(SettingsService, settings_service)

    inject.configure(config, clear=True)


def test_backup_backend(controller, backup_service_mock):
    controller.backup()
    QThreadPool.globalInstance().waitForDone(100)
    assert backup_service_mock.backup.called
