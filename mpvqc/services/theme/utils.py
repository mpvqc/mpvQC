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

import re
from decimal import ROUND_HALF_UP, Decimal

from PySide6.QtGui import QColor

from mpvqc.services.theme.schema import ThemeParseError

WHOLE_NUMBER = Decimal(0)

MULTI_WHITESPACE = re.compile(r"\s+")
HEX_COLOR_RE = re.compile(r"^#(?=(?:.{3}|.{6})$)[a-f0-9]*$")
INT_OR_FLOAT_RE = re.compile(r"^[-+]?\d+(\.\d+)?$")


def parse_color(_color_input: str) -> QColor:
    color_input = MULTI_WHITESPACE.sub(" ", _color_input).strip().lower()

    match color_input.split():
        case [color] if _is_hex(color):
            return QColor(color)
        case ["qt.darker", color, factor] if _is_hex(color) and _is_int_or_float(factor):
            return QColor(color).darker(_adapted_factor(factor))
        case ["qt.lighter", color, factor] if _is_hex(color) and _is_int_or_float(factor):
            return QColor(color).lighter(_adapted_factor(factor))
        case _:
            raise ThemeParseError(f"Cannot parse color: {_color_input}")


def _is_hex(color: str) -> bool:
    return bool(HEX_COLOR_RE.fullmatch(color))


def _is_int_or_float(factor: str) -> bool:
    return bool(INT_OR_FLOAT_RE.fullmatch(factor))


def _adapted_factor(factor: str) -> int:
    f = Decimal(f"{float(factor) * 100}").quantize(WHOLE_NUMBER, ROUND_HALF_UP)
    return int(f)
