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

import unittest
from unittest.mock import MagicMock

import inject
from parameterized import parameterized

from mpvqc.services import ApplicationPathsService, FileStartupService, ResourceService


class FileStartupServiceTest(unittest.TestCase):
    MODULE = "mpvqc.services.file_startup"

    mocked_file_service = MagicMock()

    def setUp(self):
        # fmt: off
        inject.clear_and_configure(lambda binder: binder
                                   .bind(ApplicationPathsService, self.mocked_file_service)
                                   .bind(ResourceService, MagicMock()))
        # fmt: on

    def tearDown(self):
        inject.clear()

    @parameterized.expand(
        [
            "dir_config",
            "dir_backup",
            "dir_screenshots",
            "dir_export_templates",
        ]
    )
    def test_directories_created(self, mocked_dir):
        service = FileStartupService()
        service.create_missing_directories()
        path_mock = getattr(self.mocked_file_service, mocked_dir)
        path_mock.mkdir.assert_called()

    @parameterized.expand(
        [
            "file_input_conf",
            "file_mpv_conf",
        ]
    )
    def test_files_created(self, mocked_file):
        path_mock = getattr(self.mocked_file_service, mocked_file)
        path_mock.exists.return_value = False

        service = FileStartupService()
        service.create_missing_files()

        path_mock.exists.assert_called()
        path_mock.write_text.assert_called()
