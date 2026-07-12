# SPDX-FileCopyrightText: zhiyiYo
# SPDX-FileCopyrightText: Virace
# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Inspired and based on:
#  - https://github.com/zhiyiYo/PyQt-Frameless-Window
#  - https://gitee.com/Virace/pyside6-qml-frameless-window/tree/main

from __future__ import annotations

from typing import override

import PySide6.QtCore

from .native import (
    get_monitor_info_for_rect,
    get_window_rect,
    is_maximized,
    prevent_window_resize_for,
    read_hit_test_point,
    read_nccalcsize_proposed_rect,
    read_window_message,
    write_nccalcsize_client_rect,
)
from .utils import (
    get_resize_border_thickness,
    is_fullscreen,
    overhangs_monitor,
    reserve_auto_hide_taskbar_strip,
)

_WM_STYLECHANGING = 0x007C
_WM_STYLECHANGED = 0x007D
_WM_NCCALCSIZE = 0x0083
_WM_NCHITTEST = 0x0084

_HTTOP = 12
_HTTOPLEFT = 13
_HTTOPRIGHT = 14

_WVR_REDRAW = 0x0300


def handle_non_client_hit_test(hwnd: int, l_param: int) -> tuple[bool, int]:
    # Only the top edge needs help: the client covers the strip where the native
    # caption and its resize band would live. Left, right and bottom keep real
    # non-client bands, hit-tested natively.
    if is_maximized(hwnd) or is_fullscreen(hwnd):
        return False, 0

    rect = get_window_rect(hwnd)
    if rect is None:
        return False, 0

    left, top, right, _ = rect
    cursor_x, cursor_y = read_hit_test_point(l_param)
    x_pos = cursor_x - left
    y_pos = cursor_y - top

    band = get_resize_border_thickness(hwnd, horizontal=False)
    if y_pos >= band:
        return False, 0

    width = right - left
    corner = 2 * band
    if x_pos < corner:
        return True, _HTTOPLEFT
    if x_pos > width - corner:
        return True, _HTTOPRIGHT
    return True, _HTTOP


def handle_non_client_calculate_size(hwnd: int, l_param: int) -> tuple[bool, int]:
    destination = read_nccalcsize_proposed_rect(l_param)

    # Qt's own handling (the DefWindowProc frame plus the negative caption
    # margin) is wrong in only two cases: maximized, where the caption
    # correction overshoots the work area, and fullscreen.
    maximized = is_maximized(hwnd)
    fullscreen = not maximized and overhangs_monitor(destination)
    if not (maximized or fullscreen):
        return False, 0

    destination_monitor = get_monitor_info_for_rect(destination)
    if destination_monitor is None:
        return False, 0

    # A maximized window gets the work area as its client rect. A fullscreen
    # window gets the monitor rect while the window itself is larger on
    # purpose: DWM permanently stops animating maximize/restore once a client
    # rect fills the whole window.
    client_rect = destination_monitor.work_area if maximized else destination_monitor.monitor_rect

    client_rect = reserve_auto_hide_taskbar_strip(client_rect, destination_monitor.monitor_rect)

    write_nccalcsize_client_rect(l_param, client_rect)
    return True, _WVR_REDRAW


class WindowsEventFilter(PySide6.QtCore.QAbstractNativeEventFilter):
    def __init__(self) -> None:
        super().__init__()
        self._top_lvl_hwnd: int | None = None
        self._embedded_player_hwnd: int | None = None

    def set_top_lvl_hwnd(self, hwnd: int) -> None:
        self._top_lvl_hwnd = hwnd

    def set_embedded_player_hwnd(self, hwnd: int) -> None:
        self._embedded_player_hwnd = hwnd

    @override
    def nativeEventFilter(
        self, _: PySide6.QtCore.QByteArray | bytes | bytearray | memoryview, message: int
    ) -> tuple[bool, int]:
        msg = read_window_message(int(message))

        hwnd = msg.hwnd

        match hwnd:
            case None:
                return False, 0
            case self._embedded_player_hwnd:
                return False, 0
            case self._top_lvl_hwnd:
                pass
            case _:
                # Every other window is a windowed popup, and popups must not
                # be resizable. The style is checked on each message on
                # purpose: Windows reuses handle values and Qt can add the
                # frame back at any time.
                #
                # SetWindowLong sends WM_STYLECHANGING/WM_STYLECHANGED back into
                # this filter synchronously. Handling them would call
                # SetWindowLong again, recursing until win32k's nested-message
                # limit.
                if msg.message not in {_WM_STYLECHANGING, _WM_STYLECHANGED}:
                    prevent_window_resize_for(hwnd)
                return False, 0

        if msg.message == _WM_NCHITTEST:
            return handle_non_client_hit_test(hwnd, msg.l_param)
        if msg.message == _WM_NCCALCSIZE and msg.w_param:
            return handle_non_client_calculate_size(hwnd, msg.l_param)
        return False, 0
