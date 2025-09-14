# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

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
        if isinstance(value, str):
            return value.upper() == "TRUE"
        return False

    def _str(self, key: str, default=""):
        return str(self._settings.value(key, default))

    def _int(self, key: str, default=0):
        try:
            return int(self._str(key, default=str(default)))
        except ValueError:
            return default

    @property
    def nickname(self) -> str:
        return self._str("Export/nickname")

    @property
    def writeHeaderDate(self) -> bool:
        return self._bool("Export/writeHeaderDate")

    @property
    def writeHeaderGenerator(self) -> bool:
        return self._bool("Export/writeHeaderGenerator")

    @property
    def writeHeaderNickname(self) -> bool:
        return self._bool("Export/writeHeaderNickname")

    @property
    def writeHeaderVideoPath(self) -> bool:
        return self._bool("Export/writeHeaderVideoPath")

    @property
    def language(self) -> str:
        return self._str("Common/language", default="en-US")

    class ImportWhenVideoLinkedInDocument(Enum):
        ALWAYS = 0
        ASK_EVERY_TIME = 1
        NEVER = 2

    @property
    def import_video_when_video_linked_in_document(self) -> ImportWhenVideoLinkedInDocument:
        default = SettingsService.ImportWhenVideoLinkedInDocument.ASK_EVERY_TIME
        value = self._int("Import/importWhenVideoLinkedInDocument", default=default.value)
        try:
            return self.ImportWhenVideoLinkedInDocument(value)
        except ValueError:
            return default
