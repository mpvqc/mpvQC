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


class ThemeService:
    THEME_FALLBACK = "Material You Dark"

    @staticmethod
    def get_theme_summaries() -> list[dict]:
        return [theme.overview() for theme in parse_themes().values()]

    def get_theme_summary(self, theme_identifier: str) -> dict:
        themes = parse_themes()
        theme = themes.get(theme_identifier) or themes[self.THEME_FALLBACK]
        return theme.overview()

    def get_theme_colors(self, theme_identifier: str) -> list[dict]:
        themes = parse_themes()
        theme = themes.get(theme_identifier) or themes[self.THEME_FALLBACK]
        theme_colors = theme.colors
        # noinspection PyTypeChecker
        return [asdict(colors) for colors in theme_colors]

    def get_theme_color(self, color_option: int, theme_identifier: str) -> dict:
        themes = parse_themes()
        theme = themes.get(theme_identifier) or themes[self.THEME_FALLBACK]
        theme_colors = theme.colors
        # noinspection PyTypeChecker
        return asdict(theme_colors[min(color_option, len(theme_colors) - 1)])


@dataclass(frozen=True)
class QmlThemeColors:
    background: str
    foreground: str
    control: str
    rowHighlight: str
    rowHighlightText: str
    rowBase: str
    rowBaseText: str
    rowBaseAlternate: str
    rowBaseAlternateText: str


@dataclass(frozen=True)
class QmlTheme:
    name: str
    isDark: bool
    preview: str
    colors: list[QmlThemeColors]

    def overview(self) -> dict:
        return {
            "name": self.name,
            "isDark": self.isDark,
            "preview": self.preview,
        }


@cache
def parse_themes() -> dict[str, QmlTheme]:
    themes = parse_builtin_themes()

    mapping = {}

    for theme in themes:
        name = theme.name
        is_dark = theme.is_dark
        preview = theme.preview.name(QColor.NameFormat.HexRgb)

        colors = []

        for color in theme.colors:
            option = map_to_qml_color_option(color)
            colors.append(option)

        mapping[name] = QmlTheme(name, is_dark, preview, colors)

    return mapping


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


def map_to_qml_color_option(colors: ThemeColorSet) -> QmlThemeColors:
    return QmlThemeColors(
        background=colors.background.name(QColor.NameFormat.HexRgb),
        foreground=colors.foreground.name(QColor.NameFormat.HexRgb),
        control=colors.control.name(QColor.NameFormat.HexRgb),
        rowHighlight=colors.row_highlight.name(QColor.NameFormat.HexRgb),
        rowHighlightText=colors.row_highlight_text.name(QColor.NameFormat.HexRgb),
        rowBase=colors.row_base.name(QColor.NameFormat.HexRgb),
        rowBaseText=colors.row_base_text.name(QColor.NameFormat.HexRgb),
        rowBaseAlternate=colors.row_base_alternate.name(QColor.NameFormat.HexRgb),
        rowBaseAlternateText=colors.row_base_alternate_text.name(QColor.NameFormat.HexRgb),
    )
