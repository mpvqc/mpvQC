# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys

from mpvqc.resources import read_resource


def read_input_conf() -> str:
    return read_resource(":/data/config/input.conf")


def read_mpv_conf() -> str:
    if sys.platform == "win32":
        return read_resource(":/data/config/mpv-windows.conf")
    return read_resource(":/data/config/mpv-linux.conf")
