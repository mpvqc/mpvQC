# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import urllib.error
import urllib.request
from dataclasses import dataclass

import inject

from .build_info import BuildInfoService

HOME_URL = "https://mpvqc.github.io"
_UPDATE_URL = f"{HOME_URL}/api/v1/public/version"


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


class VersionCheckerService:
    _build_info = inject.attr(BuildInfoService)

    def __init__(self) -> None:
        self._cached_version: str | None = None

    def _get_latest_version(self) -> str:
        if (version := self._cached_version) is None:
            with urllib.request.urlopen(_UPDATE_URL, timeout=5) as connection:  # noqa: S310
                text = connection.read().decode("utf-8").strip()
                version = f"{json.loads(text)['latest']}".strip()
            self._cached_version = version
        return version

    def check_for_new_version(self) -> CheckOutcome:
        try:
            latest_version = self._get_latest_version()
        except urllib.error.HTTPError as e:
            return ServerError(code=e.code)
        except urllib.error.URLError:
            return ServerNotReachable()

        if self._build_info.version != latest_version:
            return NewVersionAvailable(version=latest_version)
        return UpToDate()
