# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6.QtGui import QGuiApplication, QWindow


class WindowIntegration(ABC):
    """Platform-specific native window configuration (chrome, resize, embedding)."""

    @abstractmethod
    def configure_for(self, app: QGuiApplication, window: QWindow) -> None:
        pass

    @abstractmethod
    def set_embedded_player_hwnd(self, win_id: int) -> None:
        pass


def select_window_integration() -> WindowIntegration:
    match sys.platform:
        case "win32":
            from mpvqc.services.platform.win.integration import WinWindowIntegration

            return WinWindowIntegration()
        case "linux":
            from mpvqc.services.platform.linux.integration import LinuxWindowIntegration

            return LinuxWindowIntegration()

    msg = f"Unsupported platform for window integration: {sys.platform}"
    raise ValueError(msg)
