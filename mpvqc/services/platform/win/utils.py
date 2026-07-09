# SPDX-FileCopyrightText: zhiyiYo
# SPDX-FileCopyrightText: Virace
# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Inspired and based on:
#  - https://github.com/zhiyiYo/PyQt-Frameless-Window
#  - https://gitee.com/Virace/pyside6-qml-frameless-window/tree/main

from ctypes import POINTER, byref, sizeof, windll  # pyrefly: ignore[missing-module-attribute]
from ctypes.wintypes import HWND, LONG, RECT
from functools import lru_cache
from typing import Any

import win32api
import win32con
import win32gui
from PySide6.QtGui import QGuiApplication, QWindow

from .c_structures import APPBARDATA, MARGINS

SM_CXPADDEDBORDER = 92


def get_window_size(hwnd) -> tuple[int, int, int, int]:
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top
    return left, top, width, height


def set_outer_window_size(hwnd, w, h) -> None:
    """Hard-set the OUTER size (frame included)."""
    flags = win32con.SWP_NOMOVE | win32con.SWP_NOZORDER | win32con.SWP_NOACTIVATE
    windll.user32.SetWindowPos(hwnd, None, 0, 0, w, h, flags)


def is_maximized(hwnd) -> bool:
    window_placement = win32gui.GetWindowPlacement(hwnd)
    if not window_placement:
        return False

    return window_placement[1] == win32con.SW_MAXIMIZE


def is_fullscreen(hwnd) -> bool:
    win_rect = win32gui.GetWindowRect(hwnd)
    if not win_rect:
        return False

    monitor_info = get_monitor_info(hwnd, win32con.MONITOR_DEFAULTTOPRIMARY)
    if not monitor_info:
        return False

    monitor_rect = monitor_info["Monitor"]
    return all(i == j for i, j in zip(win_rect, monitor_rect))  # noqa:B905


def get_monitor_info(hwnd, dw_flags) -> Any | None:
    monitor = win32api.MonitorFromWindow(hwnd, dw_flags)
    if not monitor:
        return None

    return win32api.GetMonitorInfo(monitor)


def get_resize_border_thickness(hwnd, horizontal=True) -> int:
    window = find_window(hwnd)
    if not window:
        return 0

    frame = win32con.SM_CXSIZEFRAME if horizontal else win32con.SM_CYSIZEFRAME
    result = get_system_metrics(hwnd, frame) + get_system_metrics(hwnd, SM_CXPADDEDBORDER)

    if result > 0:
        return result

    return round(8 * window.devicePixelRatio())


def get_system_metrics(hwnd, index) -> int:
    dpi = windll.user32.GetDpiForWindow(hwnd)
    return windll.user32.GetSystemMetricsForDpi(index, dpi)


def find_window(hwnd) -> QWindow | None:
    hwnd = int(hwnd)
    for window in QGuiApplication.topLevelWindows():
        if window and window.winId() == hwnd:
            return window
    return None


class Taskbar:
    LEFT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    NO_POSITION = 4

    AUTO_HIDE_THICKNESS = 2

    ABS_AUTOHIDE = 1
    ABM_GETSTATE = 4
    ABM_GETAUTOHIDEBAREX = 11

    @staticmethod
    def is_auto_hide() -> bool:
        appbar_data = APPBARDATA(sizeof(APPBARDATA), 0, 0, 0, RECT(0, 0, 0, 0), 0)
        taskbar_state = windll.shell32.SHAppBarMessage(Taskbar.ABM_GETSTATE, byref(appbar_data))

        return taskbar_state == Taskbar.ABS_AUTOHIDE

    @classmethod
    def get_position(cls, hwnd) -> int:
        monitor_info = get_monitor_info(hwnd, win32con.MONITOR_DEFAULTTONEAREST)
        if not monitor_info:
            return cls.NO_POSITION

        monitor = RECT(*monitor_info["Monitor"])
        appbar_data = APPBARDATA(sizeof(APPBARDATA), 0, 0, 0, monitor, 0)
        positions = [cls.LEFT, cls.TOP, cls.RIGHT, cls.BOTTOM]
        for position in positions:
            appbar_data.uEdge = position
            if windll.shell32.SHAppBarMessage(cls.ABM_GETAUTOHIDEBAREX, byref(appbar_data)):
                return position

        return cls.NO_POSITION


DwmExtendFrameIntoClientArea = windll.dwmapi.DwmExtendFrameIntoClientArea
DwmExtendFrameIntoClientArea.argtypes = [HWND, POINTER(MARGINS)]
DwmExtendFrameIntoClientArea.restype = LONG


def extend_frame_into_client_area(hwnd) -> None:
    """Enables drop shadow if 'configure_gwl_style' gets called as well for the same hwnd"""

    margins = MARGINS(-1, -1, -1, -1)
    DwmExtendFrameIntoClientArea(hwnd, byref(margins))


def configure_gwl_style(hwnd) -> None:
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
    win32gui.SetWindowLong(
        hwnd,
        win32con.GWL_STYLE,
        style
        | win32con.WS_MINIMIZEBOX
        | win32con.WS_MAXIMIZEBOX
        | win32con.WS_SYSMENU
        | win32con.WS_CAPTION
        | win32con.WS_THICKFRAME,
    )


@lru_cache(maxsize=32)
def prevent_window_resize_for(hwnd) -> None:
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
    style &= ~win32con.WS_THICKFRAME
    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)
