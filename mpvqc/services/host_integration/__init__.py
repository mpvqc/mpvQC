# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import platform

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QGuiApplication

from .types import DEFAULT_WINDOW_BUTTON_PREFERENCE, OsBackend, WindowButtonPreference


class HostIntegrationService(QObject):
    DEFAULT_WINDOW_BUTTON_PREFERENCE = DEFAULT_WINDOW_BUTTON_PREFERENCE

    display_zoom_factor_changed = Signal(float)

    def __init__(self):
        super().__init__()
        self._impl = get_implementation()

        self._zoom_factor = None

        from mpvqc.utility import get_main_window

        QGuiApplication.primaryScreen().virtualGeometryChanged.connect(self._invalidate_zoom_factor)
        get_main_window().screenChanged.connect(self._invalidate_zoom_factor)

    def _invalidate_zoom_factor(self, *_) -> None:
        if (zoom_factor := self._impl.get_display_zoom_factor()) != self._zoom_factor:
            self._zoom_factor = zoom_factor
            self.display_zoom_factor_changed.emit(zoom_factor)

    @property
    def display_zoom_factor(self) -> float:
        if self._zoom_factor is None:
            self._invalidate_zoom_factor()
        # noinspection PyTypeChecker
        return self._zoom_factor

    def get_window_button_preference(self) -> WindowButtonPreference:
        return self._impl.get_window_button_preference()


def get_implementation() -> OsBackend:
    # fmt: off
    match platform.system():
        case "Windows":
            from .windows import WindowsBackend
            return WindowsBackend()
        case "Linux":
            from .linux import LinuxBackend
            return LinuxBackend()
        case _:
            raise NotImplementedError
    # fmt: on


__all__ = ["HostIntegrationService", "WindowButtonPreference"]
