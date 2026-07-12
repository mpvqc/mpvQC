# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

from .native import (
    get_window_placement,
    is_maximized,
    is_minimized,
    maximize_window,
    refresh_window_frame,
    set_outer_window_rect,
    set_window_border_visible,
    set_window_corners_rounded,
    set_window_placement,
    set_window_transitions_enabled,
    strip_maximize_style,
)
from .utils import (
    get_monitor_rect,
    get_resize_border_thickness,
    is_fullscreen,
    set_shell_fullscreen_marker,
)

if TYPE_CHECKING:
    from PySide6.QtGui import QWindow

    from .native import WindowPlacement


class WindowsFullscreenHandler:
    """Fullscreen as a single atomic move to the monitor rect, avoiding Qt's style
    swap plus restore/re-maximize dance that flashes intermediate frames.

    Windows pins the geometry of a maximized window, so WS_MAXIMIZE is dropped
    from the style while fullscreen. Restoring the saved placement on exit brings
    back the previous state, including the remembered normal geometry.

    The window extends off-screen by the frame border on the left, right and
    bottom: Qt's frame arithmetic then yields a scene of exactly the monitor
    rect, and the surviving non-client sliver keeps DWM from permanently dropping
    the window's transition animations, which it does once a client rect fills
    the whole window.

    Assumes a single top-level window: one parked placement at a time, always
    for the same window."""

    def __init__(self) -> None:
        self._saved_placement: WindowPlacement | None = None

    def enter(self, window: QWindow) -> None:
        hwnd = int(window.winId())

        monitor_rect = get_monitor_rect(hwnd)
        if monitor_rect is None:
            return

        # A parked placement while not covering the monitor means the OS took the
        # window out of fullscreen behind our back (e.g. Win+Up). Retire that
        # session so a later exit cannot restore its stale placement.
        if self._saved_placement is not None and not is_fullscreen(hwnd):
            self._retire_abandoned_session(hwnd)
        if self._saved_placement is None:
            self._saved_placement = get_window_placement(hwnd)

        # The frame styles stay on, so Windows 11 would keep the rounded corners
        # and accent border over the fullscreen surface.
        set_window_corners_rounded(hwnd, rounded=False)
        set_window_border_visible(hwnd, visible=False)

        left, top, right, bottom = monitor_rect
        border_x = get_resize_border_thickness(hwnd, horizontal=True)
        border_y = get_resize_border_thickness(hwnd, horizontal=False)
        fullscreen_rect = (left - border_x, top, right + border_x, bottom + border_y)

        if is_maximized(hwnd):
            # Dropping WS_MAXIMIZE reads to DWM as a restore, so the move to
            # fullscreen would animate; suppressing transitions keeps it as
            # instant as entering from a normal-state window.
            set_window_transitions_enabled(hwnd, enabled=False)
            try:
                strip_maximize_style(hwnd)
                set_outer_window_rect(hwnd, fullscreen_rect)
            finally:
                set_window_transitions_enabled(hwnd, enabled=True)
        else:
            set_outer_window_rect(hwnd, fullscreen_rect)

        set_shell_fullscreen_marker(hwnd, fullscreen=True)

    def exit(self, window: QWindow) -> None:
        placement = self._saved_placement
        if placement is None:
            return

        self._saved_placement = None
        hwnd = int(window.winId())

        self._restore_frame_chrome(hwnd)

        if placement.shows_maximized:
            # A real maximize keeps DWM's state in sync, so the next restore still
            # animates; suppressing transitions keeps this one instant.
            set_window_transitions_enabled(hwnd, enabled=False)
            try:
                maximize_window(hwnd)
            finally:
                set_window_transitions_enabled(hwnd, enabled=True)

            # Maximizing re-derived the placement from the poisoned monitor-rect
            # geometry; point the normal geometry back at the pre-fullscreen one.
            self._repin_normal_geometry(hwnd, placement.normal_rect)
        else:
            set_window_placement(hwnd, placement)
        refresh_window_frame(hwnd)

    def is_active(self, window: QWindow) -> bool:
        if self._saved_placement is None:
            return False

        # A minimized window parks off-screen; the fullscreen session survives it.
        hwnd = int(window.winId())
        if is_fullscreen(hwnd) or is_minimized(hwnd):
            return True

        # Visible but not covering the monitor: the OS ended the session behind our
        # back (Win+Up, snap, display change). The query deliberately retires the
        # session as a side effect: retire now, or the parked placement flips this
        # back to True on a later minimize.
        self._retire_abandoned_session(hwnd)
        return False

    def _retire_abandoned_session(self, hwnd: int) -> None:
        placement = self._saved_placement
        if placement is None:
            return

        self._saved_placement = None
        self._restore_frame_chrome(hwnd)

        # While fullscreen the window was in the restored style, so Windows tracked
        # the monitor rect as its normal geometry. Point it back at the pre-fullscreen
        # one, or a later restore-down yields a monitor-sized window. Only safe while
        # maximized: applying a placement to a restored window would move it.
        if is_maximized(hwnd):
            self._repin_normal_geometry(hwnd, placement.normal_rect)

    @staticmethod
    def _restore_frame_chrome(hwnd: int) -> None:
        set_shell_fullscreen_marker(hwnd, fullscreen=False)
        set_window_corners_rounded(hwnd, rounded=True)
        set_window_border_visible(hwnd, visible=True)

    @staticmethod
    def _repin_normal_geometry(hwnd: int, normal_rect: tuple[int, int, int, int]) -> None:
        placement = get_window_placement(hwnd)
        if placement is not None:
            set_window_placement(hwnd, placement._replace(normal_rect=normal_rect))
