#  mpvQC
#
#  Copyright (C) 2022 mpvQC developers
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


from unittest.mock import patch

import pytest

from mpvqc.impl import ResourceFileReader


@pytest.mark.parametrize("file_path", [
    ":/data/icon.svg",
    "/data/icon.svg",
    "data/icon.svg",
])
def test_read_from(file_path):
    reader = ResourceFileReader()
    content = reader.read_from(file_path)
    assert content.startswith('<svg ')


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        reader = ResourceFileReader()
        reader.read_from('>>')


@patch('mpvqc.impl.file_reader_resources.QFile.exists', return_value=True)
@patch('mpvqc.impl.file_reader_resources.QFile.open', return_value=False)
def test_some_other_method(*_):
    with pytest.raises(Exception):
        reader = ResourceFileReader()
        reader.read_from('')
