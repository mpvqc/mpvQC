# SPDX-FileCopyrightText: zhiyiYo
# SPDX-FileCopyrightText: Virace
# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Inspired and based on:
#  - https://github.com/zhiyiYo/PyQt-Frameless-Window
#  - https://gitee.com/Virace/pyside6-qml-frameless-window/tree/main

from __future__ import annotations

from ctypes import (
    POINTER,
    WINFUNCTYPE,  # pyrefly: ignore[missing-module-attribute]
    byref,
    c_void_p,
    cast,
    sizeof,
    windll,  # pyrefly: ignore[missing-module-attribute]
)
from ctypes.wintypes import BOOL, DWORD, HANDLE, HWND, LONG, LPCVOID, RECT, UINT
from functools import lru_cache
from typing import TYPE_CHECKING

import win32api
import win32con
import win32gui

from .c_structures import APPBARDATA, GUID

if TYPE_CHECKING:
    from collections.abc import Mapping
    from typing import Any

SM_CXPADDEDBORDER = 92


def get_window_size(hwnd: int) -> tuple[int, int, int, int]:
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top
    return left, top, width, height


def set_outer_window_rect(hwnd: int, rect: tuple[int, int, int, int]) -> None:
    """Set the outer rect, frame included."""
    left, top, right, bottom = rect
    flags = win32con.SWP_NOZORDER | win32con.SWP_NOACTIVATE | win32con.SWP_FRAMECHANGED
    windll.user32.SetWindowPos(hwnd, None, left, top, right - left, bottom - top, flags)


def refresh_window_frame(hwnd: int) -> None:
    """Force a WM_NCCALCSIZE round trip without moving the window."""
    flags = (
        win32con.SWP_FRAMECHANGED
        | win32con.SWP_NOSIZE
        | win32con.SWP_NOMOVE
        | win32con.SWP_NOZORDER
        | win32con.SWP_NOACTIVATE
    )
    windll.user32.SetWindowPos(hwnd, None, 0, 0, 0, 0, flags)


def is_maximized(hwnd: int) -> bool:
    window_placement = win32gui.GetWindowPlacement(hwnd)
    if not window_placement:
        return False

    return window_placement[1] == win32con.SW_MAXIMIZE


def is_minimized(hwnd: int) -> bool:
    return bool(win32gui.IsIconic(hwnd))


def is_fullscreen(hwnd: int) -> bool:
    # A maximized window overhangs the work area on all edges, so it covers the
    # whole monitor whenever the work area equals the monitor rect (auto-hide
    # taskbar, taskbar-less monitor). Fullscreen always runs with WS_MAXIMIZE
    # stripped, so a window that is still maximized is never fullscreen.
    if is_maximized(hwnd):
        return False

    win_rect = win32gui.GetWindowRect(hwnd)
    if not win_rect:
        return False

    return covers_monitor(win_rect)


def covers_monitor(rect: tuple[int, int, int, int]) -> bool:
    monitor_rect = get_monitor_rect_for(rect)
    return monitor_rect is not None and _covers(rect, monitor_rect)


def overhangs_monitor(rect: tuple[int, int, int, int]) -> bool:
    """Covers the monitor and extends past it on at least one edge."""
    monitor_rect = get_monitor_rect_for(rect)
    return monitor_rect is not None and _covers(rect, monitor_rect) and tuple(rect) != tuple(monitor_rect)


def _covers(rect: tuple[int, int, int, int], monitor_rect: tuple[int, int, int, int]) -> bool:
    left, top, right, bottom = rect
    m_left, m_top, m_right, m_bottom = monitor_rect
    return left <= m_left and top <= m_top and right >= m_right and bottom >= m_bottom


def get_monitor_rect_for(rect: tuple[int, int, int, int]) -> tuple[int, int, int, int] | None:
    monitor_info = get_monitor_info_for(rect)
    if monitor_info is None:
        return None
    return monitor_info["Monitor"]


def get_monitor_info_for(rect: tuple[int, int, int, int]) -> Mapping[str, Any] | None:
    monitor = win32api.MonitorFromRect(rect, win32con.MONITOR_DEFAULTTONEAREST)
    if not monitor:
        return None
    return win32api.GetMonitorInfo(monitor)


def get_monitor_rect(hwnd: int) -> tuple[int, int, int, int] | None:
    monitor_info = get_monitor_info(hwnd, win32con.MONITOR_DEFAULTTONEAREST)
    if not monitor_info:
        return None
    return monitor_info["Monitor"]


def get_monitor_info(hwnd: int, dw_flags: int) -> Mapping[str, Any] | None:
    monitor = win32api.MonitorFromWindow(hwnd, dw_flags)
    if not monitor:
        return None

    return win32api.GetMonitorInfo(monitor)


def get_resize_border_thickness(hwnd: int, *, horizontal: bool = True) -> int:
    frame = win32con.SM_CXSIZEFRAME if horizontal else win32con.SM_CYSIZEFRAME
    return get_system_metrics(hwnd, frame) + get_system_metrics(hwnd, SM_CXPADDEDBORDER)


def get_system_metrics(hwnd: int, index: int) -> int:
    dpi = windll.user32.GetDpiForWindow(hwnd)
    return windll.user32.GetSystemMetricsForDpi(index, dpi)


GetDpiForMonitor = windll.shcore.GetDpiForMonitor
GetDpiForMonitor.argtypes = [HANDLE, UINT, POINTER(UINT), POINTER(UINT)]
GetDpiForMonitor.restype = LONG

MDT_EFFECTIVE_DPI = 0


def get_primary_monitor_dpi() -> int:
    primary = win32api.MonitorFromPoint((0, 0), win32con.MONITOR_DEFAULTTOPRIMARY)
    dpi, unused = UINT(), UINT()
    if GetDpiForMonitor(int(primary), MDT_EFFECTIVE_DPI, byref(dpi), byref(unused)) != 0:
        return windll.user32.GetDpiForSystem()
    return dpi.value


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

        return bool(taskbar_state & Taskbar.ABS_AUTOHIDE)

    @classmethod
    def get_position(cls, monitor_rect: tuple[int, int, int, int]) -> int:
        appbar_data = APPBARDATA(sizeof(APPBARDATA), 0, 0, 0, RECT(*monitor_rect), 0)
        positions = [cls.LEFT, cls.TOP, cls.RIGHT, cls.BOTTOM]
        for position in positions:
            appbar_data.uEdge = position
            if windll.shell32.SHAppBarMessage(cls.ABM_GETAUTOHIDEBAREX, byref(appbar_data)):
                return position

        return cls.NO_POSITION


DwmSetWindowAttribute = windll.dwmapi.DwmSetWindowAttribute
DwmSetWindowAttribute.argtypes = [HWND, DWORD, LPCVOID, DWORD]
DwmSetWindowAttribute.restype = LONG

DwmFlush = windll.dwmapi.DwmFlush
DwmFlush.argtypes = []
DwmFlush.restype = LONG

DWMWA_TRANSITIONS_FORCEDISABLED = 3
DWMWA_CLOAK = 13
DWMWA_WINDOW_CORNER_PREFERENCE = 33
DWMWA_BORDER_COLOR = 34

DWMWCP_DEFAULT = 0
DWMWCP_DONOTROUND = 1

DWMWA_COLOR_DEFAULT = 0xFFFFFFFF
DWMWA_COLOR_NONE = 0xFFFFFFFE


_CLSID_TASKBAR_LIST = "{56FDF344-FD6D-11D0-958A-006097C9A090}"
_IID_ITASKBAR_LIST_2 = "{602D4995-B13A-429B-A66E-1935E44F4317}"
_CLSCTX_INPROC_SERVER = 1


@lru_cache(maxsize=1)
def _taskbar_list_2() -> tuple[c_void_p, Any] | None:
    ole32 = windll.ole32
    ole32.CoInitialize(None)

    clsid, iid = GUID(), GUID()
    ole32.CLSIDFromString(_CLSID_TASKBAR_LIST, byref(clsid))
    ole32.IIDFromString(_IID_ITASKBAR_LIST_2, byref(iid))

    interface = c_void_p()
    if ole32.CoCreateInstance(byref(clsid), None, _CLSCTX_INPROC_SERVER, byref(iid), byref(interface)) != 0:
        return None

    # IUnknown (0-2) | ITaskbarList: HrInit 3 ... | ITaskbarList2: MarkFullscreenWindow 8
    vtable = cast(interface, POINTER(POINTER(c_void_p * 9))).contents.contents
    hr_init = WINFUNCTYPE(LONG, c_void_p)(vtable[3])
    if hr_init(interface) != 0:
        return None

    mark_fullscreen_window = WINFUNCTYPE(LONG, c_void_p, HWND, BOOL)(vtable[8])
    return interface, mark_fullscreen_window


def set_shell_fullscreen_marker(hwnd: int, *, fullscreen: bool) -> None:
    """The shell only drops the taskbar for windows matching the monitor rect exactly;
    ours deliberately overhangs by the frame border, so tell the shell explicitly."""
    entry = _taskbar_list_2()
    if entry is None:
        return

    interface, mark_fullscreen_window = entry
    mark_fullscreen_window(interface, int(hwnd), 1 if fullscreen else 0)


def set_window_transitions_enabled(hwnd: int, *, enabled: bool) -> None:
    disabled = DWORD(0 if enabled else 1)
    DwmSetWindowAttribute(int(hwnd), DWMWA_TRANSITIONS_FORCEDISABLED, byref(disabled), sizeof(disabled))


def set_window_cloaked(hwnd: int, *, cloaked: bool) -> None:
    value = BOOL(1 if cloaked else 0)
    DwmSetWindowAttribute(int(hwnd), DWMWA_CLOAK, byref(value), sizeof(value))


def wait_for_next_composition() -> None:
    DwmFlush()


def set_window_corners_rounded(hwnd: int, *, rounded: bool) -> None:
    preference = DWORD(DWMWCP_DEFAULT if rounded else DWMWCP_DONOTROUND)
    DwmSetWindowAttribute(int(hwnd), DWMWA_WINDOW_CORNER_PREFERENCE, byref(preference), sizeof(preference))


def set_window_border_visible(hwnd: int, *, visible: bool) -> None:
    color = DWORD(DWMWA_COLOR_DEFAULT if visible else DWMWA_COLOR_NONE)
    DwmSetWindowAttribute(int(hwnd), DWMWA_BORDER_COLOR, byref(color), sizeof(color))


def set_style_flag(hwnd: int, flag: int, *, enabled: bool) -> None:
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
    style = style | flag if enabled else style & ~flag
    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)


def prevent_window_resize_for(hwnd: int) -> None:
    # Guarding on the live style keeps this idempotent without caching by
    # handle value, which would go stale once the OS recycles an HWND.
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
    if style & win32con.WS_THICKFRAME:
        win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style & ~win32con.WS_THICKFRAME)
