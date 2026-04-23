# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
import os
import sys
import typing
from functools import cached_property

import inject
from PySide6.QtCore import QEvent, QObject, QRunnable, QThreadPool, Signal

from mpvqc.services.main_window import MainWindowService

from .window_buttons import DEFAULT_WINDOW_BUTTON_PREFERENCE, WindowButtonPreference, read_window_button_preference

logger = logging.getLogger(__name__)


class HostIntegrationService(QObject):
    _main_window = inject.attr(MainWindowService)

    display_zoom_factor_changed = Signal(float)
    window_button_preference_changed = Signal(object)

    def __init__(self, detect_configuration: bool = True) -> None:
        super().__init__()
        self._zoom_factor = 1.0
        self._window_button_preference = DEFAULT_WINDOW_BUTTON_PREFERENCE

        if detect_configuration:
            self._zoom_factor = self._main_window.display_zoom_factor
            self._window = self._main_window.window
            self._window.installEventFilter(self)
            self._detect_window_button_preference_async()

    def _detect_window_button_preference_async(self) -> None:
        def job() -> None:
            preference = read_window_button_preference()
            if preference != self._window_button_preference:
                self._window_button_preference = preference
                self.window_button_preference_changed.emit(preference)

        QThreadPool.globalInstance().start(QRunnable.create(job))

    @property
    def window_button_preference(self) -> WindowButtonPreference:
        return self._window_button_preference

    @typing.override
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.DevicePixelRatioChange:
            self._invalidate_zoom_factor()
        return False

    def _invalidate_zoom_factor(self) -> None:
        if (zoom_factor := self._main_window.display_zoom_factor) != self._zoom_factor:
            self._zoom_factor = zoom_factor
            self.display_zoom_factor_changed.emit(zoom_factor)

    @property
    def display_zoom_factor(self) -> float:
        return self._zoom_factor

    @cached_property
    def is_tiling_window_manager(self) -> bool:
        if sys.platform != "linux":
            return False
        return is_tiling_window_manager()


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
