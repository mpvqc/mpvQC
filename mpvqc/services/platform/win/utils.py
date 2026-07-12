# SPDX-FileCopyrightText: zhiyiYo
# SPDX-FileCopyrightText: Virace
# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Inspired and based on:
#  - https://github.com/zhiyiYo/PyQt-Frameless-Window
#  - https://gitee.com/Virace/pyside6-qml-frameless-window/tree/main

from __future__ import annotations

from .native import (
    dwm_flush,
    find_auto_hide_app_bar,
    get_dpi_for_window,
    get_monitor_info_for_rect,
    get_monitor_info_for_window,
    get_resize_border_thickness_for_dpi,
    get_window_rect,
    is_app_bar_auto_hide,
    is_maximized,
    mark_fullscreen_window,
)


def get_window_size(hwnd: int) -> tuple[int, int, int, int]:
    left, top, right, bottom = get_window_rect(hwnd)
    width = right - left
    height = bottom - top
    return left, top, width, height


def is_fullscreen(hwnd: int) -> bool:
    # A maximized window overhangs the work area on all edges, so it covers the
    # whole monitor whenever the work area equals the monitor rect (auto-hide
    # taskbar, taskbar-less monitor). Fullscreen always runs with WS_MAXIMIZE
    # stripped, so a window that is still maximized is never fullscreen.
    if is_maximized(hwnd):
        return False

    win_rect = get_window_rect(hwnd)
    if not win_rect:
        return False

    return covers_monitor(win_rect)


def covers_monitor(rect: tuple[int, int, int, int]) -> bool:
    monitor_rect = _monitor_rect_for(rect)
    return monitor_rect is not None and _covers(rect, monitor_rect)


def overhangs_monitor(rect: tuple[int, int, int, int]) -> bool:
    """Covers the monitor and extends past it on at least one edge."""
    monitor_rect = _monitor_rect_for(rect)
    return monitor_rect is not None and _covers(rect, monitor_rect) and tuple(rect) != tuple(monitor_rect)


def _covers(rect: tuple[int, int, int, int], monitor_rect: tuple[int, int, int, int]) -> bool:
    left, top, right, bottom = rect
    m_left, m_top, m_right, m_bottom = monitor_rect
    return left <= m_left and top <= m_top and right >= m_right and bottom >= m_bottom


def _monitor_rect_for(rect: tuple[int, int, int, int]) -> tuple[int, int, int, int] | None:
    monitor_info = get_monitor_info_for_rect(rect)
    if monitor_info is None:
        return None
    return monitor_info.monitor_rect


def get_monitor_rect(hwnd: int) -> tuple[int, int, int, int] | None:
    monitor_info = get_monitor_info_for_window(hwnd)
    if monitor_info is None:
        return None
    return monitor_info.monitor_rect


def get_resize_border_thickness(hwnd: int, *, horizontal: bool = True) -> int:
    return get_resize_border_thickness_for_dpi(get_dpi_for_window(hwnd), horizontal=horizontal)


class Taskbar:
    LEFT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    NO_POSITION = 4

    AUTO_HIDE_THICKNESS = 2

    @staticmethod
    def is_auto_hide() -> bool:
        return is_app_bar_auto_hide()

    @classmethod
    def get_position(cls, monitor_rect: tuple[int, int, int, int]) -> int:
        positions = [cls.LEFT, cls.TOP, cls.RIGHT, cls.BOTTOM]
        for position in positions:
            if find_auto_hide_app_bar(position, monitor_rect):
                return position

        return cls.NO_POSITION


def set_shell_fullscreen_marker(hwnd: int, *, fullscreen: bool) -> None:
    """The shell only drops the taskbar for windows matching the monitor rect exactly;
    ours deliberately overhangs by the frame border, so tell the shell explicitly."""
    mark_fullscreen_window(int(hwnd), fullscreen=fullscreen)


def wait_for_next_composition() -> None:
    dwm_flush()
