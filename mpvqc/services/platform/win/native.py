# SPDX-FileCopyrightText: zhiyiYo
# SPDX-FileCopyrightText: Virace
# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Inspired and based on:
#  - https://github.com/zhiyiYo/PyQt-Frameless-Window
#  - https://gitee.com/Virace/pyside6-qml-frameless-window/tree/main

"""The Windows API surface: every call into Windows lives here, whether it
goes through ctypes or pywin32, wrapped in a plain-typed snake_case function.

One block per API call: its constants, its structures, its raw binding and
the wrappers the rest of the package uses. Other modules touch win32con only
as call vocabulary (metric indexes, flags, message ids)."""

from __future__ import annotations

from ctypes import (
    POINTER,
    WINFUNCTYPE,  # pyrefly: ignore[missing-module-attribute]
    Structure,
    byref,
    c_int,
    c_short,
    c_size_t,
    c_void_p,
    c_wchar_p,
    cast,
    sizeof,
    windll,  # pyrefly: ignore[missing-module-attribute]
)
from ctypes.wintypes import BOOL, BYTE, DWORD, HANDLE, HWND, LONG, LPARAM, LPCVOID, MSG, RECT, UINT, WORD
from functools import lru_cache
from typing import TYPE_CHECKING, NamedTuple

import win32api
import win32con
import win32gui

if TYPE_CHECKING:
    from typing import Any

_SetWindowPos = windll.user32.SetWindowPos
_SetWindowPos.argtypes = [HWND, HWND, c_int, c_int, c_int, c_int, UINT]
_SetWindowPos.restype = BOOL


def set_window_pos(hwnd: int, x: int, y: int, width: int, height: int, flags: int) -> None:
    _SetWindowPos(hwnd, None, x, y, width, height, flags)


def set_outer_window_rect(hwnd: int, rect: tuple[int, int, int, int]) -> None:
    """Set the outer rect, frame included."""
    left, top, right, bottom = rect
    flags = win32con.SWP_NOZORDER | win32con.SWP_NOACTIVATE | win32con.SWP_FRAMECHANGED
    set_window_pos(hwnd, left, top, right - left, bottom - top, flags)


def refresh_window_frame(hwnd: int) -> None:
    """Force a WM_NCCALCSIZE round trip without moving the window."""
    flags = (
        win32con.SWP_FRAMECHANGED
        | win32con.SWP_NOSIZE
        | win32con.SWP_NOMOVE
        | win32con.SWP_NOZORDER
        | win32con.SWP_NOACTIVATE
    )
    set_window_pos(hwnd, 0, 0, 0, 0, flags)


def get_window_rect(hwnd: int) -> tuple[int, int, int, int]:
    return win32gui.GetWindowRect(hwnd)


def get_window_placement(hwnd: int) -> tuple:
    return win32gui.GetWindowPlacement(hwnd)


def set_window_placement(hwnd: int, placement: tuple) -> None:
    win32gui.SetWindowPlacement(hwnd, placement)


def maximize_window(hwnd: int) -> None:
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)


def is_maximized(hwnd: int) -> bool:
    placement = win32gui.GetWindowPlacement(hwnd)
    if not placement:
        return False

    return placement[1] == win32con.SW_MAXIMIZE


def is_minimized(hwnd: int) -> bool:
    return bool(win32gui.IsIconic(hwnd))


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


class MonitorInfo(NamedTuple):
    monitor_rect: tuple[int, int, int, int]
    work_area: tuple[int, int, int, int]


def get_monitor_info_for_rect(rect: tuple[int, int, int, int]) -> MonitorInfo | None:
    monitor = win32api.MonitorFromRect(rect, win32con.MONITOR_DEFAULTTONEAREST)
    return _monitor_info(monitor)


def get_monitor_info_for_window(hwnd: int) -> MonitorInfo | None:
    monitor = win32api.MonitorFromWindow(hwnd, win32con.MONITOR_DEFAULTTONEAREST)
    return _monitor_info(monitor)


def _monitor_info(monitor: int) -> MonitorInfo | None:
    if not monitor:
        return None

    info = win32api.GetMonitorInfo(monitor)
    return MonitorInfo(monitor_rect=info["Monitor"], work_area=info["Work"])


_GetDpiForWindow = windll.user32.GetDpiForWindow
_GetDpiForWindow.argtypes = [HWND]
_GetDpiForWindow.restype = UINT


def get_dpi_for_window(hwnd: int) -> int:
    return _GetDpiForWindow(hwnd)


_GetDpiForSystem = windll.user32.GetDpiForSystem
_GetDpiForSystem.argtypes = []
_GetDpiForSystem.restype = UINT


_SM_CXPADDEDBORDER = 92

_GetSystemMetricsForDpi = windll.user32.GetSystemMetricsForDpi
_GetSystemMetricsForDpi.argtypes = [c_int, UINT]
_GetSystemMetricsForDpi.restype = c_int


def get_system_metrics_for_dpi(index: int, dpi: int) -> int:
    return _GetSystemMetricsForDpi(index, dpi)


def get_resize_border_thickness_for_dpi(dpi: int, *, horizontal: bool) -> int:
    frame = win32con.SM_CXSIZEFRAME if horizontal else win32con.SM_CYSIZEFRAME
    return _GetSystemMetricsForDpi(frame, dpi) + _GetSystemMetricsForDpi(_SM_CXPADDEDBORDER, dpi)


_MDT_EFFECTIVE_DPI = 0

_GetDpiForMonitor = windll.shcore.GetDpiForMonitor
_GetDpiForMonitor.argtypes = [HANDLE, UINT, POINTER(UINT), POINTER(UINT)]
_GetDpiForMonitor.restype = LONG


def get_primary_monitor_dpi() -> int:
    primary = win32api.MonitorFromPoint((0, 0), win32con.MONITOR_DEFAULTTOPRIMARY)
    dpi, unused = UINT(), UINT()
    if _GetDpiForMonitor(int(primary), _MDT_EFFECTIVE_DPI, byref(dpi), byref(unused)) != 0:
        return _GetDpiForSystem()
    return dpi.value


_ABS_AUTOHIDE = 1
_ABM_GETSTATE = 4
_ABM_GETAUTOHIDEBAREX = 11


class APPBARDATA(Structure):
    _fields_ = [
        ("cbSize", DWORD),
        ("hWnd", HWND),
        ("uCallbackMessage", UINT),
        ("uEdge", UINT),
        ("rc", RECT),
        ("lParam", LPARAM),
    ]


_SHAppBarMessage = windll.shell32.SHAppBarMessage
_SHAppBarMessage.argtypes = [DWORD, POINTER(APPBARDATA)]
_SHAppBarMessage.restype = c_size_t  # UINT_PTR


def is_app_bar_auto_hide() -> bool:
    data = APPBARDATA(sizeof(APPBARDATA), 0, 0, 0, RECT(0, 0, 0, 0), 0)
    return bool(_SHAppBarMessage(_ABM_GETSTATE, byref(data)) & _ABS_AUTOHIDE)


def find_auto_hide_app_bar(edge: int, monitor_rect: tuple[int, int, int, int]) -> int:
    data = APPBARDATA(sizeof(APPBARDATA), 0, 0, edge, RECT(*monitor_rect), 0)
    return _SHAppBarMessage(_ABM_GETAUTOHIDEBAREX, byref(data))


_DWMWA_TRANSITIONS_FORCEDISABLED = 3
_DWMWA_CLOAK = 13
_DWMWA_WINDOW_CORNER_PREFERENCE = 33
_DWMWA_BORDER_COLOR = 34

_DWMWCP_DEFAULT = 0
_DWMWCP_DONOTROUND = 1

_DWMWA_COLOR_DEFAULT = 0xFFFFFFFF
_DWMWA_COLOR_NONE = 0xFFFFFFFE

_DwmSetWindowAttribute = windll.dwmapi.DwmSetWindowAttribute
_DwmSetWindowAttribute.argtypes = [HWND, DWORD, LPCVOID, DWORD]
_DwmSetWindowAttribute.restype = LONG


def _dwm_set_window_attribute(hwnd: int, attribute: int, value: int) -> None:
    data = DWORD(value)
    _DwmSetWindowAttribute(hwnd, attribute, byref(data), sizeof(data))


def set_window_transitions_enabled(hwnd: int, *, enabled: bool) -> None:
    _dwm_set_window_attribute(hwnd, _DWMWA_TRANSITIONS_FORCEDISABLED, 0 if enabled else 1)


def set_window_cloaked(hwnd: int, *, cloaked: bool) -> None:
    _dwm_set_window_attribute(hwnd, _DWMWA_CLOAK, 1 if cloaked else 0)


def set_window_corners_rounded(hwnd: int, *, rounded: bool) -> None:
    preference = _DWMWCP_DEFAULT if rounded else _DWMWCP_DONOTROUND
    _dwm_set_window_attribute(hwnd, _DWMWA_WINDOW_CORNER_PREFERENCE, preference)


def set_window_border_visible(hwnd: int, *, visible: bool) -> None:
    color = _DWMWA_COLOR_DEFAULT if visible else _DWMWA_COLOR_NONE
    _dwm_set_window_attribute(hwnd, _DWMWA_BORDER_COLOR, color)


_DwmFlush = windll.dwmapi.DwmFlush
_DwmFlush.argtypes = []
_DwmFlush.restype = LONG


def dwm_flush() -> None:
    _DwmFlush()


class WindowMessage(NamedTuple):
    hwnd: int | None
    message: int
    w_param: int
    l_param: int


def read_window_message(address: int) -> WindowMessage:
    msg = MSG.from_address(address)
    return WindowMessage(msg.hWnd, msg.message, msg.wParam, msg.lParam)


def read_hit_test_point(l_param: int) -> tuple[int, int]:
    """The WM_NCHITTEST cursor position: two signed 16-bit screen coordinates."""
    x = c_short(l_param & 0xFFFF).value
    y = c_short((l_param >> 16) & 0xFFFF).value
    return x, y


class PWINDOWPOS(Structure):
    _fields_ = [
        ("hWnd", HWND),
        ("hwndInsertAfter", HWND),
        ("x", c_int),
        ("y", c_int),
        ("cx", c_int),
        ("cy", c_int),
        ("flags", UINT),
    ]


class NCCALCSIZE_PARAMS(Structure):
    _fields_ = [("rgrc", RECT * 3), ("lppos", POINTER(PWINDOWPOS))]


_LPNCCALCSIZE_PARAMS = POINTER(NCCALCSIZE_PARAMS)


def read_nccalcsize_proposed_rect(l_param: int) -> tuple[int, int, int, int]:
    rect = cast(l_param, _LPNCCALCSIZE_PARAMS).contents.rgrc[0]
    return rect.left, rect.top, rect.right, rect.bottom


def write_nccalcsize_client_rect(l_param: int, rect: tuple[int, int, int, int]) -> None:
    client = cast(l_param, _LPNCCALCSIZE_PARAMS).contents.rgrc[0]
    client.left, client.top, client.right, client.bottom = rect


_CLSID_TASKBAR_LIST = "{56FDF344-FD6D-11D0-958A-006097C9A090}"
_IID_ITASKBAR_LIST_2 = "{602D4995-B13A-429B-A66E-1935E44F4317}"
_CLSCTX_INPROC_SERVER = 1


class GUID(Structure):
    _fields_ = [
        ("data1", DWORD),
        ("data2", WORD),
        ("data3", WORD),
        ("data4", BYTE * 8),
    ]


_CoInitialize = windll.ole32.CoInitialize
_CoInitialize.argtypes = [c_void_p]
_CoInitialize.restype = LONG

_CLSIDFromString = windll.ole32.CLSIDFromString
_CLSIDFromString.argtypes = [c_wchar_p, POINTER(GUID)]
_CLSIDFromString.restype = LONG

_IIDFromString = windll.ole32.IIDFromString
_IIDFromString.argtypes = [c_wchar_p, POINTER(GUID)]
_IIDFromString.restype = LONG

_CoCreateInstance = windll.ole32.CoCreateInstance
_CoCreateInstance.argtypes = [POINTER(GUID), c_void_p, DWORD, POINTER(GUID), POINTER(c_void_p)]
_CoCreateInstance.restype = LONG


@lru_cache(maxsize=1)
def _taskbar_list_2() -> tuple[c_void_p, Any] | None:
    _CoInitialize(None)

    clsid, iid = GUID(), GUID()
    _CLSIDFromString(_CLSID_TASKBAR_LIST, byref(clsid))
    _IIDFromString(_IID_ITASKBAR_LIST_2, byref(iid))

    interface = c_void_p()
    if _CoCreateInstance(byref(clsid), None, _CLSCTX_INPROC_SERVER, byref(iid), byref(interface)) != 0:
        return None

    # IUnknown (0-2) | ITaskbarList: HrInit 3 ... | ITaskbarList2: MarkFullscreenWindow 8
    vtable = cast(interface, POINTER(POINTER(c_void_p * 9))).contents.contents
    hr_init = WINFUNCTYPE(LONG, c_void_p)(vtable[3])
    if hr_init(interface) != 0:
        return None

    mark_fullscreen = WINFUNCTYPE(LONG, c_void_p, HWND, BOOL)(vtable[8])
    return interface, mark_fullscreen


def mark_fullscreen_window(hwnd: int, *, fullscreen: bool) -> None:
    entry = _taskbar_list_2()
    if entry is None:
        return

    interface, mark_fullscreen = entry
    mark_fullscreen(interface, hwnd, 1 if fullscreen else 0)
