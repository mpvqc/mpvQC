# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import sys
import typing
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6.QtGui import QGuiApplication, QWindow


class FramelessWindowService(ABC):
    """Service for managing frameless window behavior across different platforms."""

    @abstractmethod
    def configure_for(self, app: QGuiApplication, window: QWindow, *, display_zoom_factor: float) -> None:
        pass

    @abstractmethod
    def set_embedded_player_hwnd(self, win_id: int) -> None:
        pass


class WinImplementation(FramelessWindowService):
    def __init__(self) -> None:
        from mpvqc.services.frameless.win import WindowsEventFilter

        self._event_filter = WindowsEventFilter()

    @typing.override
    def configure_for(self, app: QGuiApplication, window: QWindow, *, display_zoom_factor: float) -> None:
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

        width = int(1280 * display_zoom_factor)
        height = int(720 * display_zoom_factor)
        set_outer_window_size(hwnd_top_lvl, width, height)

    @typing.override
    def set_embedded_player_hwnd(self, win_id: int) -> None:
        self._event_filter.set_embedded_player_hwnd(win_id)


class LinuxImplementation(FramelessWindowService):
    @typing.override
    def configure_for(self, app: QGuiApplication, window: QWindow, *, display_zoom_factor: float) -> None:
        from mpvqc.services.frameless.linux import LinuxEventFilter

        self._event_filter = LinuxEventFilter(window, app)
        app.installEventFilter(self._event_filter)

    @typing.override
    def set_embedded_player_hwnd(self, win_id: int) -> None:
        pass


def get_frameless_window_service() -> FramelessWindowService:
    match sys.platform:
        case "win32":
            return WinImplementation()
        case "linux":
            return LinuxImplementation()

    msg = f"Cannot configure frameless window on platform: {sys.platform}"
    raise ValueError(msg)
