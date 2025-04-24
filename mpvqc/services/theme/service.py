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

from functools import cache

import inject
from PySide6.QtCore import QDir

from mpvqc.services.resource_reader import ResourceReaderService

from .parser import parse_theme
from .schema import Theme


class ThemeService:
    THEME_FALLBACK = "Material You Dark"

    @staticmethod
    def get_theme_summaries() -> list[dict]:
        return [theme.to_qml_preview() for theme in parse_themes().values()]

    def get_theme_summary(self, theme_identifier: str) -> dict:
        themes = parse_themes()
        theme = themes.get(theme_identifier) or themes[self.THEME_FALLBACK]
        return theme.to_qml_preview()

    def get_theme_colors(self, theme_identifier: str) -> list[dict]:
        themes = parse_themes()
        theme = themes.get(theme_identifier) or themes[self.THEME_FALLBACK]
        theme_colors = theme.colors
        return [colors.to_qml_notation() for colors in theme_colors]

    def get_theme_color(self, color_option: int, theme_identifier: str) -> dict:
        themes = parse_themes()
        theme = themes.get(theme_identifier) or themes[self.THEME_FALLBACK]
        theme_colors = theme.colors
        return theme_colors[min(color_option, len(theme_colors) - 1)].to_qml_notation()


@cache
def parse_themes() -> dict[str, Theme]:
    themes = parse_builtin_themes()

    return {theme.name: theme for theme in themes}


def parse_builtin_themes() -> list[Theme]:
    resource_reader = inject.instance(ResourceReaderService)

    directory = QDir(":/data/themes")
    directory.setNameFilters(["*.toml"])
    directory.setSorting(QDir.SortFlag.Name)

    themes = []

    for entry in directory.entryInfoList():
        resource_path = entry.filePath()
        file_content = resource_reader.read_from(resource_path)
        theme = parse_theme(file_content)
        themes.append(theme)

    return themes
