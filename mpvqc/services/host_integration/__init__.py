# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import platform
from dataclasses import dataclass
from typing import TYPE_CHECKING

from PySide6.QtCore import QEvent, QObject, Signal, Slot
from PySide6.QtGui import QScreen

if TYPE_CHECKING:
    from PySide6.QtGui import QWindow


@dataclass(frozen=True)
class WindowButtonPreference:
    minimize: bool
    maximize: bool
    close: bool


class ZoomFactorChangeEventListener(QObject):
    device_pixel_ratio_changed = Signal()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:  # noqa: ARG002
        if event.type() == QEvent.Type.DevicePixelRatioChange:
            self.device_pixel_ratio_changed.emit()
        return False


class HostIntegrationService(QObject):
    DEFAULT_WINDOW_BUTTON_PREFERENCE = WindowButtonPreference(minimize=True, maximize=True, close=True)

    display_zoom_factor_changed = Signal(float)
    refresh_rate_changed = Signal(float)

    def __init__(self):
        super().__init__()
        self._zoom_factor = get_display_zoom_factor()
        self._refresh_rate = get_refresh_rate()

        self._zoom_factor_change_listener = ZoomFactorChangeEventListener()
        self._zoom_factor_change_listener.device_pixel_ratio_changed.connect(self._invalidate_zoom_factor)

        from mpvqc.utility import get_main_window

        self._window: QWindow = get_main_window()
        self._window.installEventFilter(self._zoom_factor_change_listener)
        self._window.screenChanged.connect(self._on_screen_changed)

        self._screen: QScreen = self._window.screen()
        self._screen.refreshRateChanged.connect(self._invalidate_refresh_rate)

    @property
    def display_zoom_factor(self) -> float:
        return self._zoom_factor

    @Slot()
    def _invalidate_zoom_factor(self, *_) -> None:
        if (zoom_factor := get_display_zoom_factor()) != self._zoom_factor:
            self._zoom_factor = zoom_factor
            self.display_zoom_factor_changed.emit(zoom_factor)

    @property
    def refresh_rate(self) -> float:
        return self._refresh_rate

    @Slot(QScreen)
    def _on_screen_changed(self, screen: QScreen) -> None:
        self._screen.refreshRateChanged.disconnect(self._invalidate_refresh_rate)
        self._screen = screen
        self._screen.refreshRateChanged.connect(self._invalidate_refresh_rate)
        self._invalidate_refresh_rate()

    @Slot(float)
    def _invalidate_refresh_rate(self, *_) -> None:
        if (refresh_rate := get_refresh_rate()) != self._refresh_rate:
            self._refresh_rate = refresh_rate
            self.refresh_rate_changed.emit(refresh_rate)

    def get_window_button_preference(self) -> WindowButtonPreference:
        match platform.system():
            case "Windows":
                return self.DEFAULT_WINDOW_BUTTON_PREFERENCE
            case "Linux":
                return read_linux_window_button_preference()
            case _:
                raise NotImplementedError


def get_display_zoom_factor() -> float:
    from mpvqc.utility import get_main_window

    return get_main_window().devicePixelRatio()


def get_refresh_rate() -> float:
    from mpvqc.utility import get_main_window

    return get_main_window().screen().refreshRate()


def read_linux_window_button_preference() -> WindowButtonPreference:
    from mpvqc.services.host_integration.portals import SettingsPortal

    with SettingsPortal() as portal:
        layout = portal.read_one("org.gnome.desktop.wm.preferences", "button-layout")

    if layout is None:
        return WindowButtonPreference(minimize=True, maximize=True, close=True)

    buttons = layout.lower()
    return WindowButtonPreference(
        minimize="minimize" in buttons,
        maximize="maximize" in buttons,
        close="close" in buttons,
    )


__all__ = [
    "HostIntegrationService",
    "WindowButtonPreference",
]
