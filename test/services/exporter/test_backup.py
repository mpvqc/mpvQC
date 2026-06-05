# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import QDateTime

from mpvqc.services import ResourceService
from mpvqc.services.exporter.backup import backup


@pytest.fixture
def zip_file():
    with patch("mpvqc.services.exporter.backup.ZipFile", return_value=MagicMock()) as mock:
        yield mock


def test_archive_name(configure_mocks, render_context, application_paths_service_mock, zip_file):
    application_paths_service_mock.dir_backup = Path.home()
    configure_mocks()

    backup(application_paths_service_mock, ResourceService(), render_context)

    assert zip_file.called
    zip_name = zip_file.call_args.args[0]
    assert zip_name.name == f"{datetime.now(UTC):%Y-%m}.zip"


def test_writes_rendered_backup(configure_mocks, render_context, application_paths_service_mock, zip_file):
    configure_mocks(comments=[{"time": 50 * 1000, "commentType": "Spelling", "comment": "My comment"}])

    backup(application_paths_service_mock, ResourceService(), render_context)

    writestr_mock = zip_file.return_value.__enter__.return_value.writestr
    assert writestr_mock.called

    filename, content = writestr_mock.call_args.args
    assert f"{QDateTime.currentDateTime().toString('yyyy-MM-dd')}" in filename
    assert content.startswith("[FILE]")
    assert "[00:00:50] [Spelling] My comment" in content
