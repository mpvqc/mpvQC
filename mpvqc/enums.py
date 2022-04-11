#  mpvQC
#
#  Copyright (C) 2022 mpvQC developers
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


from enum import IntEnum


class AccentColor(IntEnum):
    # Found no way to access the QML enum in Python
    RED = 0
    PINK = 1
    PURPLE = 2
    DEEP_PURPLE = 3
    INDIGO = 4
    BLUE = 5
    LIGHT_BLUE = 6
    CYAN = 7
    TEAL = 8
    GREEN = 9
    LIGHT_GREEN = 10
    LIME = 11
    YELLOW = 12
    AMBER = 13
    ORANGE = 14
    DEEP_ORANGE = 15
    BROWN = 16
    GREY = 17
    BLUE_GREY = 18


class Theme(IntEnum):
    LIGHT = 0
    DARK = 1


class TimeFormat(IntEnum):
    EMPTY = 1
    CURRENT_TIME = 2
    REMAINING_TIME = 3
    CURRENT_TOTAL_TIME = 4


class TitleFormat(IntEnum):
    EMPTY = 1
    FILE_NAME = 2
    FILE_PATH = 3
