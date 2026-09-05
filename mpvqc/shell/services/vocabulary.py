# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import IntEnum


class TimeDisplayMode(IntEnum):
    NONE = 0
    CURRENT_TIME = 1
    REMAINING_TIME = 2
    CURRENT_TOTAL_TIME = 3


class WindowTitleFormat(IntEnum):
    DEFAULT = 0
    FILE_NAME = 1
    FILE_PATH = 2
