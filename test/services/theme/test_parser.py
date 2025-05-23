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

from mpvqc.services.theme.parser import parse_theme
from mpvqc.services.theme.schema import ThemeParseError
from mpvqc.services.theme.utils import parse_color


def assert_colors(*colors):
    colors = {QColor(c).name(QColor.NameFormat.HexRgb) for c in colors}
    assert len(colors) == 1


VALID_THEME_V1 = """
schema-version = "v1"

theme-name = "Nord Dark"
theme-variant = "Dark"
theme-preview = "#2e3440"

[[colors]]
background = "#2e3440"
foreground = "#d8dee9"
control = "#bf616a"
row-highlight = "#934b52"

[[colors]]
background = "#2e3440"
foreground = "#d8dee9"
control = "#d08770"
row-highlight = "#a06856"
"""


def test_parse_valid_v1():
    theme = parse_theme(VALID_THEME_V1)
    print(theme)


VALID_THEME_V1_BASE = """
schema-version = "v1"

theme-name = "Nord Dark"
theme-variant = "dark"
theme-preview = "#2e3440"

[[colors]]
background = "#2e3440"
foreground = "#d8dee9"
control = "#bf616a"
row-highlight = "#934b52"
"""


def _replace(old: str, new: str) -> str:
    return VALID_THEME_V1_BASE.replace(f"""{old}""", f"""{new}""")


def _append(line: str) -> str:
    return VALID_THEME_V1_BASE + f"\n{line}\n"


@pytest.mark.parametrize(
    ("old", "new"),
    [
        ('schema-version = "v1"', 'schema-version = "v0"'),
        ('theme-name = "Nord Dark"', 'theme-name = ""'),
        ('theme-name = "Nord Dark"', "theme-name = 1"),
        ("theme-name =", "names ="),
        ('theme-variant = "dark"', 'theme-variant = "dark lord"'),
        ('theme-preview = "#2e3440"', 'theme-preview = "2e3440"'),
        ('background = "#2e3440"', 'background = ""'),
        ('foreground = "#d8dee9"', 'foreground = "#d8dee"'),
        ("[[colors]]", 'colors = "not-list"'),
        ("[[colors]]", "[[colors]"),
        ('control = "#bf616a"', 'controls = "#bf616a"'),
        ('row-highlight = "#934b52"', ""),
    ],
)
def test_parse_errors(old, new):
    twisted_theme = _replace(old, new)
    with pytest.raises(ThemeParseError):
        parse_theme(twisted_theme)


def test_row_highlight_text():
    theme = parse_theme(VALID_THEME_V1_BASE)
    assert theme.colors[0].row_highlight_text == "#d8dee9"

    theme = parse_theme(_append('row-highlight-text = "#ff0000"'))
    assert theme.colors[0].row_highlight_text == "#ff0000"


def test_row_base():
    theme = parse_theme(VALID_THEME_V1_BASE)
    assert theme.colors[0].row_base == "#2e3440"

    theme = parse_theme(_append('row-base = "#ff0000"'))
    assert theme.colors[0].row_base == "#ff0000"


def test_row_base_text():
    theme = parse_theme(VALID_THEME_V1_BASE)
    assert theme.colors[0].row_base_text == "#d8dee9"

    theme = parse_theme(_append('row-base-text = "#ff0000"'))
    assert theme.colors[0].row_base_text == "#ff0000"


def test_row_base_alternate():
    theme = parse_theme(VALID_THEME_V1_BASE)
    assert_colors(
        theme.colors[0].row_base_alternate,
        QColor("#3c4453"),
        parse_color(f"Qt.lighter {theme.colors[0].row_base.name(QColor.NameFormat.HexRgb)} 1.3"),
    )

    theme = parse_theme(_replace('theme-variant = "dark"', 'theme-variant = "light"'))
    assert_colors(
        theme.colors[0].row_base_alternate,
        QColor("#2a2f3a"),
        parse_color(f"Qt.darker {theme.colors[0].row_base.name(QColor.NameFormat.HexRgb)} 1.1"),
    )

    theme = parse_theme(_append('row-base-alternate = "#ff0000"'))
    assert theme.colors[0].row_base_alternate == "#ff0000"


def test_row_base_alternate_text():
    theme = parse_theme(VALID_THEME_V1_BASE)
    assert theme.colors[0].row_base_alternate_text == "#d8dee9"

    theme = parse_theme(_append('row-base-alternate-text = "#ff0000"'))
    assert theme.colors[0].row_base_alternate_text == "#ff0000"
