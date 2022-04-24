#  mpvQC
#
#  Copyright (C) 2022 mpvQC developers
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


import inject

from mpvqc.impl import FileWriter
from mpvqc.services.file_paths import FilePathService
from mpvqc.services.resource import ResourceService


class FileStartupService:
    _paths = inject.attr(FilePathService)
    _resources = inject.attr(ResourceService)

    def create_missing_directories(self):
        self._paths.dir_config.mkdir(exist_ok=True, parents=True)
        self._paths.dir_backup.mkdir(exist_ok=True, parents=True)
        self._paths.dir_screenshots.mkdir(exist_ok=True, parents=True)

    def create_missing_files(self):
        self._create_missing_input_conf()
        self._create_missing_mpv_conf()

    def _create_missing_input_conf(self):
        path = self._paths.file_input_conf
        file_writer = FileWriter(path)

        if file_writer.file_doesnt_exist():
            default_text = self._resources.input_conf_content
            file_writer.write(default_text)

    def _create_missing_mpv_conf(self):
        path = self._paths.file_mpv_conf
        file_writer = FileWriter(path)

        if file_writer.file_doesnt_exist():
            default_text = self._resources.mpv_conf_content
            file_writer.write(default_text)
