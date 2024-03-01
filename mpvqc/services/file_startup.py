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

import inject

from .application_paths import ApplicationPathsService
from .resource import ResourceService


class FileStartupService:
    _paths: ApplicationPathsService = inject.attr(ApplicationPathsService)
    _resources: ResourceService = inject.attr(ResourceService)

    def create_missing_directories(self) -> None:
        self._paths.dir_config.mkdir(exist_ok=True, parents=True)
        self._paths.dir_backup.mkdir(exist_ok=True, parents=True)
        self._paths.dir_screenshots.mkdir(exist_ok=True, parents=True)
        self._paths.dir_export_templates.mkdir(exist_ok=True, parents=True)

    def create_missing_files(self) -> None:
        self._create_missing_input_conf()
        self._create_missing_mpv_conf()
        self._create_missing_export_template_readme()

    def _create_missing_input_conf(self) -> None:
        self._create_missing_file(
            path=self._paths.file_input_conf,
            content=self._resources.input_conf_content
        )

    def _create_missing_mpv_conf(self) -> None:
        self._create_missing_file(
            path=self._paths.file_mpv_conf,
            content=self._resources.mpv_conf_content
        )

    def _create_missing_export_template_readme(self) -> None:
        self._create_missing_file(
            path=self._paths.file_export_template_readme,
            content=self._resources.export_template_readme
        )

    @staticmethod
    def _create_missing_file(path: Path, content: str) -> None:
        if not path.exists():
            path.write_text(content, encoding='utf-8', newline='\n')
