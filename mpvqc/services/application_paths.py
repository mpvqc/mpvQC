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

from pathlib import Path
from typing import NamedTuple

import inject
from PySide6.QtCore import QCoreApplication, QStandardPaths

from .application_environment import ApplicationEnvironmentService


class ApplicationPathsService:
    _app = inject.attr(ApplicationEnvironmentService)

    class Paths(NamedTuple):
        dir_backup: Path
        dir_config: Path
        dir_screenshots: Path
        dir_export_templates: Path

    def __init__(self):
        if self._app.is_portable:
            self._paths = self._paths_next_to_executable()
        else:
            self._paths = self._xdg_paths()

    def _paths_next_to_executable(self) -> "ApplicationPathsService.Paths":
        dir_app = self._app.executing_directory
        return ApplicationPathsService.Paths(
            dir_backup=dir_app / "appdata" / "backups",
            dir_config=dir_app / "appdata",
            dir_screenshots=dir_app / "appdata" / "screenshots",
            dir_export_templates=dir_app / "appdata" / "export-templates",
        )

    @staticmethod
    def _xdg_paths() -> "ApplicationPathsService.Paths":
        appname = QCoreApplication.applicationName()
        config = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.ConfigLocation)
        documents = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        pictures = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.PicturesLocation)
        return ApplicationPathsService.Paths(
            dir_backup=Path(documents) / appname / "backups",
            dir_config=Path(config) / appname,
            dir_screenshots=Path(pictures) / appname,
            dir_export_templates=Path(config) / appname / "export-templates",
        )

    @property
    def dir_backup(self) -> Path:
        return self._paths.dir_backup

    @property
    def dir_config(self) -> Path:
        return self._paths.dir_config

    @property
    def dir_screenshots(self) -> Path:
        return self._paths.dir_screenshots

    @property
    def dir_export_templates(self) -> Path:
        return self._paths.dir_export_templates

    @property
    def file_input_conf(self) -> Path:
        return self.dir_config / "input.conf"

    @property
    def file_mpv_conf(self) -> Path:
        return self.dir_config / "mpv.conf"

    @property
    def file_settings(self) -> Path:
        return self.dir_config / "settings.ini"

    @property
    def files_export_templates(self) -> tuple[Path, ...]:
        return tuple(self.dir_export_templates.glob("*.jinja"))
