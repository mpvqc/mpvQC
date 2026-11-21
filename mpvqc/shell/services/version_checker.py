# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import logging
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal

from mpvqc.build import get_build_info
from mpvqc.jobs import Err, Ok, SerialJobRunner

if TYPE_CHECKING:
    from collections.abc import Callable

    from mpvqc.jobs import JobExecutor, Result

HOME_URL = "https://mpvqc.github.io"
_UPDATE_URL = f"{HOME_URL}/api/v1/public/version.json"

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class NewVersionAvailable:
    version: str


@dataclass(frozen=True)
class UpToDate:
    """The running build matches the latest published version."""


@dataclass(frozen=True)
class ServerError:
    """The update server answered with an error status."""

    code: int


@dataclass(frozen=True)
class ServerNotReachable:
    """No connection to the update server."""


type CheckOutcome = NewVersionAvailable | UpToDate | ServerError | ServerNotReachable


def fetch_latest_version() -> str:
    with urllib.request.urlopen(_UPDATE_URL, timeout=5) as connection:  # ruff: ignore[suspicious-url-open-usage]
        text = connection.read().decode("utf-8").strip()
    return f"{json.loads(text)['latest']}".strip()


def _outcome_for(latest_version: str) -> CheckOutcome:
    if get_build_info().version != latest_version:
        return NewVersionAvailable(version=latest_version)
    return UpToDate()


class VersionCheckerService(QObject):
    outcome_ready = Signal(object)  # CheckOutcome union; Qt sigs can't carry type aliases

    def __init__(
        self,
        executor: JobExecutor | None = None,
        fetch: Callable[[], str] = fetch_latest_version,
    ) -> None:
        super().__init__()
        self._fetch = fetch
        self._jobs = SerialJobRunner(executor)
        self._cached_version: str | None = None
        self._in_flight = False

    def check(self) -> None:
        """Connect to outcome_ready first: with a cached version, check() emits before it returns."""
        if self._cached_version is not None:
            self.outcome_ready.emit(_outcome_for(self._cached_version))
        elif not self._in_flight:
            self._in_flight = True
            self._jobs.run(work=self._fetch, on_result=self._deliver)

    def _deliver(self, result: Result[str]) -> None:
        self._in_flight = False
        match result:
            case Ok(version):
                self._cached_version = version
                self.outcome_ready.emit(_outcome_for(version))
            case Err(urllib.error.HTTPError() as error):
                self.outcome_ready.emit(ServerError(code=error.code))
            case Err(urllib.error.URLError()):
                self.outcome_ready.emit(ServerNotReachable())
            case Err(error):
                logger.error("Version check failed", exc_info=error)
