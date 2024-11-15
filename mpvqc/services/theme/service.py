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

from dataclasses import asdict, dataclass
from functools import cache

import inject
from PySide6.QtCore import QDir
from PySide6.QtGui import QColor

from ..resource_reader import ResourceReaderService
from .parser import parse_theme
from .schema import Theme, ThemeColorSet


@dataclass(frozen=True)
class QmlTheme:
    name: str
    isDark: bool
    background: QColor
    foreground: QColor
    control: QColor
    rowHighlight: QColor
    rowHighlightText: QColor
    rowBase: QColor
    rowBaseText: QColor
    rowBaseAlternate: QColor
    rowBaseAlternateText: QColor

    @staticmethod
    def make_from(theme: Theme, color_set: ThemeColorSet) -> "QmlTheme":
        return QmlTheme(
            name=theme.name,
            isDark=theme.is_dark,
            background=theme.background,
            foreground=theme.foreground,
            control=color_set.control,
            rowHighlight=color_set.row_highlight,
            rowHighlightText=color_set.row_highlight_text,
            rowBase=color_set.row_base,
            rowBaseText=color_set.row_base_text,
            rowBaseAlternate=color_set.row_base_alternate,
            rowBaseAlternateText=color_set.row_base_alternate_text,
        )


class ThemeService:
    _resource_reader: ResourceReaderService = inject.attr(ResourceReaderService)

    @cache
    def get_themes(self) -> dict[str, list[QmlTheme]]:
        theme_mapping = {}

        themes = self._parse_builtin_themes()

        for theme in themes:
            for color_set in theme.colors:
                qml_theme = QmlTheme.make_from(theme, color_set)
                # noinspection PyTypeChecker
                qml_theme = asdict(qml_theme)
                theme_mapping.setdefault(theme.name.title(), []).append(qml_theme)

        return theme_mapping

    def _parse_builtin_themes(self) -> list[Theme]:
        themes = []

        directory = QDir(":/data/themes")
        directory.setNameFilters(["*.toml"])
        directory.setSorting(QDir.SortFlag.Name)

        for entry in directory.entryInfoList():
            resource_path = entry.filePath()
            file_content = self._resource_reader.read_from(resource_path)
            theme = parse_theme(file_content)
            themes.append(theme)

        return themes
