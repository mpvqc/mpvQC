# mpvQC
#
# Copyright (C) 2025 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from unittest.mock import MagicMock

import inject
import pytest
from PySide6.QtCore import QThreadPool

from mpvqc.pyobjects import MpvqcBackupperBackendPyObject
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
