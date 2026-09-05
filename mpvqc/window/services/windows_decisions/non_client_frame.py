# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, Literal, Protocol

from .frame_geometry import ClientRect, overhangs

if TYPE_CHECKING:
    from .frame_geometry import MonitorGeometry, MonitorRect, ProposedRect, WindowRect

type AppBarEdge = Literal["left", "top", "right", "bottom"]


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

    # Finding the edge is four calls into the Windows shell, one per edge.
    if probe.auto_hide_enabled():
        edge = probe.auto_hide_edge(destination_monitor.monitor_rect)
        client_rect = reserve_auto_hide_taskbar_strip(client_rect, edge)

    return True, _WVR_REDRAW, client_rect


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
