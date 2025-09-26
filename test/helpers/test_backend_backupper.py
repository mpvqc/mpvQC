# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest
from PySide6.QtCore import QThreadPool

from mpvqc.helpers import MpvqcBackupperBackendPyObject
from mpvqc.services import DocumentBackupService


@pytest.fixture
def backup_service_mock() -> MagicMock:
    return MagicMock(spec=DocumentBackupService)


@pytest.fixture(autouse=True)
def configure_injections(backup_service_mock):
    def config(binder: inject.Binder):
        binder.bind(DocumentBackupService, backup_service_mock)

    inject.configure(config, clear=True)


def test_backup_backend(backup_service_mock: MagicMock):
    backend = MpvqcBackupperBackendPyObject()
    backend.backup()
    QThreadPool.globalInstance().waitForDone(100)
    assert backup_service_mock.backup.called
