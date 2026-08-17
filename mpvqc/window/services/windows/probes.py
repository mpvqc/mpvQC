# SPDX-FileCopyrightText: zhiyiYo
# SPDX-FileCopyrightText: Virace
# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Inspired and based on:
#  - https://github.com/zhiyiYo/PyQt-Frameless-Window
#  - https://gitee.com/Virace/pyside6-qml-frameless-window/tree/main

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from mpvqc.window.services.native_frame import (
    MonitorGeometry,
    MonitorRect,
    ProposedRect,
    WindowRect,
    WorkArea,
    overhangs,
    read_hit_test_point,
)

from .native import (
    find_auto_hide_app_bar_edge,
    get_dpi_for_window,
    get_monitor_info_for_rect,
    get_monitor_info_for_window,
    get_resize_border_thickness_for_dpi,
    get_window_rect,
    is_app_bar_auto_hide,
    is_maximized,
    read_nccalcsize_proposed_rect,
)

if TYPE_CHECKING:
    from mpvqc.window.services.native_frame import AppBarEdge


def is_fullscreen(hwnd: int) -> bool:
    # A maximized window overhangs the work area on all edges, so it covers the
    # whole monitor whenever the work area equals the monitor rect (auto-hide
    # taskbar, taskbar-less monitor).
    if is_maximized(hwnd):
        return False

    rect = get_window_rect(hwnd)
    return rect is not None and _overhangs_monitor(WindowRect(rect))


def _overhangs_monitor(rect: WindowRect) -> bool:
    monitor_info = get_monitor_info_for_rect(rect)
    return monitor_info is not None and overhangs(rect, MonitorRect(monitor_info.monitor_rect))


def get_monitor_rect(hwnd: int) -> MonitorRect | None:
    monitor_info = get_monitor_info_for_window(hwnd)
    if monitor_info is None:
        return None
    return MonitorRect(monitor_info.monitor_rect)


def get_resize_border_thickness(hwnd: int, *, horizontal: bool = True) -> int:
    return get_resize_border_thickness_for_dpi(get_dpi_for_window(hwnd), horizontal=horizontal)


# Both probes read on the call, never ahead. Hoisting a query into __init__ or
# caching one keeps every test green and puts cross-process taskbar calls on the
# ordinary resize.
@dataclass(frozen=True)
class WindowsHitTestProbe:
    hwnd: int
    l_param: int

    def maximized(self) -> bool:
        return is_maximized(self.hwnd)

    def window_rect(self) -> WindowRect | None:
        rect = get_window_rect(self.hwnd)
        if rect is None:
            return None
        return WindowRect(rect)

    def monitor_rect_for(self, rect: WindowRect) -> MonitorRect | None:
        monitor_info = get_monitor_info_for_rect(rect)
        if monitor_info is None:
            return None
        return MonitorRect(monitor_info.monitor_rect)

    def cursor_point(self) -> tuple[int, int]:
        return read_hit_test_point(self.l_param)

    def resize_band(self) -> int:
        return get_resize_border_thickness(self.hwnd, horizontal=False)


@dataclass(frozen=True)
class WindowsCalcSizeProbe:
    hwnd: int
    l_param: int

    def proposed_rect(self) -> ProposedRect:
        return ProposedRect(read_nccalcsize_proposed_rect(self.l_param))

    def monitor_geometry_for(self, rect: ProposedRect) -> MonitorGeometry | None:
        monitor_info = get_monitor_info_for_rect(rect)
        if monitor_info is None:
            return None
        return MonitorGeometry(
            monitor_rect=MonitorRect(monitor_info.monitor_rect),
            work_area=WorkArea(monitor_info.work_area),
        )

    def maximized(self) -> bool:
        return is_maximized(self.hwnd)

    def auto_hide_enabled(self) -> bool:
        return is_app_bar_auto_hide()

    def auto_hide_edge(self, monitor_rect: MonitorRect) -> AppBarEdge | None:
        return find_auto_hide_app_bar_edge(monitor_rect)
