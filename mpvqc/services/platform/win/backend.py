# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, override

from mpvqc.services.platform.backend import PlatformBackend
from mpvqc.services.platform.win import (
    WindowsEventFilter,
    configure_gwl_style,
    extend_frame_into_client_area,
    set_outer_window_size,
)

if TYPE_CHECKING:
    from PySide6.QtGui import QGuiApplication, QWindow


class WindowsPlatformBackend(PlatformBackend):
    def __init__(self) -> None:
        super().__init__()
        self._event_filter = WindowsEventFilter()

    @property
    @override
    def root_qml_url(self) -> str:
        return "qrc:/qt/qml/MpvqcApplicationWindows.qml"

    @property
    @override
    def draws_own_shadow(self) -> bool:
        # Windows keeps the native DWM frame and its own shadow.
        return False

    @property
    @override
    def draws_window_border(self) -> bool:
        # Leave space to let Windows draw its custom border.
        return True

    @override
    def configure_window(self, app: QGuiApplication, window: QWindow) -> None:
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
