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
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import inject

from mpvqc.services import ApplicationPathsService, BackupService


class TestPortableFileService(unittest.TestCase):
    MODULE = 'mpvqc.services.backup'

    any_directory = Path('any-directory')

    def setUp(self):
        mock = MagicMock()
        mock.is_portable = True
        mock.dir_backup = self.any_directory
        inject.clear_and_configure(lambda binder: binder
                                   .bind(ApplicationPathsService, mock))

    def tearDown(self):
        inject.clear()

    @patch(f'{MODULE}.ZipFile')
    def test_zip_name(self, zip_file_mock: MagicMock):
        service = BackupService()
        service.backup('video', 'expected-content')

        zip_file_mock.assert_called()

        zip_name = zip_file_mock.call_args.args[0]
        self.assertEqual(f'{datetime.now():%Y-%m}.zip', zip_name.name)

    @patch(f'{MODULE}.ZipFile')
    def test_zip_content(self, zip_file_mock: MagicMock):
        service = BackupService()
        service.backup('video', 'expected-content')

        writestr_mock = zip_file_mock.return_value.__enter__.return_value.writestr
        writestr_mock.assert_called()

        filename, content = writestr_mock.call_args.args
        self.assertIn(f'{datetime.now():%Y-%m-%d}', filename)
        self.assertEqual('expected-content', content)
