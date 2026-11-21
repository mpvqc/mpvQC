# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from email.message import Message
from typing import TYPE_CHECKING, NamedTuple
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError

import pytest

from mpvqc.shell.services import (
    CheckOutcome,
    NewVersionAvailable,
    ServerError,
    ServerNotReachable,
    UpToDate,
    VersionCheckerService,
)

if TYPE_CHECKING:
    from collections.abc import Callable

MODULE = "mpvqc.shell.services.version_checker"
RUNNING_VERSION = "0.1.0"


@pytest.fixture(autouse=True)
def running_version(monkeypatch, make_build_info) -> None:
    info = make_build_info(version=RUNNING_VERSION)
    monkeypatch.setattr(f"{MODULE}.get_build_info", lambda: info)


class FakeFetch:
    def __init__(self, *responses: str | Exception) -> None:
        self._responses = list(responses)
        self.calls = 0

    def __call__(self) -> str:
        response = self._responses[min(self.calls, len(self._responses) - 1)]
        self.calls += 1
        if isinstance(response, Exception):
            raise response
        return response


@pytest.fixture
def make_service(
    qt_app, manual_executor
) -> Callable[[FakeFetch | None], tuple[VersionCheckerService, list[CheckOutcome]]]:
    def _make(fetch: FakeFetch | None) -> tuple[VersionCheckerService, list[CheckOutcome]]:
        service = (
            VersionCheckerService(manual_executor)
            if fetch is None
            else VersionCheckerService(manual_executor, fetch=fetch)
        )
        outcomes: list[CheckOutcome] = []
        service.outcome_ready.connect(outcomes.append)
        return service, outcomes

    return _make


def _server_error() -> HTTPError:
    return HTTPError("https://example.com", 500, "Internal Error", Message(), None)


class OutcomeCase(NamedTuple):
    name: str
    response: str | Exception
    expected: CheckOutcome


OUTCOME_CASES = [
    OutcomeCase(name="up to date", response=RUNNING_VERSION, expected=UpToDate()),
    OutcomeCase(name="newer", response="0.1.2", expected=NewVersionAvailable(version="0.1.2")),
    OutcomeCase(name="verbatim", response="1.2.3<script>", expected=NewVersionAvailable(version="1.2.3<script>")),
    OutcomeCase(name="server error", response=_server_error(), expected=ServerError(code=500)),
    OutcomeCase(name="not reachable", response=URLError(reason="offline"), expected=ServerNotReachable()),
]


@pytest.mark.parametrize("case", OUTCOME_CASES, ids=lambda case: case.name)
def test_check_emits_outcome_after_fetch(case: OutcomeCase, make_service, manual_executor):
    service, outcomes = make_service(FakeFetch(case.response))

    service.check()
    assert outcomes == []

    manual_executor.drain()
    assert outcomes == [case.expected]


def test_check_reuses_cached_version_synchronously(make_service, manual_executor):
    fetch = FakeFetch("0.1.2")
    service, outcomes = make_service(fetch)
    service.check()
    manual_executor.drain()

    service.check()

    assert outcomes == [NewVersionAvailable(version="0.1.2"), NewVersionAvailable(version="0.1.2")]
    assert fetch.calls == 1
    assert not manual_executor.pending


@pytest.mark.parametrize("error", [_server_error(), URLError(reason="offline")], ids=["server error", "not reachable"])
def test_check_fetches_again_after_error(error: Exception, make_service, manual_executor):
    fetch = FakeFetch(error, RUNNING_VERSION)
    service, outcomes = make_service(fetch)
    service.check()
    manual_executor.drain()

    service.check()
    manual_executor.drain()

    assert fetch.calls == 2
    assert outcomes[-1] == UpToDate()


def test_check_coalesces_while_in_flight(make_service, manual_executor):
    fetch = FakeFetch(RUNNING_VERSION)
    service, outcomes = make_service(fetch)

    service.check()
    service.check()
    manual_executor.drain()

    assert fetch.calls == 1
    assert outcomes == [UpToDate()]


def test_check_logs_unexpected_failure_and_fetches_again(make_service, manual_executor, caplog):
    fetch = FakeFetch(ValueError("malformed"), RUNNING_VERSION)
    service, outcomes = make_service(fetch)
    service.check()
    manual_executor.drain()

    assert outcomes == []
    assert "Version check failed" in caplog.text

    service.check()
    manual_executor.drain()

    assert fetch.calls == 2
    assert outcomes == [UpToDate()]


def test_default_fetch_reads_latest_version_from_update_server(make_service, manual_executor):
    service, outcomes = make_service(None)

    with patch(f"{MODULE}.urllib.request.urlopen") as urlopen:
        response = MagicMock()
        response.read.return_value = b' { "latest": "0.1.2" } \n'
        urlopen.return_value.__enter__.return_value = response
        service.check()
        manual_executor.drain()

    urlopen.assert_called_once_with("https://mpvqc.github.io/api/v1/public/version.json", timeout=5)
    assert outcomes == [NewVersionAvailable(version="0.1.2")]
