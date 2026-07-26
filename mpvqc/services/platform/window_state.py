# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from PySide6.QtCore import Qt

from .content_margins import NoContentMarginsApplier

if TYPE_CHECKING:
    from PySide6.QtGui import QWindow

    from .content_margins import ContentMarginsApplier


class WindowStateHandler(Protocol):
    """Drives every window-state change and answers the state reads, so
    platform quirks stay in platform code and out of shared services.

    `is_maximized` reports the logical state: the state the window returns
    to, even while fullscreen covers it."""

    def minimize(self, window: QWindow) -> None: ...

    def maximize(self, window: QWindow) -> None: ...

    def show_normal(self, window: QWindow) -> None: ...

    def enter_fullscreen(self, window: QWindow) -> None: ...

    def exit_fullscreen(self, window: QWindow) -> None: ...

    def is_fullscreen(self, window: QWindow) -> bool: ...

    def is_maximized(self, window: QWindow) -> bool: ...

    def shadow_margin(self, window: QWindow) -> int: ...

    def apply_content_margins(self, margin: int) -> None: ...


class QtWindowStateHandler:
    """Requests window states through Qt for platforms whose window system
    honors them directly."""

    def __init__(self, *, shadow_margin: int = 0, margins_applier: ContentMarginsApplier | None = None) -> None:
        self._shadow_margin = shadow_margin
        self._margins_applier = margins_applier if margins_applier is not None else NoContentMarginsApplier()

    def minimize(self, window: QWindow) -> None:
        # Keep the other state bits while minimized. Replacing the set would
        # drop the Maximized bit, and the window system would restore the
        # window to its normal geometry instead of maximized.
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

    def is_fullscreen(self, window: QWindow) -> bool:
        return bool(window.windowStates() & Qt.WindowState.WindowFullScreen)

    def is_maximized(self, window: QWindow) -> bool:
        return bool(window.windowStates() & Qt.WindowState.WindowMaximized)

    def shadow_margin(self, window: QWindow) -> int:
        if self.is_fullscreen(window) or self.is_maximized(window):
            return 0
        return self._shadow_margin

    def apply_content_margins(self, margin: int) -> None:
        self._margins_applier.apply_content_margins(margin)
