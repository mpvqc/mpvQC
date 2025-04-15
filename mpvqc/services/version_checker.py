# mpvQC
#
# Copyright (C) 2022 mpvQC developers
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

import json
import urllib.error
import urllib.request
from functools import cache

from PySide6.QtCore import QCoreApplication


class VersionCheckerService:
    HOME_URL = "https://mpvqc.github.io"
    UPDATE_URL = f"{HOME_URL}/api/v1/public/version"

    @property
    def _current_version(self) -> str:
        return QCoreApplication.instance().applicationVersion()

    def check_for_new_version(self) -> tuple[str, str]:
        # fmt: off
        try:
            latest_version = self._fetch_latest_version()
        except urllib.error.HTTPError as e:
            title = QCoreApplication.translate("VersionCheckDialog", "Server Error")
            text = QCoreApplication.translate("VersionCheckDialog", "The server returned error code {}.").format(e.code)
            return title, text
        except urllib.error.URLError:
            title = QCoreApplication.translate("VersionCheckDialog", "Server Not Reachable")
            text = QCoreApplication.translate("VersionCheckDialog", "A connection to the server could not be established.")
            return title, text

        if self._current_version != latest_version:
            new_version = f'<i>{latest_version}</i>'
            home_url = f'<a href="{self.HOME_URL}">{self.HOME_URL}</a>'

            title = QCoreApplication.translate("VersionCheckDialog", "New Version Available")
            text = QCoreApplication.translate("VersionCheckDialog", "There is a new version of mpvQC available ({}). Visit {} to download it.") \
                .format(new_version, home_url)
            return title, text

        title = "👌"
        text = QCoreApplication.translate("VersionCheckDialog", "You are already using the most recent version of mpvQC!")
        return title, text
        # fmt: on

    @cache
    def _fetch_latest_version(self) -> str:
        with urllib.request.urlopen(self.UPDATE_URL, timeout=5) as connection:
            text = connection.read().decode("utf-8").strip()
            return f"{json.loads(text)['latest']}".strip()
