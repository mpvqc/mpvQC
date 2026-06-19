# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, override

from mpvqc.services.platform.backend import PlatformBackend
from mpvqc.services.platform.linux.window_button_detector import WindowButtonDetector

if TYPE_CHECKING:
    from PySide6.QtGui import QGuiApplication, QWindow

    from mpvqc.services.platform.window_buttons import WindowButtonPreference


class LinuxWindowManagerPlatformBackend(PlatformBackend):
    def __init__(self) -> None:
        super().__init__()
        self._window_buttons = WindowButtonDetector()
        self._window_buttons.preference_changed.connect(self.window_button_preference_changed)
        self._window_buttons.detect()

    @property
    @override
    def root_qml_url(self) -> str:
        return "qrc:/qt/qml/MpvqcApplicationLinux.qml"

    @property
    @override
    def draws_own_shadow(self) -> bool:
        return False

    @property
    @override
    def draws_window_border(self) -> bool:
        return False

    @property
    @override
    def window_button_preference(self) -> WindowButtonPreference:
        return self._window_buttons.preference

    @override
    def configure_window(self, app: QGuiApplication, window: QWindow) -> None:
        # The window manager owns sizing and placement; nothing to set up here.
        pass
