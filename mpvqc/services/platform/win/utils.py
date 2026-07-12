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
    find_auto_hide_app_bar_edge,
    get_dpi_for_window,
    get_monitor_info_for_rect,
    get_monitor_info_for_window,
    get_resize_border_thickness_for_dpi,
    get_window_rect,
    is_app_bar_auto_hide,
    is_maximized,
    mark_fullscreen_window,
)


def is_fullscreen(hwnd: int) -> bool:
    # A maximized window overhangs the work area on all edges, so it covers the
    # whole monitor whenever the work area equals the monitor rect (auto-hide
    # taskbar, taskbar-less monitor). Fullscreen always runs with WS_MAXIMIZE
    # stripped, so a window that is still maximized is never fullscreen.
    if is_maximized(hwnd):
        return False

    rect = get_window_rect(hwnd)
    return rect is not None and overhangs_monitor(rect)


def overhangs_monitor(rect: tuple[int, int, int, int]) -> bool:
    monitor_rect = _monitor_rect_for(rect)
    return monitor_rect is not None and overhangs(rect, monitor_rect)


def overhangs(rect: tuple[int, int, int, int], monitor_rect: tuple[int, int, int, int]) -> bool:
    """Covers the monitor rect and extends past it on at least one edge."""
    return _covers(rect, monitor_rect) and tuple(rect) != tuple(monitor_rect)


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


# An auto-hide taskbar collapses to a thin strip at its monitor edge.
_AUTO_HIDE_TASKBAR_STRIP = 2


def reserve_auto_hide_taskbar_strip(
    client_rect: tuple[int, int, int, int], monitor_rect: tuple[int, int, int, int]
) -> tuple[int, int, int, int]:
    """Keep a thin strip of the client rect free at the taskbar edge, so the
    mouse can still bring back the hidden taskbar."""
    if not is_app_bar_auto_hide():
        return client_rect

    left, top, right, bottom = client_rect
    strip = _AUTO_HIDE_TASKBAR_STRIP
    match find_auto_hide_app_bar_edge(monitor_rect):
        case "left":
            return left + strip, top, right, bottom
        case "top":
            return left, top + strip, right, bottom
        case "right":
            return left, top, right - strip, bottom
        case "bottom":
            return left, top, right, bottom - strip
        case _:
            return client_rect


def set_shell_fullscreen_marker(hwnd: int, *, fullscreen: bool) -> None:
    """The shell hides the taskbar only for windows that match the monitor rect
    exactly. Our fullscreen window is larger by the frame border on purpose, so
    the shell must be told explicitly."""
    mark_fullscreen_window(int(hwnd), fullscreen=fullscreen)


def wait_for_next_composition() -> None:
    dwm_flush()
