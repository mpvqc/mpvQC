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

import tomllib
from typing import Any

from PySide6.QtGui import QColor

from mpvqc.services.theme.schema import Theme, ThemeColorSet, ThemeParseError
from mpvqc.services.theme.utils import parse_color


class V1ThemeParser:
    def __init__(self, theme_data: dict):
        self.theme_data = theme_data
        self.theme_name = _parse_theme_name(theme_data)
        self.is_dark = _parse_theme_variant(theme_data, self.theme_name)

    def parse(self) -> Theme:
        preview_color = self._get_color("theme-preview", throw_if_missing=False)
        color_sets = self._parse_color_sets()
        return Theme(name=self.theme_name, is_dark=self.is_dark, preview=preview_color, colors=color_sets)

    def _get_color(self, prop: str, container=None, throw_if_missing=True) -> QColor | None:
        color = self._get_property(prop, container, throw_if_missing=throw_if_missing)
        if color is not None:
            return parse_color(f"{color}")
        return None

    def _get_property(self, prop: str, container=None, is_list=False, throw_if_missing=True) -> Any:
        value = (container or self.theme_data).get(prop)
        if value is None and throw_if_missing:
            msg = f"Property '{prop}' not found"
            raise self._error(msg)
        if is_list and not isinstance(value, list) and throw_if_missing:
            msg = f"Property '{prop}' required to be a list"
            raise self._error(msg)
        return value

    def _error(self, message: str) -> ThemeParseError:
        return ThemeParseError(f"Cannot parse schema '{self.theme_name}'. {message}")

    def _parse_color_sets(self) -> list[ThemeColorSet]:
        return [self._parse_color_set(color_set) for color_set in self._get_property("colors", is_list=True)]

    def _parse_color_set(self, color_set: dict) -> ThemeColorSet:
        background = self._get_color("background", color_set)
        foreground = self._get_color("foreground", color_set)
        control = self._get_color("control", color_set)
        row_highlight = self._get_color("row-highlight", color_set)

        row_highlight_text = self._get_color("row-highlight-text", color_set, throw_if_missing=False)
        row_highlight_text = row_highlight_text or foreground

        row_base = self._get_color("row-base", color_set, throw_if_missing=False)
        row_base = row_base or background

        row_base_text = self._get_color("row-base-text", color_set, throw_if_missing=False)
        row_base_text = row_base_text or foreground

        match self._get_color("row-base-alternate", color_set, throw_if_missing=False):
            case None if self.is_dark:
                row_base_alternate = parse_color(f"Qt.lighter {row_base.name(QColor.NameFormat.HexRgb)} 1.3")
            case None if not self.is_dark:
                row_base_alternate = parse_color(f"Qt.darker {row_base.name(QColor.NameFormat.HexRgb)} 1.1")
            case color_value:
                row_base_alternate = color_value

        row_base_alternate_text = self._get_color("row-base-alternate-text", color_set, throw_if_missing=False)
        row_base_alternate_text = row_base_alternate_text or foreground

        return ThemeColorSet(
            background=background,
            foreground=foreground,
            control=control,
            row_highlight=row_highlight,
            row_highlight_text=row_highlight_text,
            row_base=row_base,
            row_base_text=row_base_text,
            row_base_alternate=row_base_alternate,
            row_base_alternate_text=row_base_alternate_text,
        )


def parse_theme(theme: str) -> Theme:
    try:
        data = tomllib.loads(theme)
    except tomllib.TOMLDecodeError as e:
        raise ThemeParseError(e)

    match data.get("schema-version"):
        case "v1":
            return V1ThemeParser(data).parse()
        case version:
            msg = f"Cannot parse schema version {version}"
            raise ThemeParseError(msg)


def _parse_theme_name(theme_data: dict) -> str:
    match theme_data.get("theme-name"):
        case None:
            msg = "Cannot parse schema without 'theme-name' property"
            raise ThemeParseError(msg)
        case str(name) if name.strip() == "":
            msg = "Cannot parse schema without 'theme-name' property"
            raise ThemeParseError(msg)
        case str(name):
            return name.strip()
        case other_value:
            msg = f"Cannot parse schema theme-name: {other_value}"
            raise ThemeParseError(msg)


def _parse_theme_variant(theme_data: dict, theme_name: str) -> bool:
    match theme_data.get("theme-variant"):
        case str(v) if v.strip().lower() == "light":
            return False
        case str(v) if v.strip().lower() == "dark":
            return True
        case other_value:
            msg = (
                f"Cannot parse schema '{theme_name}'. "
                f'Property theme-variant = "{other_value}" not supported. Allowed values: dark, light'
            )
            raise ThemeParseError(msg)
