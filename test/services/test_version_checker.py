# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError

import pytest

from mpvqc.services import VersionCheckerService

MODULE = "mpvqc.services.version_checker"


def mock_response(mock, *, status=200, body="", error=None):
    if error:
        mock.side_effect = error
        return

    context_manager_mock = MagicMock()
    context_manager_mock.getcode.return_value = status
    context_manager_mock.read.return_value = body.encode()
    context_manager_mock.__enter__.return_value = context_manager_mock
    mock.return_value = context_manager_mock


def mock_current_version(mock, *, version: str):
    mock.return_value.applicationVersion.return_value = version


@pytest.fixture
def service() -> VersionCheckerService:
    return VersionCheckerService()


def test_version_checker_latest(service):
    with (
        patch(f"{MODULE}.urllib.request.urlopen") as mock_request,
        patch(f"{MODULE}.QCoreApplication.instance") as mock_app,
    ):
        mock_response(mock_request, body='{ "latest": "0.1.0" }')
        mock_current_version(mock_app, version="0.1.0")
        actual_title, _ = service.check_for_new_version()

    assert actual_title == "👌"


def test_version_checker_new_version_available(service):
    with (
        patch(f"{MODULE}.urllib.request.urlopen") as mock_request,
        patch(f"{MODULE}.QCoreApplication.instance") as mock_app,
    ):
        mock_response(mock_request, body='{ "latest": "0.1.0" }')
        mock_current_version(mock_app, version="0.1.1")
        actual_title, _ = service.check_for_new_version()

    assert actual_title == "New Version Available"


def test_version_checker_service_error(service):
    error = HTTPError("https://example.com", 500, "Internal Error", {}, None)

    with patch(f"{MODULE}.urllib.request.urlopen") as mock_request:
        mock_response(mock_request, error=error)
        actual_title, _ = service.check_for_new_version()

    assert actual_title == "Server Error"


def test_version_checker_url_error(service):
    error = URLError(reason="it's a mock, brooooo")

    with patch(f"{MODULE}.urllib.request.urlopen") as mock_request:
        mock_response(mock_request, error=error)
        actual_title, _ = service.check_for_new_version()

    assert actual_title == "Server Not Reachable"
