# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import typing
from typing import TYPE_CHECKING

import inject
from PySide6.QtCore import QEvent, QObject, Qt, Signal, Slot
from PySide6.QtGui import QGuiApplication

from .frameless import FramelessWindowService

if TYPE_CHECKING:
    from collections.abc import Callable

    from PySide6.QtGui import QScreen, QWindow

MAIN_WINDOW_OBJECT_NAME = "MpvqcMainWindow"


class MainWindowService(QObject):
    _frameless = inject.attr(FramelessWindowService)

    width_changed = Signal(int)
    height_changed = Signal(int)
    is_fullscreen_changed = Signal(bool)
    is_maximized_changed = Signal(bool)
    display_zoom_factor_changed = Signal(float)

    def __init__(self) -> None:
        super().__init__()
        self._window: QWindow | None = None
        self._zoom_monitor: _DisplayZoomMonitor | None = None
        self._width = 0
        self._height = 0
        self._is_fullscreen = False
        self._is_maximized = False
        self._zoom_factor = 1.0

    def initialize(self, app: QGuiApplication) -> None:
        window = _find_main_window()

        self._zoom_factor = window.devicePixelRatio()
        self._width = window.width()
        self._height = window.height()

        state = window.windowState()
        self._is_fullscreen = state == Qt.WindowState.WindowFullScreen
        self._is_maximized = state == Qt.WindowState.WindowMaximized

        self._frameless.configure_for(app, window, display_zoom_factor=self._zoom_factor)

        window.widthChanged.connect(self._on_width_changed)
        window.heightChanged.connect(self._on_height_changed)
        window.windowStateChanged.connect(self._on_window_state_changed)

        zoom_monitor = _DisplayZoomMonitor(window, self._on_zoom_factor_changed)
        window.installEventFilter(zoom_monitor)

        self._zoom_monitor = zoom_monitor
        self._window = window

    def install_event_filter(self, event_filter: QObject) -> None:
        self._active_window.installEventFilter(event_filter)

    def show(self) -> None:
        self._active_window.setVisible(True)

    def show_fullscreen(self) -> None:
        self._active_window.showFullScreen()

    def show_maximized(self) -> None:
        self._active_window.showMaximized()

    def show_normal(self) -> None:
        self._active_window.showNormal()

    @property
    def _active_window(self) -> QWindow:
        if self._window is None:
            msg = "MainWindowService.initialize() has not been called yet"
            raise RuntimeError(msg)
        return self._window

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
    def display_zoom_factor(self) -> float:
        return self._zoom_factor

    @property
    def screen_width(self) -> int:
        return self._active_screen.geometry().width()

    @property
    def screen_height(self) -> int:
        return self._active_screen.geometry().height()

    @property
    def _active_screen(self) -> QScreen:
        screen = self._active_window.screen()
        if screen is None:
            msg = "Main window is not associated with a screen"
            raise RuntimeError(msg)
        return screen

    @Slot(int)
    def _on_width_changed(self, width: int) -> None:
        if width != self._width:
            self._width = width
            self.width_changed.emit(width)

    @Slot(int)
    def _on_height_changed(self, height: int) -> None:
        if height != self._height:
            self._height = height
            self.height_changed.emit(height)

    @Slot(Qt.WindowState)
    def _on_window_state_changed(self, state: Qt.WindowState) -> None:
        is_fullscreen = state == Qt.WindowState.WindowFullScreen
        is_maximized = state == Qt.WindowState.WindowMaximized

        if is_fullscreen != self._is_fullscreen:
            self._is_fullscreen = is_fullscreen
            self.is_fullscreen_changed.emit(is_fullscreen)

        if is_maximized != self._is_maximized:
            self._is_maximized = is_maximized
            self.is_maximized_changed.emit(is_maximized)

    def _on_zoom_factor_changed(self, zoom_factor: float) -> None:
        if zoom_factor != self._zoom_factor:
            self._zoom_factor = zoom_factor
            self.display_zoom_factor_changed.emit(zoom_factor)


class _DisplayZoomMonitor(QObject):
    def __init__(self, window: QWindow, on_change: Callable[[float], None]) -> None:
        super().__init__()
        self._window = window
        self._on_change = on_change
        self._last = window.devicePixelRatio()

    @typing.override
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.DevicePixelRatioChange:
            current = self._window.devicePixelRatio()
            if current != self._last:
                self._last = current
                self._on_change(current)
        return False


def _find_main_window() -> QWindow:
    for window in QGuiApplication.topLevelWindows():
        if window.objectName() == MAIN_WINDOW_OBJECT_NAME:
            return window
    msg = f"Could not find window with name: {MAIN_WINDOW_OBJECT_NAME}"
    raise ValueError(msg)
