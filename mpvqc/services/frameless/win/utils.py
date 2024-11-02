# Copyright 2023
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# Inspired and based on:
#  - https://github.com/zhiyiYo/PyQt-Frameless-Window
#  - https://gitee.com/Virace/pyside6-qml-frameless-window/tree/main

import ctypes
from ctypes import Structure, byref, c_int, sizeof, windll
from ctypes.wintypes import DWORD, HWND, LONG, LPARAM, RECT, UINT

import win32api
import win32con
import win32gui
import win32print
from PySide6.QtCore import QOperatingSystemVersion, QVersionNumber
from PySide6.QtGui import QGuiApplication

from .c_structures import MARGINS


def get_window_size(hwnd) -> tuple[int, int, int, int]:
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top
    return left, top, width, height


def is_maximized(hwnd):
    window_placement = win32gui.GetWindowPlacement(hwnd)
    if not window_placement:
        return False

    return window_placement[1] == win32con.SW_MAXIMIZE


def is_fullscreen(hwnd):
    win_rect = win32gui.GetWindowRect(hwnd)
    if not win_rect:
        return False

    monitor_info = get_monitor_info(hwnd, win32con.MONITOR_DEFAULTTOPRIMARY)
    if not monitor_info:
        return False

    monitor_rect = monitor_info["Monitor"]
    return all(i == j for i, j in zip(win_rect, monitor_rect))


def is_composition_enabled():
    b_result = c_int(0)
    windll.dwmapi.DwmIsCompositionEnabled(byref(b_result))
    return bool(b_result.value)


def get_monitor_info(hwnd, dw_flags):
    monitor = win32api.MonitorFromWindow(hwnd, dw_flags)
    if not monitor:
        return

    return win32api.GetMonitorInfo(monitor)


def get_resize_border_thickness(hwnd, horizontal=True):
    window = find_window(hwnd)
    if not window:
        return 0

    frame = win32con.SM_CXSIZEFRAME if horizontal else win32con.SM_CYSIZEFRAME
    result = get_system_metrics(hwnd, frame, horizontal) + get_system_metrics(hwnd, 92, horizontal)

    if result > 0:
        return result

    thickness = 8 if is_composition_enabled() else 4
    return round(thickness * window.devicePixelRatio())


def get_system_metrics(hwnd, index, horizontal):
    if not hasattr(windll.user32, "GetSystemMetricsForDpi"):
        return win32api.GetSystemMetrics(index)

    dpi = get_dpi_for_window(hwnd, horizontal)
    return windll.user32.GetSystemMetricsForDpi(index, dpi)


def get_dpi_for_window(hwnd, horizontal=True):
    if hasattr(windll.user32, "GetDpiForWindow"):
        return windll.user32.GetDpiForWindow(hwnd)

    hdc = win32gui.GetDC(hwnd)
    if not hdc:
        return 96

    dpi_x = win32print.GetDeviceCaps(hdc, win32con.LOGPIXELSX)
    dpi_y = win32print.GetDeviceCaps(hdc, win32con.LOGPIXELSY)
    win32gui.ReleaseDC(hwnd, hdc)
    if dpi_x > 0 and horizontal:
        return dpi_x
    elif dpi_y > 0 and not horizontal:
        return dpi_y

    return 96


def find_window(hwnd):
    windows = QGuiApplication.topLevelWindows()
    if not windows:
        return

    hwnd = int(hwnd)
    for window in windows:
        if window and int(window.winId()) == hwnd:
            return window


def is_greater_equal_win8_1():
    cv = QOperatingSystemVersion.current()
    cv = QVersionNumber(cv.majorVersion(), cv.minorVersion(), cv.microVersion())
    return cv >= QVersionNumber(8, 1, 0)


class APPBARDATA(Structure):
    _fields_ = [
        ("cbSize", DWORD),
        ("hWnd", HWND),
        ("uCallbackMessage", UINT),
        ("uEdge", UINT),
        ("rc", RECT),
        ("lParam", LPARAM),
    ]


class Taskbar:
    LEFT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    NO_POSITION = 4

    AUTO_HIDE_THICKNESS = 2

    ABS_AUTOHIDE = 1
    ABM_GETSTATE = 4
    ABM_GETTASKBARPOS = 5

    @staticmethod
    def is_auto_hide():
        appbar_data = APPBARDATA(sizeof(APPBARDATA), 0, 0, 0, RECT(0, 0, 0, 0), 0)
        taskbar_state = windll.shell32.SHAppBarMessage(Taskbar.ABM_GETSTATE, byref(appbar_data))

        return taskbar_state == Taskbar.ABS_AUTOHIDE

    @classmethod
    def get_position(cls, hwnd):
        if is_greater_equal_win8_1():
            monitor_info = get_monitor_info(hwnd, win32con.MONITOR_DEFAULTTONEAREST)
            if not monitor_info:
                return cls.NO_POSITION

            monitor = RECT(*monitor_info["Monitor"])
            appbar_data = APPBARDATA(sizeof(APPBARDATA), 0, 0, 0, monitor, 0)
            positions = [cls.LEFT, cls.TOP, cls.RIGHT, cls.BOTTOM]
            for position in positions:
                appbar_data.uEdge = position
                if windll.shell32.SHAppBarMessage(11, byref(appbar_data)):
                    return position

            return cls.NO_POSITION

        appbar_data = APPBARDATA(
            sizeof(APPBARDATA), win32gui.FindWindow("Shell_TrayWnd", None), 0, 0, RECT(0, 0, 0, 0), 0
        )
        if appbar_data.hWnd:
            window_monitor = win32api.MonitorFromWindow(hwnd, win32con.MONITOR_DEFAULTTONEAREST)
            if not window_monitor:
                return cls.NO_POSITION

            taskbar_monitor = win32api.MonitorFromWindow(appbar_data.hWnd, win32con.MONITOR_DEFAULTTOPRIMARY)
            if not taskbar_monitor:
                return cls.NO_POSITION

            if taskbar_monitor == window_monitor:
                windll.shell32.SHAppBarMessage(Taskbar.ABM_GETTASKBARPOS, byref(appbar_data))
                return appbar_data.uEdge

        return cls.NO_POSITION


dwmapi = ctypes.windll.dwmapi

DwmExtendFrameIntoClientArea = dwmapi.DwmExtendFrameIntoClientArea
DwmExtendFrameIntoClientArea.argtypes = [ctypes.wintypes.HWND, ctypes.POINTER(MARGINS)]
DwmExtendFrameIntoClientArea.restype = LONG


def extend_frame_into_client_area(hwnd):
    """Enables drop shadow if 'configure_gwl_style' gets called as well for the same hwnd"""

    margins = MARGINS(-1, -1, -1, -1)
    DwmExtendFrameIntoClientArea(hwnd, ctypes.byref(margins))


def configure_gwl_style(hwnd):
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
    win32gui.SetWindowLong(
        hwnd,
        win32con.GWL_STYLE,
        style
        | win32con.WS_MINIMIZEBOX
        | win32con.WS_MAXIMIZEBOX
        | win32con.WS_SYSMENU
        | win32con.WS_CAPTION
        | win32con.CS_DBLCLKS
        | win32con.WS_THICKFRAME,
    )
