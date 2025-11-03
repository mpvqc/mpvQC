# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import QDateTime

from mpvqc.services import DocumentBackupService

from .conftest import MODULE


@pytest.fixture
def service() -> DocumentBackupService:
    return DocumentBackupService()


@pytest.fixture
def zip_file():
    with patch(f"{MODULE}.ZipFile", return_value=MagicMock()) as mock:
        yield mock


def test_archive_name(configure_mocks, application_paths_service_mock, zip_file, service):
    application_paths_service_mock.dir_backup = Path.home()
    configure_mocks()

    service.backup()

    assert zip_file.called
    zip_name = zip_file.call_args.args[0]
    assert zip_name.name == f"{datetime.now(UTC):%Y-%m}.zip"


def test_render_called(configure_mocks, document_render_service_mock, zip_file, service):
    configure_mocks()

    service.backup()

    writestr_mock = zip_file.return_value.__enter__.return_value.writestr
    assert writestr_mock.called

    filename, content = writestr_mock.call_args.args
    assert f"{QDateTime.currentDateTime().toString('yyyy-MM-dd')}" in filename
    document_render_service_mock.render.assert_called_once()
