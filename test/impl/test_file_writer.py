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
from pathlib import Path
from unittest.mock import patch, Mock

from mpvqc.impl import FileWriter


class TestFileWriter(unittest.TestCase):
    MODULE = 'mpvqc.impl.file_writer'

    @patch(f'{MODULE}.Path.exists', return_value=False)
    def test_file_doesnt_exist(self, *_):
        writer = FileWriter(Path())
        self.assertFalse(writer.file_exists())
        self.assertTrue(writer.file_doesnt_exist())

    @patch(f'{MODULE}.Path.exists', return_value=True)
    def test_file_exists(self, *_):
        writer = FileWriter(Path())
        self.assertTrue(writer.file_exists())
        self.assertFalse(writer.file_doesnt_exist())

    @patch(f'{MODULE}.Path.write_text')
    def test_write(self, mocked_func: Mock):
        writer = FileWriter(Path())
        writer.write('')
        mocked_func.assert_called()
