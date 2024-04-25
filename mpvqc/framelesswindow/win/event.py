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

from .c_structures import LPNCCALCSIZE_PARAMS
from .utils import is_maximized, is_fullscreen, get_resize_border_thickness, Taskbar, get_window_size

RESIZE_BORDER_WIDTH = 6


def handle_non_client_hit_test(hwnd, l_param) -> tuple[bool, int]:
    if is_maximized(hwnd) or is_fullscreen(hwnd):
        return False, win32con.HTNOWHERE

    x, y, w, h = get_window_size(hwnd)
    x_pos = (win32api.LOWORD(l_param) - x) % 65536
    y_pos = (win32api.HIWORD(l_param) - y) % 65536

    lx = x_pos < RESIZE_BORDER_WIDTH
    rx = x_pos > w - RESIZE_BORDER_WIDTH
    ty = y_pos < RESIZE_BORDER_WIDTH
    by = y_pos > h - RESIZE_BORDER_WIDTH

    if lx and ty:
        return True, win32con.HTTOPLEFT
    if rx and by:
        return True, win32con.HTBOTTOMRIGHT
    if rx and ty:
        return True, win32con.HTTOPRIGHT
    if lx and by:
        return True, win32con.HTBOTTOMLEFT
    if ty:
        return True, win32con.HTTOP
    if by:
        return True, win32con.HTBOTTOM
    if lx:
        return True, win32con.HTLEFT
    if rx:
        return True, win32con.HTRIGHT

    return False, win32con.HTNOWHERE


def handle_non_client_calculate_size(hwnd, l_param) -> tuple[bool, int]:
    rect = cast(l_param, LPNCCALCSIZE_PARAMS).contents.rgrc[0]

    maximized = is_maximized(hwnd)
    fullscreen = is_fullscreen(hwnd)

    # adjust the size of client rect
    if maximized and not fullscreen:
        ty = get_resize_border_thickness(hwnd, False)
        rect.top += ty
        rect.bottom -= ty

        tx = get_resize_border_thickness(hwnd, True)
        rect.left += tx
        rect.right -= tx

    if (maximized or fullscreen) and Taskbar.is_auto_hide():
        position = Taskbar.get_position(hwnd)
        if position == Taskbar.LEFT:
            rect.top += Taskbar.AUTO_HIDE_THICKNESS
        elif position == Taskbar.BOTTOM:
            rect.bottom -= Taskbar.AUTO_HIDE_THICKNESS
        elif position == Taskbar.LEFT:
            rect.left += Taskbar.AUTO_HIDE_THICKNESS
        elif position == Taskbar.RIGHT:
            rect.right -= Taskbar.AUTO_HIDE_THICKNESS

    return True, win32con.WVR_REDRAW


GetClientRect = ctypes.windll.user32.GetClientRect
GetDC = ctypes.windll.user32.GetDC
CreateSolidBrush = ctypes.windll.gdi32.CreateSolidBrush
FillRect = ctypes.windll.user32.FillRect
ReleaseDC = ctypes.windll.user32.ReleaseDC
DeleteObject = ctypes.windll.gdi32.DeleteObject


def handle_erase_background(hwnd) -> tuple[bool, int]:
    rect = ctypes.wintypes.RECT()
    GetClientRect(hwnd, ctypes.byref(rect))

    hdc = GetDC(hwnd)
    brush = CreateSolidBrush(0x00000000)

    FillRect(hdc, ctypes.byref(rect), brush)

    ReleaseDC(hwnd, hdc)
    DeleteObject(brush)
    return True, 0


class WindowsEventFilter(PySide6.QtCore.QAbstractNativeEventFilter):
    """"""

    def nativeEventFilter(self, _, message):
        msg = ctypes.wintypes.MSG.from_address(message.__int__())

        hwnd = msg.hWnd

        if not hwnd:
            return False, 0

        l_param = msg.lParam
        w_param = msg.wParam
        message = msg.message

        match message:
            case win32con.WM_NCHITTEST:
                return handle_non_client_hit_test(hwnd, l_param)
            case win32con.WM_NCCALCSIZE if w_param:
                return handle_non_client_calculate_size(hwnd, l_param)
            case win32con.WM_ERASEBKGND:
                return handle_erase_background(hwnd)
            case _:
                return False, 0
