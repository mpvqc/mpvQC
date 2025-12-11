# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
import os
import platform
from dataclasses import dataclass
from functools import cached_property

from PySide6.QtCore import QEvent, QObject, Signal, Slot

logger = logging.getLogger(__name__)


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

    def __init__(self):
        super().__init__()
        self._zoom_factor = get_display_zoom_factor()

        self._zoom_factor_change_listener = ZoomFactorChangeEventListener()
        self._zoom_factor_change_listener.device_pixel_ratio_changed.connect(self._invalidate_zoom_factor)

        from mpvqc.utility import get_main_window

        self._window = get_main_window()
        self._window.installEventFilter(self._zoom_factor_change_listener)

    @Slot()
    def _invalidate_zoom_factor(self, *_) -> None:
        if (zoom_factor := get_display_zoom_factor()) != self._zoom_factor:
            self._zoom_factor = zoom_factor
            self.display_zoom_factor_changed.emit(zoom_factor)

    @property
    def display_zoom_factor(self) -> float:
        return self._zoom_factor

    @cached_property
    def is_tiling_window_manager(self) -> bool:
        if platform.system() != "Linux":
            return False
        return is_tiling_window_manager()

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


def is_tiling_window_manager() -> bool:
    tiling_wms = {
        "awesome",
        "bspwm",
        "dwm",
        "herbstluftwm",
        "hyprland",
        "i3",
        "niri",
        "qtile",
        "river",
        "sway",
        "wlroots",
        "xmonad",
    }

    xdg_current_desktop = os.environ.get("XDG_CURRENT_DESKTOP", "")
    desktops = {d.lower() for d in xdg_current_desktop.split(":")}
    is_tiling_wm = bool(desktops & tiling_wms)

    if is_tiling_wm:
        logger.debug("Running on tiling window manager")

    return is_tiling_wm


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
