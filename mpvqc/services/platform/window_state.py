# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple, Protocol

from PySide6.QtCore import Qt

if TYPE_CHECKING:
    from PySide6.QtGui import QWindow


class WindowStateSnapshot(NamedTuple):
    """Both window-state flags, taken in one read.

    `is_maximized` reports the logical state: the state the window returns
    to, even while it is minimized or fullscreen covers it."""

    is_fullscreen: bool
    is_maximized: bool


class WindowStateHandler(Protocol):
    """Drives every window-state change and answers reads about it, so platform
    quirks stay out of the shared services."""

    def minimize(self, window: QWindow) -> None: ...

    def maximize(self, window: QWindow) -> None: ...

    def show_normal(self, window: QWindow) -> None: ...

    def enter_fullscreen(self, window: QWindow) -> None: ...

    def exit_fullscreen(self, window: QWindow) -> None: ...

    def read_state(self, window: QWindow) -> WindowStateSnapshot: ...

    def sizes_own_window(self, window: QWindow) -> bool:
        """Whether the app decides this window's size, rather than a tiling
        desktop deciding it."""
        ...


class QtWindowStateHandler:
    """Requests window states through Qt for platforms whose window system
    honors them directly."""

    def __init__(self, *, sizes_own_window: bool) -> None:
        self._sizes_own_window = sizes_own_window

    def minimize(self, window: QWindow) -> None:
        # Keep the other state bits: replacing the set would drop Maximized,
        # and the window would restore to its normal geometry instead of
        # maximized.
        states = window.windowStates() | Qt.WindowState.WindowMinimized
        window.setWindowStates(states)

    def maximize(self, window: QWindow) -> None:
        window.setWindowStates(Qt.WindowState.WindowMaximized)

    def show_normal(self, window: QWindow) -> None:
        window.setWindowStates(Qt.WindowState.WindowNoState)

    def enter_fullscreen(self, window: QWindow) -> None:
        # Keep the maximized flag set while fullscreen so leaving fullscreen returns
        # to maximized, instead of the compositor restoring the saved normal geometry.
        states = window.windowStates() | Qt.WindowState.WindowFullScreen
        window.setWindowStates(states)

    def exit_fullscreen(self, window: QWindow) -> None:
        states = window.windowStates() & ~Qt.WindowState.WindowFullScreen
        window.setWindowStates(states)

    def read_state(self, window: QWindow) -> WindowStateSnapshot:
        states = window.windowStates()
        return WindowStateSnapshot(
            is_fullscreen=bool(states & Qt.WindowState.WindowFullScreen),
            is_maximized=bool(states & Qt.WindowState.WindowMaximized),
        )

    def sizes_own_window(self, window: QWindow) -> bool:  # noqa: ARG002
        return self._sizes_own_window
