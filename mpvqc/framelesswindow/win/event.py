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

import ctypes.wintypes
from ctypes import c_void_p

import PySide6.QtCore
import win32api
import win32con
import win32gui


class WindowsEventFilter(PySide6.QtCore.QAbstractNativeEventFilter):
    def __init__(self, border_width=None) -> None:
        super().__init__()
        self.border_width = border_width
        self.monitor_info = None

    def nativeEventFilter(self, eventType, message):
        msg = ctypes.wintypes.MSG.from_address(message.__int__())

        if not msg.hWnd:
            return False, 0

        if msg.message == win32con.WM_NCHITTEST and (self.border_width is not None):
            x, y, w, h = self.get_window_size(msg.hWnd)
            x_pos = (win32api.LOWORD(msg.lParam) - x) % 65536
            y_pos = win32api.HIWORD(msg.lParam) - y

            bw = 0 if self.isWindowMaximized(msg.hWnd) or self.isFullScreen(msg.hWnd) else self.border_width
            lx = x_pos < bw
            rx = x_pos > w - bw
            ty = y_pos < bw
            by = y_pos > h - bw

            if lx and ty:
                return True, win32con.HTTOPLEFT
            elif rx and by:
                return True, win32con.HTBOTTOMRIGHT
            elif rx and ty:
                return True, win32con.HTTOPRIGHT
            elif lx and by:
                return True, win32con.HTBOTTOMLEFT
            elif ty:
                return True, win32con.HTTOP
            elif by:
                return True, win32con.HTBOTTOM
            elif lx:
                return True, win32con.HTLEFT
            elif rx:
                return True, win32con.HTRIGHT
        elif msg.message == win32con.WM_NCCALCSIZE:
            result = 0 if not msg.wParam else win32con.WVR_REDRAW
            return True, result
        elif msg.message == win32con.WM_GETMINMAXINFO:
            if self.isWindowMaximized(msg.hWnd):
                return True, 1
        return False, 0

    @classmethod
    def get_window_size(cls, hwnd):
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top
        return left, top, width, height

    @classmethod
    def isWindowMaximized(cls, hwnd: int or c_void_p) -> bool:
        windowPlacement = win32gui.GetWindowPlacement(hwnd)
        if not windowPlacement:
            return False
        return windowPlacement[1] == win32con.SW_MAXIMIZE

    def isFullScreen(self, hwnd: int or c_void_p):
        if not hwnd:
            return False

        hwnd = int(hwnd)
        winRect = win32gui.GetWindowRect(hwnd)
        if not winRect:
            return False

        monitorInfo = self.getMonitorInfo(hwnd, win32con.MONITOR_DEFAULTTOPRIMARY)
        if not monitorInfo:
            return False

        monitorRect = monitorInfo["Monitor"]
        return all(i == j for i, j in zip(winRect, monitorRect))

    def getMonitorInfo(self, hwnd: int or c_void_p, dwFlags: int):
        monitor = win32api.MonitorFromWindow(hwnd, dwFlags)
        if not monitor:
            return

        return win32api.GetMonitorInfo(monitor)
