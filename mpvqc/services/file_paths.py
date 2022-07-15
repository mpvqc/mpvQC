#  mpvQC
#
#  Copyright (C) 2022 mpvQC developers
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


from functools import cached_property
from pathlib import Path
from typing import NamedTuple

import inject
from PySide6.QtCore import QCoreApplication, QStandardPaths

from mpvqc.services.app_environment import AppEnvironmentService


class FilePathService:
    _app_environment = inject.attr(AppEnvironmentService)

    class Impl(NamedTuple):
        dir_backup: Path
        dir_config: Path
        dir_screenshots: Path

    @cached_property
    def _impl(self):
        if self._app_environment.is_portable:
            return self._get_portable()
        return self._get_non_portable()

    def _get_portable(self):
        dir_app = self._app_environment.executing_directory
        return FilePathService.Impl(
            dir_backup=dir_app / 'appdata' / 'backups',
            dir_config=dir_app / 'appdata',
            dir_screenshots=dir_app / 'appdata' / 'screenshots'
        )

    @staticmethod
    def _get_non_portable():
        appname = QCoreApplication.applicationName()
        config = QStandardPaths.writableLocation(QStandardPaths.ConfigLocation)
        documents = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
        pictures = QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)
        return FilePathService.Impl(
            dir_backup=Path(documents) / appname / 'backups',
            dir_config=Path(config) / appname,
            dir_screenshots=Path(pictures) / appname
        )

    @cached_property
    def dir_backup(self) -> Path:
        return self._impl.dir_backup

    @cached_property
    def dir_config(self) -> Path:
        return self._impl.dir_config

    @cached_property
    def dir_screenshots(self) -> Path:
        return self._impl.dir_screenshots

    @cached_property
    def file_input_conf(self) -> Path:
        return self.dir_config / 'input.conf'

    @cached_property
    def file_mpv_conf(self) -> Path:
        return self.dir_config / 'mpv.conf'

    @cached_property
    def file_settings(self) -> Path:
        return self.dir_config / 'settings.ini'
