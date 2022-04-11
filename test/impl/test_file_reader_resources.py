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
from unittest.mock import patch, Mock

from mpvqc.impl import ResourceFileReader


class TestResourceFileReader(unittest.TestCase):
    MODULE = 'mpvqc.impl.file_reader_resources'

    def test_make_resource_path_simple(self):
        reader = ResourceFileReader()

        expected, data = ':/data', 'data'
        actual = reader._make_resource_path_from(data)

        self.assertEqual(expected, actual)

    def test_make_resource_path_slash(self):
        reader = ResourceFileReader()

        expected, data = ':/data', '/data'
        actual = reader._make_resource_path_from(data)

        self.assertEqual(expected, actual)

    def test_make_resource_path_complete(self):
        reader = ResourceFileReader()

        expected, data = ':/data', ':/data'
        actual = reader._make_resource_path_from(data)

        self.assertEqual(expected, actual)

    @patch(f'{MODULE}.QFile.open', return_value=True)
    @patch(f'{MODULE}.QFile.readAll')
    def test_read(self, read_all_function: Mock, *_):
        expected = 'This is a sample text'

        read_all_function.return_value.data().decode.return_value = expected
        reader = ResourceFileReader()
        actual = reader._read_from('')

        self.assertEqual(expected, actual)

    @patch(f'{MODULE}.QFile.open', return_value=False)
    def test_read_file_not_found(self, *_):
        with self.assertRaises(FileNotFoundError):
            reader = ResourceFileReader()
            reader._read_from('')
