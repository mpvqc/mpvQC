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

from dataclasses import dataclass

from PySide6.QtGui import QColor


@dataclass(frozen=True)
class Theme:
    name: str
    is_dark: bool
    background: QColor
    foreground: QColor
    colors: list["ThemeColorSet"]


@dataclass(frozen=True)
class ThemeColorSet:
    control: QColor
    row_highlight: QColor
    row_highlight_text: QColor
    row_base: QColor
    row_base_text: QColor
    row_base_alternate: QColor
    row_base_alternate_text: QColor


class ThemeParseError(Exception):
    pass
