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
import win32con

from .native import (
    get_monitor_info_for_rect,
    is_maximized,
    prevent_window_resize_for,
    read_hit_test_point,
    read_nccalcsize_proposed_rect,
    read_window_message,
    write_nccalcsize_client_rect,
)
from .utils import (
    get_resize_border_thickness,
    get_window_size,
    is_fullscreen,
    overhangs_monitor,
    reserve_auto_hide_taskbar_strip,
)


def handle_non_client_hit_test(hwnd: int, l_param: int) -> tuple[bool, int]:
    # Only the top edge needs help: the client covers the strip where the native
    # caption and its resize band would live. Left, right and bottom keep real
    # non-client bands, hit-tested natively.
    if is_maximized(hwnd) or is_fullscreen(hwnd):
        return False, 0

    x, y, w, _ = get_window_size(hwnd)
    cursor_x, cursor_y = read_hit_test_point(l_param)
    x_pos = cursor_x - x
    y_pos = cursor_y - y

    band = get_resize_border_thickness(hwnd, horizontal=False)
    if y_pos >= band:
        return False, 0

    corner = 2 * band
    if x_pos < corner:
        return True, win32con.HTTOPLEFT
    if x_pos > w - corner:
        return True, win32con.HTTOPRIGHT
    return True, win32con.HTTOP


def handle_non_client_calculate_size(hwnd: int, l_param: int) -> tuple[bool, int]:
    destination = read_nccalcsize_proposed_rect(l_param)

    # Qt's own handling (DefWindowProc frame plus the negative caption margin) is
    # only wrong when maximized, where the caption correction overshoots the work
    # area, and when fullscreen.
    maximized = is_maximized(hwnd)
    fullscreen = not maximized and overhangs_monitor(destination)
    if not (maximized or fullscreen):
        return False, 0

    destination_monitor = get_monitor_info_for_rect(destination)
    if destination_monitor is None:
        return False, 0

    # Maximized gets the work area. Fullscreen gets the monitor rect, and its
    # window is deliberately larger: DWM permanently drops maximize/restore
    # animations once a client rect fills the whole window.
    client_rect = destination_monitor.work_area if maximized else destination_monitor.monitor_rect

    client_rect = reserve_auto_hide_taskbar_strip(client_rect, destination_monitor.monitor_rect)

    write_nccalcsize_client_rect(l_param, client_rect)
    return True, win32con.WVR_REDRAW


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
                # SetWindowLong pumps WM_STYLECHANGING/WM_STYLECHANGED back
                # through this filter synchronously; acting on them would
                # re-enter the style write until win32k's nested-send cap.
                if msg.message not in {win32con.WM_STYLECHANGING, win32con.WM_STYLECHANGED}:
                    prevent_window_resize_for(hwnd)
                return False, 0

        match msg.message:
            case win32con.WM_NCHITTEST:
                return handle_non_client_hit_test(hwnd, msg.l_param)
            case win32con.WM_NCCALCSIZE if msg.w_param:
                return handle_non_client_calculate_size(hwnd, msg.l_param)
            case _:
                return False, 0
