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
from ctypes import cast

import PySide6.QtCore
import win32api
import win32con
import win32gui

from .c_structures import LPNCCALCSIZE_PARAMS
from .utils import isMaximized, isFullScreen, getResizeBorderThickness, Taskbar, erase_background


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
            y_pos = (win32api.HIWORD(msg.lParam) - y) % 65536

            bw = 0 if isMaximized(msg.hWnd) or isFullScreen(msg.hWnd) else self.border_width
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
        elif msg.message == win32con.WM_NCCALCSIZE and msg.wParam:
            rect = cast(msg.lParam, LPNCCALCSIZE_PARAMS).contents.rgrc[0]

            isMax = isMaximized(msg.hWnd)
            isFull = isFullScreen(msg.hWnd)

            # adjust the size of client rect
            if isMax and not isFull:
                ty = getResizeBorderThickness(msg.hWnd, False)
                rect.top += ty
                rect.bottom -= ty

                tx = getResizeBorderThickness(msg.hWnd, True)
                rect.left += tx
                rect.right -= tx

            # handle the situation that an auto-hide taskbar is enabled
            if (isMax or isFull) and Taskbar.isAutoHide():
                position = Taskbar.getPosition(msg.hWnd)
                if position == Taskbar.LEFT:
                    rect.top += Taskbar.AUTO_HIDE_THICKNESS
                elif position == Taskbar.BOTTOM:
                    rect.bottom -= Taskbar.AUTO_HIDE_THICKNESS
                elif position == Taskbar.LEFT:
                    rect.left += Taskbar.AUTO_HIDE_THICKNESS
                elif position == Taskbar.RIGHT:
                    rect.right -= Taskbar.AUTO_HIDE_THICKNESS

            result = 0 if not msg.wParam else win32con.WVR_REDRAW
            return True, result
        elif msg.message == win32con.WM_ERASEBKGND:
            erase_background(msg.hWnd)
            return True, 0

        return False, 0

    @classmethod
    def get_window_size(cls, hwnd):
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top
        return left, top, width, height
