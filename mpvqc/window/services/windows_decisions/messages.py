# SPDX-FileCopyrightText: zhiyiYo
# SPDX-FileCopyrightText: Virace
# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Inspired and based on:
#  - https://github.com/zhiyiYo/PyQt-Frameless-Window
#  - https://gitee.com/Virace/pyside6-qml-frameless-window/tree/main

from __future__ import annotations


def read_hit_test_point(l_param: int) -> tuple[int, int]:
    """The WM_NCHITTEST cursor position: two signed 16-bit screen coordinates.
    Signed because a monitor left of or above the primary one has negative
    coordinates."""
    return _signed_16(l_param & 0xFFFF), _signed_16((l_param >> 16) & 0xFFFF)


def _signed_16(value: int) -> int:
    return value - 0x10000 if value & 0x8000 else value
