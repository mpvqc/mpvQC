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
    from .fullscreen import FullscreenHandler


class PlatformService(QObject):
    window_button_preference_changed = Signal(WindowButtonPreference)

    def __init__(self, backend: PlatformBackend | None = None) -> None:
        super().__init__()
        self._backend = backend or select_platform_backend()
        # Signal.__get__ is typed for QObject owners only, which the protocol cannot promise
        # pyrefly: ignore [no-matching-overload]
        self._backend.window_buttons.preference_changed.connect(self.window_button_preference_changed)

    @property
    def window_button_preference(self) -> WindowButtonPreference:
        return self._backend.window_buttons.preference

    @property
    def root_qml_url(self) -> str:
        return self._backend.root_qml_url

    @property
    def draws_own_shadow(self) -> bool:
        return self._backend.draws_own_shadow

    @property
    def owns_window_geometry(self) -> bool:
        return self._backend.owns_window_geometry

    @property
    def fullscreen_handler(self) -> FullscreenHandler:
        return self._backend.fullscreen

    def configure_window(self, app: QGuiApplication, window: QWindow) -> None:
        self._backend.window_configuration.configure_window(app, window)
        self._backend.window_reveal.install(app, window)

    def track_embedded_player(self, win_id: int) -> None:
        self._backend.embedded_player.track(win_id)

    def apply_content_margins(self, margin: int) -> None:
        self._backend.content_margins.apply_content_margins(margin)
