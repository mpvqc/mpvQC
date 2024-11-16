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
    @staticmethod
    def get_theme_summaries() -> list[dict]:
        summaries, _ = parse_themes()
        return summaries

    @staticmethod
    def get_options_for_theme(name: str) -> list[dict]:
        _, color_options = parse_themes()
        return color_options.get(name, [])


@dataclass(frozen=True)
class QmlThemeSummary:
    name: str
    isDark: bool
    preview: QColor


@dataclass(frozen=True)
class QmlThemeColors:
    background: QColor
    foreground: QColor
    control: QColor
    rowHighlight: QColor
    rowHighlightText: QColor
    rowBase: QColor
    rowBaseText: QColor
    rowBaseAlternate: QColor
    rowBaseAlternateText: QColor


@cache
def parse_themes() -> tuple[list[dict], dict[str, list[dict]]]:
    summaries: list[dict] = []
    color_options: dict[str, list[dict]] = {}

    themes = parse_builtin_themes()

    for theme in themes:
        summary = map_to_summary(theme)
        # noinspection PyTypeChecker
        summaries.append(asdict(summary))

        for color_set in theme.colors:
            color_option = map_to_qml_color_set(color_set)
            # noinspection PyTypeChecker
            color_options.setdefault(theme.name, []).append(asdict(color_option))

    return summaries, color_options


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


def map_to_summary(theme: Theme) -> QmlThemeSummary:
    return QmlThemeSummary(
        name=theme.name,
        isDark=theme.is_dark,
        preview=theme.preview,
    )


def map_to_qml_color_set(colors: ThemeColorSet) -> QmlThemeColors:
    return QmlThemeColors(
        background=colors.background,
        foreground=colors.foreground,
        control=colors.control,
        rowHighlight=colors.row_highlight,
        rowHighlightText=colors.row_highlight_text,
        rowBase=colors.row_base,
        rowBaseText=colors.row_base_text,
        rowBaseAlternate=colors.row_base_alternate,
        rowBaseAlternateText=colors.row_base_alternate_text,
    )
