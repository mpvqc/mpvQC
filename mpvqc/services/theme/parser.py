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


def parse_theme(theme: str) -> Theme:
    try:
        data = tomllib.loads(theme)
    except tomllib.TOMLDecodeError as e:
        raise ThemeParseError(e)

    match data.get("schema-version"):
        case "v1":
            return _parse_v1_theme(data)
        case version:
            raise ThemeParseError(f"Cannot parse schema version {version}")


def _parse_v1_theme(theme: dict) -> Theme:
    match theme.get("theme-name"):
        case None:
            raise ThemeParseError("Cannot parse schema without 'theme-name' property")
        case str(name) if name.strip() == "":
            raise ThemeParseError("Cannot parse schema without 'theme-name' property")
        case str(name):
            theme_name = name.strip()
        case other_value:
            raise ThemeParseError(f"Cannot parse schema theme-name: {other_value}")

    match theme.get("variant"):
        case str(v) if v.strip().lower() == "light":
            variant = "light"
        case str(v) if v.strip().lower() == "dark":
            variant = "dark"
        case other_value:
            raise ThemeParseError(
                f"Cannot parse variant '{other_value}' from theme '{theme_name}'. Allowed values are 'dark' and 'light'"
            )

    def get(prop: str, from_container=None, is_list=False, throw_if_missing=True) -> Any:
        value = (from_container or theme).get(prop)
        if value is None and throw_if_missing:
            raise ThemeParseError(f"Cannot parse property '{prop}' from theme '{theme_name}'")
        if is_list and not isinstance(value, list) and throw_if_missing:
            raise ThemeParseError(f"Cannot parse list property '{prop}' from theme '{theme_name}'")
        return value

    def get_color(prop: str, from_container=None, throw_if_missing=True) -> QColor | None:
        color = get(prop, from_container=from_container, throw_if_missing=throw_if_missing)
        if color is not None:
            return parse_color(f"{color}")

    color_sets = []

    for color_set in get("colors", is_list=True):
        background = get_color("background", from_container=color_set)
        foreground = get_color("foreground", from_container=color_set)

        control = get_color("control", from_container=color_set)
        row_highlight = get_color("row-highlight", from_container=color_set)

        row_highlight_text = get_color("row-highlight-text", from_container=color_set, throw_if_missing=False)
        row_highlight_text = row_highlight_text or foreground

        row_base = get_color("row-base", from_container=color_set, throw_if_missing=False)
        row_base = row_base or background

        row_base_text = get_color("row-base-text", from_container=color_set, throw_if_missing=False)
        row_base_text = row_base_text or foreground

        match get_color("row-base-alternate", from_container=color_set, throw_if_missing=False):
            case None if variant == "light":
                row_base_alternate = parse_color(f"Qt.darker {row_base.name(QColor.NameFormat.HexRgb)} 1.1")
            case None if variant == "dark":
                row_base_alternate = parse_color(f"Qt.lighter {row_base.name(QColor.NameFormat.HexRgb)} 1.3")
            case color_value:
                row_base_alternate = color_value

        row_base_alternate_text = get_color("row-base-alternate-text", from_container=color_set, throw_if_missing=False)
        row_base_alternate_text = row_base_alternate_text or foreground

        color_sets.append(
            ThemeColorSet(
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
        )

    return Theme(name=theme_name, is_dark=variant == "dark", colors=color_sets)
