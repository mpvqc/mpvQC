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


import unittest
from unittest.mock import MagicMock

import inject

from mpvqc.services import FilePathService, FileStartupService, ResourceService


class TestFileStartupService(unittest.TestCase):
    MODULE = 'mpvqc.services.file_startup'

    mocked_file_service = MagicMock()

    def setUp(self):
        inject.clear_and_configure(lambda binder: binder
                                   .bind(FilePathService, self.mocked_file_service)
                                   .bind(ResourceService, MagicMock()))

    def tearDown(self):
        inject.clear()

    def test_dir_config_created(self):
        service = FileStartupService()
        service.create_missing_directories()
        self.mocked_file_service.dir_config.mkdir.assert_called()

    def test_dir_backup_created(self):
        service = FileStartupService()
        service.create_missing_directories()
        self.mocked_file_service.dir_backup.mkdir.assert_called()

    def test_dir_screenshots_created(self):
        service = FileStartupService()
        service.create_missing_directories()
        self.mocked_file_service.dir_screenshots.mkdir.assert_called()
