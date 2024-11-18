# mpvQC
#
# Copyright (C) 2024 mpvQC developers
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

import pytest
from PySide6.QtGui import QColor

from mpvqc.services.theme.schema import ThemeParseError
from mpvqc.services.theme.utils import parse_color


@pytest.mark.parametrize(
    "string, expected_hex",
    [
        ("#2e3440", "#2e3440"),
        ("Qt.darker #bf616a 1.3", "#934b52"),
        ("Qt.darker   #bf616a    1.5", "#7f4147"),
        ("qt.Lighter #bf6 1.5", "#f4ffe5"),
        ("qt.lighter #bf616a 1.3", "#f87e8a"),
        ("Qt.lighter #bf616a 1.5", "#ffa1aa"),
    ],
)
def test_parse_color(string: str, expected_hex: str) -> None:
    actual = parse_color(string).name(QColor.NameFormat.HexRgb)
    assert expected_hex == actual


@pytest.mark.parametrize(
    "string",
    [
        "bf616a",
        "Qt.darker bf616a 1.3",
        "Qt.lighter #bf616a",
    ],
)
def test_parse_color_errors(string: str) -> None:
    with pytest.raises(ThemeParseError):
        parse_color(string)
