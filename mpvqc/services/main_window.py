# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, override

import inject
from PySide6.QtCore import QEvent, QObject, Qt, Signal, Slot
from PySide6.QtGui import QGuiApplication, QWindow

from .platform import PlatformService

if TYPE_CHECKING:
    from collections.abc import Callable

    from PySide6.QtGui import QScreen


logger = logging.getLogger(__name__)

# Transparent padding the self-drawn drop shadow lives in. Must exceed the
# widest shadow blur + offset, otherwise the soft edge clips at the surface.
_SHADOW_MARGIN = 88


class MainWindowService(QObject):
    _platform = inject.attr(PlatformService)

    content_width_changed = Signal(int)
    content_height_changed = Signal(int)
    shadow_margin_changed = Signal(int)
    is_fullscreen_changed = Signal(bool)
    is_maximized_changed = Signal(bool)
    is_main_window_focused_changed = Signal(bool)
    display_zoom_factor_changed = Signal(float)

    def __init__(self) -> None:
        super().__init__()
        self._window: QWindow | None = None
        self._zoom_monitor: _DisplayZoomMonitor | None = None
        self._outer_width = 0
        self._outer_height = 0
        self._shadow_margin = 0
        self._is_fullscreen = False
        self._is_maximized = False
        self._is_main_window_focused = True
        self._zoom_factor = 1.0

    def initialize(self, window: QWindow) -> None:
        app = QGuiApplication.instance()
        if not isinstance(app, QGuiApplication):
            logger.error("fatal: cannot bind to QGuiApplication.instance()")
            return

        self._window = window

        self._outer_width = window.width()
        self._outer_height = window.height()
        self._apply_window_state()
        self._on_focus_window_changed(app.focusWindow())

        self._zoom_factor = window.devicePixelRatio()
        self._platform.configure_window(app, window)

        # Sync QML bindings that were created during engine.load(), before the window
        # size was known. Margin first: content size reads it.
        self._refresh_shadow_margin()
        self.content_width_changed.emit(self.content_width)
        self.content_height_changed.emit(self.content_height)

        window.widthChanged.connect(self._on_width_changed)
        window.heightChanged.connect(self._on_height_changed)
        window.xChanged.connect(self._on_position_changed)
        window.yChanged.connect(self._on_position_changed)
        window.windowStateChanged.connect(self._on_window_state_changed)
        app.focusWindowChanged.connect(self._on_focus_window_changed)

        self._zoom_monitor = zoom_monitor = _DisplayZoomMonitor(window, self._on_zoom_factor_changed)
        window.installEventFilter(zoom_monitor)

        logger.debug("Wired up main window service")

    def install_event_filter(self, event_filter: QObject) -> None:
        self._active_window.installEventFilter(event_filter)

    def show(self) -> None:
        self._active_window.setVisible(True)

    def show_fullscreen(self) -> None:
        self._platform.enter_fullscreen(self._active_window)
        self._sync_window_state()

    def exit_fullscreen(self) -> None:
        self._platform.exit_fullscreen(self._active_window)
        self._sync_window_state()

    def show_maximized(self) -> None:
        self._active_window.setWindowStates(Qt.WindowState.WindowMaximized)

    def show_normal(self) -> None:
        self._active_window.setWindowStates(Qt.WindowState.WindowNoState)

    @property
    def _active_window(self) -> QWindow:
        if self._window is None:
            msg = "MainWindowService.initialize() has not been called yet"
            raise RuntimeError(msg)
        return self._window

    @property
    def content_width(self) -> int:
        return self._outer_width - 2 * self._shadow_margin

    @property
    def content_height(self) -> int:
        return self._outer_height - 2 * self._shadow_margin

    @property
    def shadow_margin(self) -> int:
        return self._shadow_margin

    @property
    def is_fullscreen(self) -> bool:
        return self._is_fullscreen

    @property
    def is_maximized(self) -> bool:
        return self._is_maximized

    @property
    def is_main_window_focused(self) -> bool:
        return self._is_main_window_focused

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

    def _compute_shadow_margin(self) -> int:
        if not self._platform.draws_own_shadow:
            return 0
        if self._is_fullscreen or self._is_maximized:
            return 0
        return _SHADOW_MARGIN

    @Slot(int)
    def _on_width_changed(self, width: int) -> None:
        if width == self._outer_width:
            return
        previous = self.content_width
        self._outer_width = width
        if self.content_width != previous:
            self.content_width_changed.emit(self.content_width)
        # The OS can take the window out of fullscreen through geometry alone
        # (snapping, display scale changes), without any window state event.
        self._apply_window_state()

    @Slot(int)
    def _on_height_changed(self, height: int) -> None:
        if height == self._outer_height:
            return
        previous = self.content_height
        self._outer_height = height
        if self.content_height != previous:
            self.content_height_changed.emit(self.content_height)
        self._apply_window_state()

    @Slot(int)
    def _on_position_changed(self, _: int) -> None:
        # Moving without resizing (keyboard move via the system menu) can also take
        # the window out of fullscreen without any window state event.
        self._apply_window_state()

    @Slot(Qt.WindowState)
    def _on_window_state_changed(self, _state: Qt.WindowState) -> None:
        self._sync_window_state()

    def _sync_window_state(self) -> None:
        self._apply_window_state()
        self._refresh_shadow_margin()

    def _apply_window_state(self) -> None:
        window = self._active_window
        is_fullscreen = self._platform.is_fullscreen(window)

        # While fullscreen the OS-level maximized state is parked (Windows drops the
        # style bit), so keep reporting the value from before entering.
        if is_fullscreen:
            is_maximized = self._is_maximized
        else:
            is_maximized = bool(window.windowStates() & Qt.WindowState.WindowMaximized)

        if is_fullscreen != self._is_fullscreen:
            self._is_fullscreen = is_fullscreen
            self.is_fullscreen_changed.emit(is_fullscreen)

        if is_maximized != self._is_maximized:
            self._is_maximized = is_maximized
            self.is_maximized_changed.emit(is_maximized)

    def _refresh_shadow_margin(self) -> None:
        margin = self._compute_shadow_margin()
        if margin == self._shadow_margin:
            return

        previous_width = self.content_width
        previous_height = self.content_height
        self._shadow_margin = margin
        self._platform.apply_content_margins(margin)
        self.shadow_margin_changed.emit(margin)

        if self.content_width != previous_width:
            self.content_width_changed.emit(self.content_width)
        if self.content_height != previous_height:
            self.content_height_changed.emit(self.content_height)

    def _on_zoom_factor_changed(self, zoom_factor: float) -> None:
        if zoom_factor != self._zoom_factor:
            self._zoom_factor = zoom_factor
            self.display_zoom_factor_changed.emit(zoom_factor)

    @Slot(QWindow)
    def _on_focus_window_changed(self, focused: QWindow | None) -> None:
        is_focused = focused is self._window or (focused is not None and not focused.isVisible())
        if is_focused != self._is_main_window_focused:
            self._is_main_window_focused = is_focused
            self.is_main_window_focused_changed.emit(is_focused)


class _DisplayZoomMonitor(QObject):
    def __init__(self, window: QWindow, on_change: Callable[[float], None]) -> None:
        super().__init__()
        self._window = window
        self._on_change = on_change
        self._last = window.devicePixelRatio()

    @override
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.DevicePixelRatioChange:
            current = self._window.devicePixelRatio()
            if current != self._last:
                self._last = current
                self._on_change(current)
        return False
