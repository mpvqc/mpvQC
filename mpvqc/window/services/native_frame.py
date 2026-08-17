# SPDX-FileCopyrightText: zhiyiYo
# SPDX-FileCopyrightText: Virace
# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Inspired and based on:
#  - https://github.com/zhiyiYo/PyQt-Frameless-Window
#  - https://gitee.com/Virace/pyside6-qml-frameless-window/tree/main

"""Windows-only decisions, kept out of the Windows package so they touch no
ctypes and run on any platform."""

from __future__ import annotations

from typing import Literal, NamedTuple, NewType, Protocol

type Rect = tuple[int, int, int, int]
"""left, top, right, bottom, the order a Win32 RECT uses."""

WindowRect = NewType("WindowRect", Rect)
ProposedRect = NewType("ProposedRect", Rect)
MonitorRect = NewType("MonitorRect", Rect)
WorkArea = NewType("WorkArea", Rect)
ClientRect = NewType("ClientRect", Rect)

type AppBarEdge = Literal["left", "top", "right", "bottom"]


class MonitorGeometry(NamedTuple):
    monitor_rect: MonitorRect
    work_area: WorkArea


class HitTestProbe(Protocol):
    def maximized(self) -> bool: ...
    def window_rect(self) -> WindowRect | None: ...
    def monitor_rect_for(self, rect: WindowRect) -> MonitorRect | None: ...
    def cursor_point(self) -> tuple[int, int]: ...
    def resize_band(self) -> int: ...


class CalcSizeProbe(Protocol):
    def proposed_rect(self) -> ProposedRect: ...
    def monitor_geometry_for(self, rect: ProposedRect) -> MonitorGeometry | None: ...
    def maximized(self) -> bool: ...
    def auto_hide_enabled(self) -> bool: ...
    def auto_hide_edge(self, monitor_rect: MonitorRect) -> AppBarEdge | None: ...


_HTTOP = 12
_HTTOPLEFT = 13
_HTTOPRIGHT = 14

_WVR_REDRAW = 0x0300


def handle_non_client_hit_test(probe: HitTestProbe) -> tuple[bool, int]:
    if probe.maximized():
        return False, 0

    rect = probe.window_rect()
    if rect is None:
        return False, 0

    monitor_rect = probe.monitor_rect_for(rect)
    fullscreen = monitor_rect is not None and overhangs(rect, monitor_rect)
    if fullscreen:
        return False, 0

    left, top, right, _ = rect
    cursor_x, cursor_y = probe.cursor_point()
    x_pos = cursor_x - left
    y_pos = cursor_y - top

    band = probe.resize_band()
    if y_pos >= band:
        return False, 0

    width = right - left
    corner = 2 * band
    if x_pos < corner:
        return True, _HTTOPLEFT
    if x_pos > width - corner:
        return True, _HTTOPRIGHT
    return True, _HTTOP


def handle_non_client_calculate_size(probe: CalcSizeProbe) -> tuple[bool, int, ClientRect | None]:
    destination = probe.proposed_rect()

    destination_monitor = probe.monitor_geometry_for(destination)
    if destination_monitor is None:
        return False, 0, None

    maximized = probe.maximized()
    fullscreen = not maximized and overhangs(destination, destination_monitor.monitor_rect)
    if not (maximized or fullscreen):
        return False, 0, None

    client_rect = ClientRect(destination_monitor.work_area if maximized else destination_monitor.monitor_rect)

    # Finding the edge means asking the shell about each of the four in turn,
    # every one a call into another process.
    if probe.auto_hide_enabled():
        edge = probe.auto_hide_edge(destination_monitor.monitor_rect)
        client_rect = reserve_auto_hide_taskbar_strip(client_rect, edge)

    return True, _WVR_REDRAW, client_rect


def overhangs(rect: WindowRect | ProposedRect, monitor_rect: MonitorRect) -> bool:
    return _covers(rect, monitor_rect) and rect != monitor_rect


def _covers(rect: Rect, monitor_rect: MonitorRect) -> bool:
    left, top, right, bottom = rect
    m_left, m_top, m_right, m_bottom = monitor_rect
    return left <= m_left and top <= m_top and right >= m_right and bottom >= m_bottom


_AUTO_HIDE_TASKBAR_STRIP = 2


def reserve_auto_hide_taskbar_strip(client_rect: ClientRect, edge: AppBarEdge | None) -> ClientRect:
    """A window that covers the taskbar edge completely leaves the mouse no way
    to bring the hidden taskbar back."""
    left, top, right, bottom = client_rect
    strip = _AUTO_HIDE_TASKBAR_STRIP
    match edge:
        case "left":
            return ClientRect((left + strip, top, right, bottom))
        case "top":
            return ClientRect((left, top + strip, right, bottom))
        case "right":
            return ClientRect((left, top, right - strip, bottom))
        case "bottom":
            return ClientRect((left, top, right, bottom - strip))
        case _:
            return client_rect


def read_hit_test_point(l_param: int) -> tuple[int, int]:
    """The WM_NCHITTEST cursor position: two signed 16-bit screen coordinates.
    Signed because a monitor left of or above the primary one has negative
    coordinates."""
    return _signed_16(l_param & 0xFFFF), _signed_16((l_param >> 16) & 0xFFFF)


def _signed_16(value: int) -> int:
    return value - 0x10000 if value & 0x8000 else value
