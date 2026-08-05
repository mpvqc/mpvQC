# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import IntEnum


class ImportFoundVideo(IntEnum):
    ALWAYS = 0
    ASK_EVERY_TIME = 1
    NEVER = 2
