# mpvQC
#
# Copyright (C) 2024 mpvQC developers
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

import inject
from PySide6.QtCore import QSettings

from .application_paths import ApplicationPathsService


# noinspection PyPep8Naming
class SettingsService:
    _paths = inject.attr(ApplicationPathsService)

    def __init__(self):
        settings_file_path = self._paths.file_settings.absolute()
        self._settings = QSettings(str(settings_file_path), QSettings.defaultFormat())

    def _bool(self, key: str):
        value = self._settings.value(key, False)
        if isinstance(value, bool):
            return value
        elif isinstance(value, str):
            return value.upper() == 'TRUE'
        else:
            return False

    def _str(self, key: str, default=''):
        return str(self._settings.value(key, default))

    @property
    def nickname(self) -> str:
        return self._str('Export/nickname')

    @property
    def writeHeaderDate(self) -> bool:
        return self._bool('Export/writeHeaderDate')

    @property
    def writeHeaderGenerator(self) -> bool:
        return self._bool('Export/writeHeaderGenerator')

    @property
    def writeHeaderNickname(self) -> bool:
        return self._bool('Export/writeHeaderNickname')

    @property
    def writeHeaderVideoPath(self) -> bool:
        return self._bool('Export/writeHeaderVideoPath')

    @property
    def language(self) -> str:
        return self._str('Common/language', default='en-US')
