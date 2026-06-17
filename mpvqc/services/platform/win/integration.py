# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, override

from mpvqc.services.platform.win import (
    WindowsEventFilter,
    configure_gwl_style,
    extend_frame_into_client_area,
    set_outer_window_size,
)
from mpvqc.services.platform.window_integration import WindowIntegration

if TYPE_CHECKING:
    from PySide6.QtGui import QGuiApplication, QWindow


class WinWindowIntegration(WindowIntegration):
    def __init__(self) -> None:
        self._event_filter = WindowsEventFilter()

    @override
    def configure_for(self, app: QGuiApplication, window: QWindow) -> None:
        hwnd_top_lvl = window.winId()
        self._event_filter.set_top_lvl_hwnd(hwnd_top_lvl)
        app.installNativeEventFilter(self._event_filter)

        extend_frame_into_client_area(hwnd_top_lvl)
        configure_gwl_style(hwnd_top_lvl)

        zoom = window.devicePixelRatio()
        width = int(1280 * zoom)
        height = int(720 * zoom)
        set_outer_window_size(hwnd_top_lvl, width, height)

    @override
    def set_embedded_player_hwnd(self, win_id: int) -> None:
        self._event_filter.set_embedded_player_hwnd(win_id)

    @override
    def apply_content_margins(self, margin: int) -> None:
        # Windows keeps the real window rect via the DWM frame; no inset needed.
        pass
