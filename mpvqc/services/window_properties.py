# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import inject
from PySide6.QtCore import QObject, Qt, Signal, Slot

from .main_window import MainWindowService

if TYPE_CHECKING:
    from PySide6.QtGui import QWindow

logger = logging.getLogger(__name__)


class WindowPropertiesService(QObject):
    _main_window = inject.attr(MainWindowService)

    width_changed = Signal(int)
    height_changed = Signal(int)
    is_fullscreen_changed = Signal(bool)
    is_maximized_changed = Signal(bool)

    def __init__(
        self,
        parent: QObject | None = None,
        *,
        bind_window: bool = True,
        width: int = 0,
        height: int = 0,
    ) -> None:
        super().__init__(parent)

        self._width = width
        self._height = height
        self._is_fullscreen = False
        self._is_maximized = False
        self._window: QWindow | None = None

        if bind_window:
            window = self._main_window.window

            self._on_width_changed(window.width())
            self._on_height_changed(window.height())
            self._on_window_state_changed(window.windowState())
            window.widthChanged.connect(self._on_width_changed)
            window.heightChanged.connect(self._on_height_changed)
            window.windowStateChanged.connect(self._on_window_state_changed)

            self._window = window

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
    def screen_width(self) -> int:
        screen = self._window.screen() if self._window else None
        if not screen:
            logger.error("Primary screen is None - cannot determine available width")
            return 0
        return screen.geometry().width()

    @property
    def screen_height(self) -> int:
        screen = self._window.screen() if self._window else None
        if not screen:
            logger.error("Primary screen is None - cannot determine available height")
            return 0
        return screen.geometry().height()

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
