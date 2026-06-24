# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
import sys
from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal

from .window_buttons import DEFAULT_WINDOW_BUTTON_PREFERENCE, WindowButtonPreference

if TYPE_CHECKING:
    from PySide6.QtGui import QGuiApplication, QWindow

logger = logging.getLogger(__name__)


class PlatformBackend(QObject):
    window_button_preference_changed = Signal(WindowButtonPreference)

    @property
    def root_qml_url(self) -> str:
        raise NotImplementedError

    @property
    def draws_own_shadow(self) -> bool:
        raise NotImplementedError

    @property
    def draws_window_border(self) -> bool:
        raise NotImplementedError

    @property
    def owns_window_geometry(self) -> bool:
        return False

    @property
    def window_button_preference(self) -> WindowButtonPreference:
        return DEFAULT_WINDOW_BUTTON_PREFERENCE

    def configure_window(self, app: QGuiApplication, window: QWindow) -> None:
        raise NotImplementedError

    def set_embedded_player_hwnd(self, win_id: int) -> None:
        pass

    def apply_content_margins(self, margin: int) -> None:
        pass


def select_platform_backend() -> PlatformBackend:
    match sys.platform:
        case "win32":
            from .win.backend import WindowsPlatformBackend

            backend = WindowsPlatformBackend()
        case "linux":
            backend = _select_linux_backend()
        case _:
            msg = f"Unsupported platform for window integration: {sys.platform}"
            raise NotImplementedError(msg)

    logger.info("Using platform backend: %s", type(backend).__name__)
    return backend


def _select_linux_backend() -> PlatformBackend:
    from .linux.desktop_backend import LinuxDesktopPlatformBackend
    from .linux.tiling import is_tiling_window_manager
    from .linux.window_manager_backend import LinuxWindowManagerPlatformBackend

    if is_tiling_window_manager():
        return LinuxWindowManagerPlatformBackend()
    return LinuxDesktopPlatformBackend()
