# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from PySide6.QtCore import QObject, Qt, Signal
from PySide6.QtGui import QScreen


class WindowPropertiesService(QObject):
    width_changed = Signal(int)
    height_changed = Signal(int)
    is_fullscreen_changed = Signal(bool)
    is_maximized_changed = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._width = 0
        self._height = 0
        self._is_fullscreen = False
        self._is_maximized = False

        from mpvqc.utility import get_main_window

        self._window = get_main_window()

        self._on_width_changed(self._window.width())
        self._on_height_changed(self._window.height())
        self._on_window_state_changed(self._window.windowState())

        self._window.widthChanged.connect(self._on_width_changed)
        self._window.heightChanged.connect(self._on_height_changed)
        self._window.windowStateChanged.connect(self._on_window_state_changed)

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def is_fullscreen(self) -> bool:
        return self._is_fullscreen

    @property
    def is_maximized(self) -> bool:
        return self._is_maximized

    @property
    def screen(self) -> QScreen:
        return self._window.screen()

    def _on_width_changed(self, width: int) -> None:
        if width != self._width:
            self._width = width
            self.width_changed.emit(width)

    def _on_height_changed(self, height: int) -> None:
        if height != self._height:
            self._height = height
            self.height_changed.emit(height)

    def _on_window_state_changed(self, state: Qt.WindowState) -> None:
        is_fullscreen = state == Qt.WindowState.WindowFullScreen
        is_maximized = state == Qt.WindowState.WindowMaximized

        if is_fullscreen != self._is_fullscreen:
            self._is_fullscreen = is_fullscreen
            self.is_fullscreen_changed.emit(is_fullscreen)

        if is_maximized != self._is_maximized:
            self._is_maximized = is_maximized
            self.is_maximized_changed.emit(is_maximized)
