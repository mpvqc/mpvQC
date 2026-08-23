# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from mpvqc.window.services.windows_decisions import (
    MonitorGeometry,
    MonitorRect,
    ProposedRect,
    ResizeBorders,
    WindowRect,
    WorkArea,
    classify_native_state,
    overhangs,
    read_hit_test_point,
)

from .native import (
    find_auto_hide_app_bar_edge,
    get_dpi_for_window,
    get_monitor_info_for_rect,
    get_monitor_info_for_window,
    get_resize_border_thickness_for_dpi,
    get_window_placement,
    get_window_rect,
    is_app_bar_auto_hide,
    is_maximized,
    is_minimized,
    read_nccalcsize_proposed_rect,
)

if TYPE_CHECKING:
    from PySide6.QtGui import QWindow

    from mpvqc.window.services.windows_decisions import AppBarEdge, NativeWindowState, WindowPlacement


def overhangs_monitor(hwnd: int) -> bool:
    rect = get_window_rect(hwnd)
    if rect is None:
        return False

    window_rect = WindowRect(rect)
    monitor_info = get_monitor_info_for_rect(window_rect)
    return monitor_info is not None and overhangs(window_rect, MonitorRect(monitor_info.monitor_rect))


def get_monitor_rect(hwnd: int) -> MonitorRect | None:
    monitor_info = get_monitor_info_for_window(hwnd)
    if monitor_info is None:
        return None
    return MonitorRect(monitor_info.monitor_rect)


def get_resize_border_thickness(hwnd: int, *, horizontal: bool = True) -> int:
    return get_resize_border_thickness_for_dpi(get_dpi_for_window(hwnd), horizontal=horizontal)


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


@dataclass(frozen=True)
class WindowsWindowStateProbe:
    # The handle stays unbound until a question: winId() on a window without a
    # native handle creates one, and the frame configuration would come too
    # late to reclaim the caption strip.
    window: QWindow

    def native_state(self) -> NativeWindowState:
        return classify_native_state(self)

    def minimized(self) -> bool:
        return is_minimized(self.window.winId())

    def maximized(self) -> bool:
        return is_maximized(self.window.winId())

    def overhangs_monitor(self) -> bool:
        return overhangs_monitor(self.window.winId())

    def placement(self) -> WindowPlacement | None:
        return get_window_placement(self.window.winId())

    def restores_to_maximized(self) -> bool:
        placement = get_window_placement(self.window.winId())
        return placement is not None and placement.restores_to_maximized

    def monitor_rect(self) -> MonitorRect | None:
        return get_monitor_rect(self.window.winId())

    def resize_borders(self) -> ResizeBorders:
        hwnd = self.window.winId()
        return ResizeBorders(
            horizontal=get_resize_border_thickness(hwnd, horizontal=True),
            vertical=get_resize_border_thickness(hwnd, horizontal=False),
        )
