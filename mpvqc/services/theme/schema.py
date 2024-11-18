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
class ThemeColorSet:
    background: QColor
    foreground: QColor
    control: QColor
    row_highlight: QColor
    row_highlight_text: QColor
    row_base: QColor
    row_base_text: QColor
    row_base_alternate: QColor
    row_base_alternate_text: QColor

    def to_qml_notation(self) -> dict[str, str]:
        return {
            "background": self.background.name(QColor.NameFormat.HexRgb),
            "foreground": self.foreground.name(QColor.NameFormat.HexRgb),
            "control": self.control.name(QColor.NameFormat.HexRgb),
            "rowHighlight": self.row_highlight.name(QColor.NameFormat.HexRgb),
            "rowHighlightText": self.row_highlight_text.name(QColor.NameFormat.HexRgb),
            "rowBase": self.row_base.name(QColor.NameFormat.HexRgb),
            "rowBaseText": self.row_base_text.name(QColor.NameFormat.HexRgb),
            "rowBaseAlternate": self.row_base_alternate.name(QColor.NameFormat.HexRgb),
            "rowBaseAlternateText": self.row_base_alternate_text.name(QColor.NameFormat.HexRgb),
        }


@dataclass(frozen=True)
class Theme:
    name: str
    is_dark: bool
    preview: QColor
    colors: list["ThemeColorSet"]

    def to_qml_preview(self) -> dict:
        return {
            "name": self.name,
            "isDark": self.is_dark,
            "preview": self.preview,
        }


class ThemeParseError(Exception):
    pass
