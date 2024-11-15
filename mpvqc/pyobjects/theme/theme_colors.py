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

from PySide6.QtCore import Property, QObject
from PySide6.QtGui import QColor

from mpvqc.services.theme import Theme

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


class ThemeColors(QObject):
    def __init__(
        self,
        parent,
        name: str,
        is_dark: bool,
        background: QColor,
        foreground: QColor,
        control: QColor,
        row_highlight: QColor,
        row_highlight_text: QColor,
        row_base: QColor,
        row_base_text: QColor,
        row_base_alternate: QColor,
        row_base_alternate_text: QColor,
    ):
        super().__init__(parent)
        self._name = name
        self._is_dark = is_dark
        self._background = background
        self._foreground = foreground

        self._control = control
        self._row_highlight = row_highlight
        self._row_highlight_text = row_highlight_text
        self._row_base = row_base
        self._row_base_text = row_base_text
        self._row_base_alternate = row_base_alternate
        self._row_base_alternate_text = row_base_alternate_text

    @Property(str, constant=True, final=True)
    def name(self) -> str:
        return self._name

    @Property(bool, constant=True, final=True)
    def is_dark(self) -> bool:
        return self._is_dark

    @Property(QColor, constant=True, final=True)
    def background(self) -> QColor:
        return self._background

    @Property(QColor, constant=True, final=True)
    def foreground(self) -> QColor:
        return self._foreground

    @Property(QColor, constant=True, final=True)
    def control(self) -> QColor:
        return self._control

    @Property(QColor, constant=True, final=True)
    def row_highlight(self) -> QColor:
        return self._row_highlight

    @Property(QColor, constant=True, final=True)
    def row_highlight_text(self) -> QColor:
        return self._row_highlight_text

    @Property(QColor, constant=True, final=True)
    def row_base(self) -> QColor:
        return self._row_base

    @Property(QColor, constant=True, final=True)
    def row_base_text(self) -> QColor:
        return self._row_base_text

    @Property(QColor, constant=True, final=True)
    def row_base_alternate(self) -> QColor:
        return self._row_base_alternate

    @Property(QColor, constant=True, final=True)
    def row_base_alternate_text(self) -> QColor:
        return self._row_base_alternate_text


def from_theme(theme: Theme) -> list[ThemeColors]:
    # colors = []
    # for color_set in theme.colors:

    pass
