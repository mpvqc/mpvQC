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
import ctypes.wintypes
from ctypes import cast
from ctypes import wintypes

import PySide6.QtCore
import win32api
import win32con
import win32gui

from . import utils
from .c_structures import LPNCCALCSIZE_PARAMS

# Constants and types
HWND = wintypes.HWND
RECT = wintypes.RECT
HDC = wintypes.HDC
COLORREF = wintypes.COLORREF

# Function prototypes
GetClientRect = ctypes.windll.user32.GetClientRect
FillRect = ctypes.windll.user32.FillRect
CreateSolidBrush = ctypes.windll.gdi32.CreateSolidBrush


def get_message_name(msg):
    # Retrieves the name of the Windows message
    for name, value in vars(win32con).items():
        if name.startswith("WM_") and value == msg:
            return name
    return f"Unknown ({msg})"


class WindowsEventFilter(PySide6.QtCore.QAbstractNativeEventFilter):
    def __init__(self, border_width=None) -> None:
        super().__init__()
        self.border_width = border_width
        self.monitor_info = None

    # https://kubyshkin.name/posts/win32-window-custom-title-bar-caption/
    # https://github.com/grassator/win32-window-custom-titlebar/blob/832ed2d76b50ed33d6cd0f699f095caa8b144343/main.c#L1

    def nativeEventFilter(self, eventType, message):
        msg = ctypes.wintypes.MSG.from_address(message.__int__())

        if not msg.hWnd:
            return False, 0

        hwnd = msg.hWnd
        message = msg.message
        w_param = msg.wParam
        l_param = msg.lParam

        # Handling this event allows us to extend client (paintable) area into the title bar region
        # The information is partially coming from:
        # https://docs.microsoft.com/en-us/windows/win32/dwm/customframe#extending-the-client-frame
        # Most important paragraph is:
        #   To remove the standard window frame, you must handle the WM_NCCALCSIZE message,
        #   specifically when its wParam value is TRUE and the return value is 0.
        #   By doing so, your application uses the entire window region as the client area,
        #   removing the standard frame.
        if message == win32con.WM_NCCALCSIZE:
            if not w_param:
                return win32gui.DefWindowProc(hwnd, message, w_param, l_param)

            dpi = utils.GetDpiForWindow(hwnd)
            frame_x = utils.GetSystemMetricsForDpi(win32con.SM_CXFRAME, dpi)
            frame_y = utils.GetSystemMetricsForDpi(win32con.SM_CYFRAME, dpi)
            padding = utils.GetSystemMetricsForDpi(utils.SM_CXPADDEDBORDER, dpi)

            rect = cast(msg.lParam, LPNCCALCSIZE_PARAMS).contents.rgrc[0]
            rect.right -= frame_x + padding
            rect.left += frame_x + padding
            rect.bottom -= frame_y + padding

            if utils.isMaximized(hwnd):
                rect.top += padding * 2
            return True, 0
        elif message == win32con.WM_CREATE:
            rect = utils.GetWindowRect(hwnd)

            # Inform the application of the frame change to force redrawing with the new
            # client area that is extended into the title bar todo not working currently
            win32gui.SetWindowPos(
                hwnd,
                hwnd,  # Interesting :)
                rect.left,
                rect.top,
                rect.right - rect.left,
                rect.bottom - rect.top,
                win32con.SWP_FRAMECHANGED | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE,
            )
            return True, win32con.WVR_REDRAW
        elif message == win32con.WM_ACTIVATE:
            rect = utils.win32_titlebar_rect(hwnd)
            win32gui.InvalidateRect(hwnd, rect, True)
            return False
        elif message == win32con.WM_NCHITTEST:
            # Let the default procedure handle resizing areas
            hit = win32gui.DefWindowProc(hwnd, message, w_param, l_param)
            if hit in (
                    win32con.HTNOWHERE,
                    win32con.HTRIGHT,
                    win32con.HTLEFT,
                    win32con.HTTOPLEFT,
                    win32con.HTTOP,
                    win32con.HTTOPRIGHT,
                    win32con.HTBOTTOMRIGHT,
                    win32con.HTBOTTOM,
                    win32con.HTBOTTOMLEFT,
            ):
                return True, hit

            # Looks like adjustment happening in NCCALCSIZE is messing with the detection
            # of the top hit area so manually fixing that.
            rect = utils.GetWindowRect(hwnd)
            x = (win32api.LOWORD(l_param) - rect.left) % 65536
            y = (win32api.HIWORD(l_param) - rect.top) % 65536

            win32gui.ScreenToClient(hwnd, (x, y))

            dpi = utils.GetDpiForWindow(hwnd)
            frame_y = utils.GetSystemMetricsForDpi(win32con.SM_CYFRAME, dpi)
            padding = utils.GetSystemMetricsForDpi(utils.SM_CXPADDEDBORDER, dpi)

            if 0 < y < frame_y + padding:
                return True, win32con.HTTOP

            return True, win32con.HTCLIENT
        elif message == win32con.WM_ERASEBKGND:
            rect = RECT()
            GetClientRect(hwnd, ctypes.byref(rect))

            hdc = ctypes.windll.user32.GetDC(hwnd)
            brush = CreateSolidBrush(0x00000000)

            FillRect(hdc, ctypes.byref(rect), brush)

            ctypes.windll.user32.ReleaseDC(hwnd, hdc)
            ctypes.windll.gdi32.DeleteObject(brush)
            return True, 0

        return False, 0
