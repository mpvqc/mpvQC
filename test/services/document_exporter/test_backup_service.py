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
def document_backup_service() -> DocumentBackupService:
    return DocumentBackupService()


@pytest.fixture
def zip_file():
    with patch(f"{MODULE}.ZipFile", return_value=MagicMock()) as mock:
        yield mock


def test_backup_service_archive_name(make_mock, zip_file, document_backup_service):
    make_mock()

    document_backup_service.backup()

    assert zip_file.called
    zip_name = zip_file.call_args.args[0]
    assert zip_name.name == f"{datetime.now(UTC):%Y-%m}.zip"


def test_backup_service_performs_backup(make_mock, zip_file, document_backup_service):
    make_mock(
        video="/path/to/nice/video",
        comments=[
            {"time": 0, "commentType": "Frrrranky", "comment": "Suuuuuuuper"},
        ],
    )

    document_backup_service.backup()

    writestr_mock = zip_file.return_value.__enter__.return_value.writestr
    assert writestr_mock.called

    filename, content = writestr_mock.call_args.args
    assert f"{QDateTime.currentDateTime().toString('yyyy-MM-dd')}" in filename
    assert f"{Path('/path/to/nice/video')}" in content
    assert "[00:00:00] [Frrrranky] Suuuuuuuper" in content
