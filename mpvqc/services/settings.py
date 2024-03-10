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

from enum import Enum

import inject
from PySide6.QtCore import QSettings

from .application_paths import ApplicationPathsService
from .type_mapper import TypeMapperService


# noinspection PyPep8Naming
class SettingsService:
    _paths = inject.attr(ApplicationPathsService)
    _type_mapper: TypeMapperService = inject.attr(TypeMapperService)

    def __init__(self):
        path = self._type_mapper.map_path_to_str(self._paths.file_settings)
        self._settings = QSettings(path, QSettings.defaultFormat())

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

    def _int(self, key: str, default=0):
        try:
            return int(self._str(key, default=str(default)))
        except ValueError:
            return default

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

    class ImportWhenVideoLinkedInDocument(Enum):
        ALWAYS = 0
        ASK_EVERY_TIME = 1
        NEVER = 2

    @property
    def import_video_when_video_linked_in_document(self) -> ImportWhenVideoLinkedInDocument:
        default = SettingsService.ImportWhenVideoLinkedInDocument.ASK_EVERY_TIME
        value = self._int('Import/importWhenVideoLinkedInDocument', default=default.value)
        try:
            return self.ImportWhenVideoLinkedInDocument(value)
        except ValueError:
            return default
