# SPDX-FileCopyrightText: zhiyiYo
# SPDX-FileCopyrightText: Virace
# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Inspired and based on:
#  - https://github.com/zhiyiYo/PyQt-Frameless-Window
#  - https://gitee.com/Virace/pyside6-qml-frameless-window/tree/main

from __future__ import annotations

import ctypes.wintypes
from ctypes import cast
from typing import override

import PySide6.QtCore
import win32api
import win32con

from .c_structures import LPNCCALCSIZE_PARAMS
from .utils import (
    Taskbar,
    covers_monitor,
    get_monitor_info,
    get_monitor_rect_for,
    get_resize_border_thickness,
    get_window_size,
    is_fullscreen,
    is_maximized,
    prevent_window_resize_for,
)


def handle_non_client_hit_test(hwnd: int, l_param: int) -> tuple[bool, int]:
    # Only the top edge needs help: the client covers the strip where the native
    # caption and its resize band would live. Left, right and bottom keep real
    # non-client bands, hit-tested natively.
    if is_maximized(hwnd) or is_fullscreen(hwnd):
        return False, 0

    x, y, w, _ = get_window_size(hwnd)
    x_pos = (win32api.LOWORD(l_param) - x) % 65536
    y_pos = (win32api.HIWORD(l_param) - y) % 65536

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
    rect = cast(l_param, LPNCCALCSIZE_PARAMS).contents.rgrc[0]
    proposed = (rect.left, rect.top, rect.right, rect.bottom)

    # Qt's own handling (DefWindowProc frame plus the negative caption margin) is
    # only wrong when maximized, where the caption correction overshoots the work
    # area, and when fullscreen.
    if is_maximized(hwnd):
        monitor_info = get_monitor_info(hwnd, win32con.MONITOR_DEFAULTTONEAREST)
        if monitor_info is None:
            return False, 0
        rect.left, rect.top, rect.right, rect.bottom = monitor_info["Work"]
    elif covers_monitor(proposed):
        # The fullscreen window is deliberately larger than the monitor: DWM
        # permanently drops maximize/restore animations once a client rect fills
        # the whole window.
        monitor_rect = get_monitor_rect_for(proposed)
        if monitor_rect is None:
            return False, 0
        rect.left, rect.top, rect.right, rect.bottom = monitor_rect
    else:
        return False, 0

    if Taskbar.is_auto_hide():
        position = Taskbar.get_position(hwnd)
        if position == Taskbar.TOP:
            rect.top += Taskbar.AUTO_HIDE_THICKNESS
        elif position == Taskbar.BOTTOM:
            rect.bottom -= Taskbar.AUTO_HIDE_THICKNESS
        elif position == Taskbar.LEFT:
            rect.left += Taskbar.AUTO_HIDE_THICKNESS
        elif position == Taskbar.RIGHT:
            rect.right -= Taskbar.AUTO_HIDE_THICKNESS

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
        msg = ctypes.wintypes.MSG.from_address(int(message))

        hwnd = msg.hWnd

        match hwnd:
            case None:
                return False, 0
            case self._embedded_player_hwnd:
                return False, 0
            case self._top_lvl_hwnd:
                pass
            case _:
                prevent_window_resize_for(hwnd)
                return False, 0

        match msg.message:
            case win32con.WM_NCHITTEST:
                return handle_non_client_hit_test(hwnd, msg.lParam)
            case win32con.WM_NCCALCSIZE if msg.wParam:
                return handle_non_client_calculate_size(hwnd, msg.lParam)
            case _:
                return False, 0
