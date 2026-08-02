# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import QSettings

from .application_paths import ApplicationPathsService
from .type_mapper import TypeMapperService


class SettingsFileService:
    _paths = inject.attr(ApplicationPathsService)
    _type_mapper = inject.attr(TypeMapperService)

    def __init__(self, ini_file: str | None = None) -> None:
        file = ini_file if ini_file is not None else self._type_mapper.map_path_to_str(self._paths.file_settings)
        self._qsettings = QSettings(file, QSettings.Format.IniFormat)

    @property
    def qsettings(self) -> QSettings:
        return self._qsettings
