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

from functools import cached_property
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
        if self._app.built_by_pyinstaller:
            self._paths = self._local_paths()
        elif self._app.runs_as_flatpak:
            self._paths = self._system_paths()
        else:
            self._paths = self._local_paths()

    def _local_paths(self) -> 'ApplicationPathsService.Paths':
        dir_app = self._app.executing_directory
        return ApplicationPathsService.Paths(
            dir_backup=dir_app / 'appdata' / 'backups',
            dir_config=dir_app / 'appdata',
            dir_screenshots=dir_app / 'appdata' / 'screenshots',
            dir_export_templates=dir_app / 'appdata' / 'export-templates',
        )

    @staticmethod
    def _system_paths() -> 'ApplicationPathsService.Paths':
        appname = QCoreApplication.applicationName()
        config = QStandardPaths.writableLocation(QStandardPaths.ConfigLocation)
        documents = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
        pictures = QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)
        return ApplicationPathsService.Paths(
            dir_backup=Path(documents) / appname / 'backups',
            dir_config=Path(config) / appname,
            dir_screenshots=Path(pictures) / appname,
            dir_export_templates=Path(config) / appname / 'export-templates',
        )

    @cached_property
    def dir_backup(self) -> Path:
        return self._paths.dir_backup

    @cached_property
    def dir_config(self) -> Path:
        return self._paths.dir_config

    @cached_property
    def dir_screenshots(self) -> Path:
        return self._paths.dir_screenshots

    @cached_property
    def dir_export_templates(self) -> Path:
        return self._paths.dir_export_templates

    @cached_property
    def file_input_conf(self) -> Path:
        return self.dir_config / 'input.conf'

    @cached_property
    def file_mpv_conf(self) -> Path:
        return self.dir_config / 'mpv.conf'

    @cached_property
    def file_settings(self) -> Path:
        return self.dir_config / 'settings.ini'

    @cached_property
    def file_mpvqc_export_template(self) -> Path:
        return self.dir_export_templates / 'mpvQC-export.template'

    @property
    def files_export_templates(self) -> tuple[Path, ...]:
        return tuple(self.dir_export_templates.glob("*.jinja"))
