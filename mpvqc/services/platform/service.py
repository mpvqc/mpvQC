# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal

from .backend import select_platform_backend
from .window_buttons import WindowButtonPreference

if TYPE_CHECKING:
    from PySide6.QtGui import QGuiApplication, QWindow

    from .backend import PlatformBackend
    from .window_state import WindowStateSnapshot


class PlatformService(QObject):
    window_button_preference_changed = Signal(WindowButtonPreference)
    shadow_margin_changed = Signal(int)

    def __init__(self, backend: PlatformBackend | None = None) -> None:
        super().__init__()
        self._backend = backend or select_platform_backend()
        # Signal.__get__ is typed for QObject owners only, which the protocols cannot promise
        # pyrefly: ignore [no-matching-overload]
        self._backend.window_buttons.preference_changed.connect(self.window_button_preference_changed)
        # pyrefly: ignore [no-matching-overload]
        self._backend.surface.shadow_margin_changed.connect(self.shadow_margin_changed)

    @property
    def window_button_preference(self) -> WindowButtonPreference:
        return self._backend.window_buttons.preference

    @property
    def desktop_sizes_window(self) -> bool:
        return self._backend.desktop_sizes_window

    def minimize(self, window: QWindow) -> None:
        self._backend.window_state.minimize(window)

    def maximize(self, window: QWindow) -> None:
        self._backend.window_state.maximize(window)

    def show_normal(self, window: QWindow) -> None:
        self._backend.window_state.show_normal(window)

    def enter_fullscreen(self, window: QWindow) -> None:
        self._backend.window_state.enter_fullscreen(window)

    def exit_fullscreen(self, window: QWindow) -> None:
        self._backend.window_state.exit_fullscreen(window)

    def read_state(self, window: QWindow) -> WindowStateSnapshot:
        return self._backend.window_state.read_state(window)

    def shadow_margin(self, window: QWindow) -> int:
        return self._backend.surface.shadow_margin(window)

    def configure_window(self, app: QGuiApplication, window: QWindow) -> None:
        self._backend.window_configuration.configure_window(app, window)
        self._backend.window_reveal.install(app, window)

    def track_embedded_player(self, win_id: int) -> None:
        self._backend.embedded_player.track(win_id)
