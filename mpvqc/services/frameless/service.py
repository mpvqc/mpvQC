# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import platform
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import inject

from ..host_integration import HostIntegrationService  # noqa: TID252

if TYPE_CHECKING:
    from PySide6.QtGui import QGuiApplication, QWindow


class FramelessWindowService(ABC):
    """Service for managing frameless window behavior across different platforms."""

    @abstractmethod
    def configure_for(self, app: QGuiApplication, window: QWindow) -> None:
        pass

    @abstractmethod
    def set_embedded_player_hwnd(self, win_id: int) -> None:
        pass


class WinImplementation(FramelessWindowService):
    host_integration: HostIntegrationService = inject.attr(HostIntegrationService)

    def __init__(self):
        from mpvqc.services.frameless.win import WindowsEventFilter

        self._event_filter = WindowsEventFilter()

    def configure_for(self, app: QGuiApplication, window: QWindow) -> None:
        hwnd_top_lvl = window.winId()
        self._event_filter.set_top_lvl_hwnd(hwnd_top_lvl)
        app.installNativeEventFilter(self._event_filter)

        from mpvqc.services.frameless.win import (
            configure_gwl_style,
            extend_frame_into_client_area,
            set_outer_window_size,
        )

        extend_frame_into_client_area(hwnd_top_lvl)
        configure_gwl_style(hwnd_top_lvl)

        width = int(1280 * self.host_integration.display_zoom_factor)
        height = int(720 * self.host_integration.display_zoom_factor)
        set_outer_window_size(hwnd_top_lvl, width, height)

    def set_embedded_player_hwnd(self, win_id: int) -> None:
        self._event_filter.set_embedded_player_hwnd(win_id)


class LinuxImplementation(FramelessWindowService):
    def configure_for(self, app: QGuiApplication, window: QWindow) -> None:
        from mpvqc.services.frameless.linux import LinuxEventFilter

        self._event_filter = LinuxEventFilter(window, app)
        app.installEventFilter(self._event_filter)

    def set_embedded_player_hwnd(self, win_id: int) -> None:
        pass


def get_frameless_window_service() -> FramelessWindowService:
    match platform.system():
        case "Windows":
            return WinImplementation()
        case "Linux":
            return LinuxImplementation()
        case system:
            msg = f"Cannot configure frameless window on platform: {system}"
            raise ValueError(msg)
