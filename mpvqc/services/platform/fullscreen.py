# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from PySide6.QtCore import Qt

if TYPE_CHECKING:
    from PySide6.QtGui import QWindow


class FullscreenHandler(Protocol):
    def enter(self, window: QWindow) -> None: ...

    def exit(self, window: QWindow) -> None: ...

    def is_active(self, window: QWindow) -> bool: ...


class QtFullscreenHandler:
    """Enters and leaves fullscreen via Qt window states."""

    def enter(self, window: QWindow) -> None:
        # Keep the maximized flag set while fullscreen so leaving fullscreen returns
        # to maximized, instead of the compositor restoring the saved normal geometry.
        states = window.windowStates() | Qt.WindowState.WindowFullScreen
        window.setWindowStates(states)

    def exit(self, window: QWindow) -> None:
        states = window.windowStates() & ~Qt.WindowState.WindowFullScreen
        window.setWindowStates(states)

    def is_active(self, window: QWindow) -> bool:
        return bool(window.windowStates() & Qt.WindowState.WindowFullScreen)
