# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import urllib.error
import urllib.request
from functools import cache

import inject
from PySide6.QtCore import QCoreApplication

from .build_info import BuildInfoService

_HOME_URL = "https://mpvqc.github.io"
_UPDATE_URL = f"{_HOME_URL}/api/v1/public/version"


@cache
def _fetch_latest_version() -> str:
    with urllib.request.urlopen(_UPDATE_URL, timeout=5) as connection:  # noqa: S310
        text = connection.read().decode("utf-8").strip()
        return f"{json.loads(text)['latest']}".strip()


class VersionCheckerService:
    _build_info = inject.attr(BuildInfoService)

    def check_for_new_version(self) -> tuple[str, str]:
        # fmt: off
        try:
            latest_version = _fetch_latest_version()
        except urllib.error.HTTPError as e:
            title = QCoreApplication.translate("VersionCheckDialog", "Server Error")
            text = QCoreApplication.translate("VersionCheckDialog", "The server returned error code {}.").format(e.code)
            return title, text
        except urllib.error.URLError:
            title = QCoreApplication.translate("VersionCheckDialog", "Server Not Reachable")
            text = QCoreApplication.translate("VersionCheckDialog", "A connection to the server could not be established.")
            return title, text

        if self._build_info.version != latest_version:
            new_version = f"<i>{latest_version}</i>"
            home_url = f'<a href="{_HOME_URL}">{_HOME_URL}</a>'

            title = QCoreApplication.translate("VersionCheckDialog", "New Version Available")
            text = QCoreApplication.translate("VersionCheckDialog", "There is a new version of mpvQC available ({}). Visit {} to download it.") \
                .format(new_version, home_url)
            return title, text

        title = "👌"
        text = QCoreApplication.translate("VersionCheckDialog", "You are already using the most recent version of mpvQC!")
        return title, text
        # fmt: on
