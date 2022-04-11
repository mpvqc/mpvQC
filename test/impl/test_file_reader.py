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

from mpvqc.impl.file_reader import FileReader


class TestFileReader(unittest.TestCase):
    MODULE = 'mpvqc.impl.file_reader'

    @patch(f'{MODULE}.Path.read_text')
    def test_read(self, mocked_func: Mock):
        reader = FileReader()
        reader.read(Path())
        mocked_func.assert_called()
