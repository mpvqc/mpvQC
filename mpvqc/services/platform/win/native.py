# SPDX-FileCopyrightText: zhiyiYo
# SPDX-FileCopyrightText: Virace
# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Inspired and based on:
#  - https://github.com/zhiyiYo/PyQt-Frameless-Window
#  - https://gitee.com/Virace/pyside6-qml-frameless-window/tree/main

"""Every Windows API call used by this package lives here, as a ctypes
binding with declared argument and return types, wrapped in a small
function that uses plain Python types.

One block per API call: its constants, its structures, its raw binding and
the wrappers the rest of the package uses.

All calls are best-effort: queries report failure through their return
value, setters fail silently — broken window decoration is not worth an
exception."""

from __future__ import annotations

from ctypes import (
    POINTER,
    WINFUNCTYPE,  # pyrefly: ignore[missing-module-attribute]
    Structure,
    WinDLL,  # pyrefly: ignore[missing-module-attribute]
    byref,
    c_int,
    c_short,
    c_size_t,
    c_ssize_t,
    c_void_p,
    c_wchar_p,
    cast,
    sizeof,
)
from ctypes.wintypes import BOOL, BYTE, DWORD, HANDLE, HWND, LONG, LPARAM, LPCVOID, MSG, POINT, RECT, UINT, WORD
from functools import lru_cache
from typing import TYPE_CHECKING, Literal, NamedTuple

if TYPE_CHECKING:
    from typing import Any

type AppBarEdge = Literal["left", "top", "right", "bottom"]

# Private handles: prototypes set on the shared ctypes.windll cache would be
# visible to every other library in the process.
_user32 = WinDLL("user32")
_shcore = WinDLL("shcore")
_shell32 = WinDLL("shell32")
_dwmapi = WinDLL("dwmapi")
_ole32 = WinDLL("ole32")

_SWP_NOSIZE = 0x0001
_SWP_NOMOVE = 0x0002
_SWP_NOZORDER = 0x0004
_SWP_NOACTIVATE = 0x0010
_SWP_FRAMECHANGED = 0x0020

_SetWindowPos = _user32.SetWindowPos
_SetWindowPos.argtypes = [HWND, HWND, c_int, c_int, c_int, c_int, UINT]
_SetWindowPos.restype = BOOL


def _set_window_pos(hwnd: int, x: int, y: int, width: int, height: int, flags: int) -> None:
    _SetWindowPos(hwnd, None, x, y, width, height, flags)


def set_outer_window_rect(hwnd: int, rect: tuple[int, int, int, int]) -> None:
    """Set the outer rect, frame included."""
    left, top, right, bottom = rect
    _set_window_pos(hwnd, left, top, right - left, bottom - top, _SWP_NOZORDER | _SWP_NOACTIVATE | _SWP_FRAMECHANGED)


def resize_window(hwnd: int, width: int, height: int) -> None:
    _set_window_pos(hwnd, 0, 0, width, height, _SWP_NOMOVE | _SWP_NOZORDER | _SWP_NOACTIVATE)


def refresh_window_frame(hwnd: int) -> None:
    """Force a WM_NCCALCSIZE round trip without moving the window."""
    flags = _SWP_FRAMECHANGED | _SWP_NOSIZE | _SWP_NOMOVE | _SWP_NOZORDER | _SWP_NOACTIVATE
    _set_window_pos(hwnd, 0, 0, 0, 0, flags)


_GetWindowRect = _user32.GetWindowRect
_GetWindowRect.argtypes = [HWND, POINTER(RECT)]
_GetWindowRect.restype = BOOL


def get_window_rect(hwnd: int) -> tuple[int, int, int, int]:
    rect = RECT()
    _GetWindowRect(hwnd, byref(rect))
    return rect.left, rect.top, rect.right, rect.bottom


_SW_MAXIMIZE = 3


class WindowPlacement(NamedTuple):
    flags: int
    show_cmd: int
    min_position: tuple[int, int]
    max_position: tuple[int, int]
    normal_rect: tuple[int, int, int, int]

    @property
    def shows_maximized(self) -> bool:
        return self.show_cmd == _SW_MAXIMIZE


class WINDOWPLACEMENT(Structure):
    _fields_ = [
        ("length", UINT),
        ("flags", UINT),
        ("showCmd", UINT),
        ("ptMinPosition", POINT),
        ("ptMaxPosition", POINT),
        ("rcNormalPosition", RECT),
    ]


_GetWindowPlacement = _user32.GetWindowPlacement
_GetWindowPlacement.argtypes = [HWND, POINTER(WINDOWPLACEMENT)]
_GetWindowPlacement.restype = BOOL


def get_window_placement(hwnd: int) -> WindowPlacement | None:
    data = WINDOWPLACEMENT(length=sizeof(WINDOWPLACEMENT))
    if not _GetWindowPlacement(hwnd, byref(data)):
        return None

    minimum, maximum, normal = data.ptMinPosition, data.ptMaxPosition, data.rcNormalPosition
    return WindowPlacement(
        flags=data.flags,
        show_cmd=data.showCmd,
        min_position=(minimum.x, minimum.y),
        max_position=(maximum.x, maximum.y),
        normal_rect=(normal.left, normal.top, normal.right, normal.bottom),
    )


def is_maximized(hwnd: int) -> bool:
    placement = get_window_placement(hwnd)
    return placement is not None and placement.shows_maximized


_SetWindowPlacement = _user32.SetWindowPlacement
_SetWindowPlacement.argtypes = [HWND, POINTER(WINDOWPLACEMENT)]
_SetWindowPlacement.restype = BOOL


def set_window_placement(hwnd: int, placement: WindowPlacement) -> None:
    data = WINDOWPLACEMENT(
        length=sizeof(WINDOWPLACEMENT),
        flags=placement.flags,
        showCmd=placement.show_cmd,
        ptMinPosition=POINT(*placement.min_position),
        ptMaxPosition=POINT(*placement.max_position),
        rcNormalPosition=RECT(*placement.normal_rect),
    )
    _SetWindowPlacement(hwnd, byref(data))


_ShowWindow = _user32.ShowWindow
_ShowWindow.argtypes = [HWND, c_int]
_ShowWindow.restype = BOOL


def maximize_window(hwnd: int) -> None:
    _ShowWindow(hwnd, _SW_MAXIMIZE)


_IsIconic = _user32.IsIconic
_IsIconic.argtypes = [HWND]
_IsIconic.restype = BOOL


def is_minimized(hwnd: int) -> bool:
    return bool(_IsIconic(hwnd))


_GWL_STYLE = -16
_WS_THICKFRAME = 0x00040000
_WS_MAXIMIZE = 0x01000000

_GetWindowLongPtr = _user32.GetWindowLongPtrW
_GetWindowLongPtr.argtypes = [HWND, c_int]
_GetWindowLongPtr.restype = c_ssize_t

_SetWindowLongPtr = _user32.SetWindowLongPtrW
_SetWindowLongPtr.argtypes = [HWND, c_int, c_ssize_t]
_SetWindowLongPtr.restype = c_ssize_t


def strip_maximize_style(hwnd: int) -> None:
    style = _GetWindowLongPtr(hwnd, _GWL_STYLE)
    _SetWindowLongPtr(hwnd, _GWL_STYLE, style & ~_WS_MAXIMIZE)


def prevent_window_resize_for(hwnd: int) -> None:
    # Checking the current style keeps this idempotent without caching handles;
    # a cache would go stale because Windows reuses HWND values.
    style = _GetWindowLongPtr(hwnd, _GWL_STYLE)
    if style & _WS_THICKFRAME:
        _SetWindowLongPtr(hwnd, _GWL_STYLE, style & ~_WS_THICKFRAME)


class MonitorInfo(NamedTuple):
    monitor_rect: tuple[int, int, int, int]
    work_area: tuple[int, int, int, int]


class MONITORINFO(Structure):
    _fields_ = [
        ("cbSize", DWORD),
        ("rcMonitor", RECT),
        ("rcWork", RECT),
        ("dwFlags", DWORD),
    ]


_MONITOR_DEFAULTTONEAREST = 2

_GetMonitorInfo = _user32.GetMonitorInfoW
_GetMonitorInfo.argtypes = [HANDLE, POINTER(MONITORINFO)]
_GetMonitorInfo.restype = BOOL


def _monitor_info(monitor: int | None) -> MonitorInfo | None:
    if not monitor:
        return None

    info = MONITORINFO(cbSize=sizeof(MONITORINFO))
    if not _GetMonitorInfo(monitor, byref(info)):
        return None

    monitor_rect = (info.rcMonitor.left, info.rcMonitor.top, info.rcMonitor.right, info.rcMonitor.bottom)
    work_area = (info.rcWork.left, info.rcWork.top, info.rcWork.right, info.rcWork.bottom)
    return MonitorInfo(monitor_rect=monitor_rect, work_area=work_area)


_MonitorFromRect = _user32.MonitorFromRect
_MonitorFromRect.argtypes = [POINTER(RECT), DWORD]
_MonitorFromRect.restype = HANDLE


def get_monitor_info_for_rect(rect: tuple[int, int, int, int]) -> MonitorInfo | None:
    monitor = _MonitorFromRect(byref(RECT(*rect)), _MONITOR_DEFAULTTONEAREST)
    return _monitor_info(monitor)


_MonitorFromWindow = _user32.MonitorFromWindow
_MonitorFromWindow.argtypes = [HWND, DWORD]
_MonitorFromWindow.restype = HANDLE


def get_monitor_info_for_window(hwnd: int) -> MonitorInfo | None:
    monitor = _MonitorFromWindow(hwnd, _MONITOR_DEFAULTTONEAREST)
    return _monitor_info(monitor)


_GetDpiForWindow = _user32.GetDpiForWindow
_GetDpiForWindow.argtypes = [HWND]
_GetDpiForWindow.restype = UINT


def get_dpi_for_window(hwnd: int) -> int:
    return _GetDpiForWindow(hwnd)


_SM_CYCAPTION = 4
_SM_CXSIZEFRAME = 32
_SM_CYSIZEFRAME = 33
_SM_CXPADDEDBORDER = 92

_GetSystemMetricsForDpi = _user32.GetSystemMetricsForDpi
_GetSystemMetricsForDpi.argtypes = [c_int, UINT]
_GetSystemMetricsForDpi.restype = c_int


def get_resize_border_thickness_for_dpi(dpi: int, *, horizontal: bool) -> int:
    frame = _SM_CXSIZEFRAME if horizontal else _SM_CYSIZEFRAME
    return _GetSystemMetricsForDpi(frame, dpi) + _GetSystemMetricsForDpi(_SM_CXPADDEDBORDER, dpi)


def get_caption_height_for_dpi(dpi: int) -> int:
    return _GetSystemMetricsForDpi(_SM_CYCAPTION, dpi)


_MDT_EFFECTIVE_DPI = 0
_MONITOR_DEFAULTTOPRIMARY = 1

_GetDpiForSystem = _user32.GetDpiForSystem
_GetDpiForSystem.argtypes = []
_GetDpiForSystem.restype = UINT

_GetDpiForMonitor = _shcore.GetDpiForMonitor
_GetDpiForMonitor.argtypes = [HANDLE, UINT, POINTER(UINT), POINTER(UINT)]
_GetDpiForMonitor.restype = LONG

_MonitorFromPoint = _user32.MonitorFromPoint
_MonitorFromPoint.argtypes = [POINT, DWORD]
_MonitorFromPoint.restype = HANDLE


def get_primary_monitor_dpi() -> int:
    primary = _MonitorFromPoint(POINT(0, 0), _MONITOR_DEFAULTTOPRIMARY)
    dpi, unused = UINT(), UINT()
    if _GetDpiForMonitor(primary, _MDT_EFFECTIVE_DPI, byref(dpi), byref(unused)) != 0:
        return _GetDpiForSystem()
    return dpi.value


_ABS_AUTOHIDE = 1
_ABM_GETSTATE = 4
_ABM_GETAUTOHIDEBAREX = 11

_APP_BAR_EDGES: dict[AppBarEdge, int] = {"left": 0, "top": 1, "right": 2, "bottom": 3}


class APPBARDATA(Structure):
    _fields_ = [
        ("cbSize", DWORD),
        ("hWnd", HWND),
        ("uCallbackMessage", UINT),
        ("uEdge", UINT),
        ("rc", RECT),
        ("lParam", LPARAM),
    ]


_SHAppBarMessage = _shell32.SHAppBarMessage
_SHAppBarMessage.argtypes = [DWORD, POINTER(APPBARDATA)]
_SHAppBarMessage.restype = c_size_t  # UINT_PTR


def is_app_bar_auto_hide() -> bool:
    data = APPBARDATA(sizeof(APPBARDATA), 0, 0, 0, RECT(0, 0, 0, 0), 0)
    return bool(_SHAppBarMessage(_ABM_GETSTATE, byref(data)) & _ABS_AUTOHIDE)


def find_auto_hide_app_bar_edge(monitor_rect: tuple[int, int, int, int]) -> AppBarEdge | None:
    for name, edge in _APP_BAR_EDGES.items():
        data = APPBARDATA(sizeof(APPBARDATA), 0, 0, edge, RECT(*monitor_rect), 0)
        if _SHAppBarMessage(_ABM_GETAUTOHIDEBAREX, byref(data)):
            return name

    return None


_DWMWA_TRANSITIONS_FORCEDISABLED = 3
_DWMWA_CLOAK = 13
_DWMWA_WINDOW_CORNER_PREFERENCE = 33
_DWMWA_BORDER_COLOR = 34

_DWMWCP_DEFAULT = 0
_DWMWCP_DONOTROUND = 1

_DWMWA_COLOR_DEFAULT = 0xFFFFFFFF
_DWMWA_COLOR_NONE = 0xFFFFFFFE

_DwmSetWindowAttribute = _dwmapi.DwmSetWindowAttribute
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


_DwmFlush = _dwmapi.DwmFlush
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


class WINDOWPOS(Structure):
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
    _fields_ = [("rgrc", RECT * 3), ("lppos", POINTER(WINDOWPOS))]


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

_S_OK = 0
_S_FALSE = 1  # COM already started on this thread
_RPC_E_CHANGED_MODE = -2147417850  # COM already started with the other threading model; still usable


class GUID(Structure):
    _fields_ = [
        ("data1", DWORD),
        ("data2", WORD),
        ("data3", WORD),
        ("data4", BYTE * 8),
    ]


_CoInitialize = _ole32.CoInitialize
_CoInitialize.argtypes = [c_void_p]
_CoInitialize.restype = LONG

_CLSIDFromString = _ole32.CLSIDFromString
_CLSIDFromString.argtypes = [c_wchar_p, POINTER(GUID)]
_CLSIDFromString.restype = LONG

_IIDFromString = _ole32.IIDFromString
_IIDFromString.argtypes = [c_wchar_p, POINTER(GUID)]
_IIDFromString.restype = LONG

_CoCreateInstance = _ole32.CoCreateInstance
_CoCreateInstance.argtypes = [POINTER(GUID), c_void_p, DWORD, POINTER(GUID), POINTER(c_void_p)]
_CoCreateInstance.restype = LONG


class _ComUnavailableError(Exception):
    pass


# A successful instance lives until process exit on purpose. The OS reclaims
# COM and the interface with it. lru_cache does not store raised exceptions,
# so a failed attempt is simply tried again on the next call.
@lru_cache(maxsize=1)
def _taskbar_list_2() -> tuple[c_void_p, Any]:
    if _CoInitialize(None) not in {_S_OK, _S_FALSE, _RPC_E_CHANGED_MODE}:
        raise _ComUnavailableError

    clsid, iid = GUID(), GUID()
    _CLSIDFromString(_CLSID_TASKBAR_LIST, byref(clsid))
    _IIDFromString(_IID_ITASKBAR_LIST_2, byref(iid))

    interface = c_void_p()
    if _CoCreateInstance(byref(clsid), None, _CLSCTX_INPROC_SERVER, byref(iid), byref(interface)) != 0:
        raise _ComUnavailableError

    # IUnknown (0-2) | ITaskbarList: HrInit 3 ... | ITaskbarList2: MarkFullscreenWindow 8
    vtable = cast(interface, POINTER(POINTER(c_void_p * 9))).contents.contents
    hr_init = WINFUNCTYPE(LONG, c_void_p)(vtable[3])
    if hr_init(interface) != 0:
        raise _ComUnavailableError

    mark_fullscreen = WINFUNCTYPE(LONG, c_void_p, HWND, BOOL)(vtable[8])
    return interface, mark_fullscreen


def mark_fullscreen_window(hwnd: int, *, fullscreen: bool) -> None:
    try:
        interface, mark_fullscreen = _taskbar_list_2()
    except _ComUnavailableError:
        return

    mark_fullscreen(interface, hwnd, 1 if fullscreen else 0)
