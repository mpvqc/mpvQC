# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import QSettings

from mpvqc.shared import map_path_to_str

from .application_paths import ApplicationPathsService


class SettingsFileService:
    _paths = inject.attr(ApplicationPathsService)

    def __init__(self, ini_file: str | None = None) -> None:
        file = ini_file if ini_file is not None else map_path_to_str(self._paths.file_settings)
        self._qsettings = QSettings(file, QSettings.Format.IniFormat)

    @property
    def qsettings(self) -> QSettings:
        return self._qsettings
