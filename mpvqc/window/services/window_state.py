# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple, Protocol

from PySide6.QtCore import Qt

if TYPE_CHECKING:
    from PySide6.QtGui import QWindow


class WindowStateSnapshot(NamedTuple):
    is_fullscreen: bool
    is_maximized: bool


class WindowStateHandler(Protocol):
    def minimize(self, window: QWindow) -> None: ...

    def maximize(self, window: QWindow) -> None: ...

    def show_normal(self, window: QWindow) -> None: ...

    def enter_fullscreen(self, window: QWindow) -> None: ...

    def exit_fullscreen(self, window: QWindow) -> None: ...

    def read_state(self, window: QWindow) -> WindowStateSnapshot: ...


class QtWindowStateHandler:
    def minimize(self, window: QWindow) -> None:
        # Keep the other state bits deliberately
        states = window.windowStates() | Qt.WindowState.WindowMinimized
        window.setWindowStates(states)

    def maximize(self, window: QWindow) -> None:
        window.setWindowStates(Qt.WindowState.WindowMaximized)

    def show_normal(self, window: QWindow) -> None:
        window.setWindowStates(Qt.WindowState.WindowNoState)

    def enter_fullscreen(self, window: QWindow) -> None:
        # Keep the other state bits deliberately
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
