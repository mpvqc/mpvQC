# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from email.message import Message
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError

import inject
import pytest

from mpvqc.services import BuildInfoService, VersionCheckerService
from mpvqc.services.version_checker import NewVersionAvailable, ServerError, ServerNotReachable, UpToDate

MODULE = "mpvqc.services.version_checker"


@pytest.fixture
def build_info_service_mock() -> MagicMock:
    return MagicMock(spec_set=BuildInfoService)


@pytest.fixture(autouse=True)
def configure_inject(
    common_bindings_with,
    build_info_service_mock,
):
    def custom_bindings(binder: inject.Binder):
        binder.bind(BuildInfoService, build_info_service_mock)

    common_bindings_with(custom_bindings)


def mock_response(mock, *, status=200, body="", error=None):
    if error:
        mock.side_effect = error
        return

    context_manager_mock = MagicMock()
    context_manager_mock.getcode.return_value = status
    context_manager_mock.read.return_value = body.encode()
    context_manager_mock.__enter__.return_value = context_manager_mock
    mock.return_value = context_manager_mock


@pytest.fixture
def service() -> VersionCheckerService:
    return VersionCheckerService()


def test_version_checker_latest(service, build_info_service_mock):
    build_info_service_mock.version = "0.1.0"

    with patch(f"{MODULE}.urllib.request.urlopen") as mock_request:
        mock_response(mock_request, body='{ "latest": "0.1.0" }')
        outcome = service.check_for_new_version()

    assert outcome == UpToDate()


def test_version_checker_new_version_available(service, build_info_service_mock):
    build_info_service_mock.version = "0.1.1"

    with patch(f"{MODULE}.urllib.request.urlopen") as mock_request:
        mock_response(mock_request, body='{ "latest": "0.1.2" }')
        outcome = service.check_for_new_version()

    assert outcome == NewVersionAvailable(version="0.1.2")


def test_version_checker_reports_remote_version_verbatim(service, build_info_service_mock):
    build_info_service_mock.version = "0.1.1"

    with patch(f"{MODULE}.urllib.request.urlopen") as mock_request:
        mock_response(mock_request, body='{ "latest": "1.2.3<script>" }')
        outcome = service.check_for_new_version()

    assert outcome == NewVersionAvailable(version="1.2.3<script>")


def test_version_checker_service_error(service):
    error = HTTPError("https://example.com", 500, "Internal Error", Message(), None)

    with patch(f"{MODULE}.urllib.request.urlopen") as mock_request:
        mock_response(mock_request, error=error)
        outcome = service.check_for_new_version()

    assert outcome == ServerError(code=500)


def test_version_checker_url_error(service):
    error = URLError(reason="it's a mock, brooooo")

    with patch(f"{MODULE}.urllib.request.urlopen") as mock_request:
        mock_response(mock_request, error=error)
        outcome = service.check_for_new_version()

    assert outcome == ServerNotReachable()
