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

from ctypes import POINTER, byref, c_int, WinDLL, windll
from ctypes.wintypes import LONG

import win32con
import win32gui

from .c_structures import MARGINS


class WindowsWindowEffect:
    """"""

    def __init__(self):
        self.user32 = WinDLL("user32")
        self.dwmapi = WinDLL("dwmapi")

        self.DwmExtendFrameIntoClientArea = self.dwmapi.DwmExtendFrameIntoClientArea
        self.DwmExtendFrameIntoClientArea.restype = LONG
        self.DwmExtendFrameIntoClientArea.argtypes = [c_int, POINTER(MARGINS)]

    def addShadowEffect(self, hWnd):
        if not self._isDwmCompositionEnabled():
            return
        hWnd = int(hWnd)
        margins = MARGINS(-1, -1, -1, -1)
        self.DwmExtendFrameIntoClientArea(hWnd, byref(margins))

    @staticmethod
    def _isDwmCompositionEnabled():
        bResult = c_int(0)
        windll.dwmapi.DwmIsCompositionEnabled(byref(bResult))
        return bool(bResult.value)

    @staticmethod
    def addWindowAnimation(hWnd):
        hWnd = int(hWnd)
        style = win32gui.GetWindowLong(hWnd, win32con.GWL_STYLE)
        win32gui.SetWindowLong(
            hWnd,
            win32con.GWL_STYLE,
            style
            | win32con.WS_MINIMIZEBOX
            | win32con.WS_MAXIMIZEBOX
            | win32con.WS_SYSMENU
            | win32con.WS_CAPTION
            | win32con.CS_DBLCLKS
            | win32con.WS_THICKFRAME,
        )
