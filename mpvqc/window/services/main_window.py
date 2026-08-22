# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, override

import inject
from PySide6.QtCore import QEvent, QObject, Signal, Slot
from PySide6.QtGui import QGuiApplication, QWindow

from .platform import PlatformService

if TYPE_CHECKING:
    from collections.abc import Callable

    from PySide6.QtGui import QScreen


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class MainWindowInputs:
    surface_width: int
    surface_height: int
    drop_shadow_margin: int
    is_fullscreen: bool
    is_maximized: bool
    is_main_window_focused: bool
    display_zoom_factor: float


@dataclass(frozen=True)
class MainWindowProps:
    drop_shadow_margin: int
    window_geometry_width: int
    window_geometry_height: int
    is_fullscreen: bool
    is_maximized: bool
    is_main_window_focused: bool
    display_zoom_factor: float


def derive_main_window_props(inputs: MainWindowInputs) -> MainWindowProps:
    return MainWindowProps(
        drop_shadow_margin=inputs.drop_shadow_margin,
        window_geometry_width=inputs.surface_width - 2 * inputs.drop_shadow_margin,
        window_geometry_height=inputs.surface_height - 2 * inputs.drop_shadow_margin,
        is_fullscreen=inputs.is_fullscreen,
        is_maximized=inputs.is_maximized,
        is_main_window_focused=inputs.is_main_window_focused,
        display_zoom_factor=inputs.display_zoom_factor,
    )


class MainWindowService(QObject):
    _platform = inject.attr(PlatformService)

    window_geometry_width_changed = Signal(int)
    window_geometry_height_changed = Signal(int)
    drop_shadow_margin_changed = Signal(int)
    is_fullscreen_changed = Signal(bool)
    is_maximized_changed = Signal(bool)
    is_main_window_focused_changed = Signal(bool)
    display_zoom_factor_changed = Signal(float)

    def __init__(self) -> None:
        super().__init__()
        self._window: QWindow | None = None
        self._zoom_monitor: _DisplayZoomMonitor | None = None
        self._inputs = MainWindowInputs(
            surface_width=0,
            surface_height=0,
            drop_shadow_margin=0,
            is_fullscreen=False,
            is_maximized=False,
            is_main_window_focused=True,
            display_zoom_factor=1.0,
        )
        self._props = derive_main_window_props(self._inputs)

    def initialize(self, window: QWindow) -> None:
        app = QGuiApplication.instance()
        if not isinstance(app, QGuiApplication):
            logger.error("fatal: cannot bind to QGuiApplication.instance()")
            return

        self._window = window
        self._platform.configure_window(app, window)

        state = self._platform.read_state(window)
        self._update(
            MainWindowInputs(
                surface_width=window.width(),
                surface_height=window.height(),
                drop_shadow_margin=self._platform.drop_shadow_margin(window),
                is_fullscreen=state.is_fullscreen,
                is_maximized=state.is_maximized,
                is_main_window_focused=_is_main_window_focused(window, app.focusWindow()),
                display_zoom_factor=window.devicePixelRatio(),
            )
        )

        self._platform.drop_shadow_margin_changed.connect(self._fold_drop_shadow_margin)
        window.widthChanged.connect(self._fold_surface_width)
        window.heightChanged.connect(self._fold_surface_height)
        # Moving without resizing (keyboard move via the system menu) can also take
        # the window out of fullscreen without any window state event.
        window.xChanged.connect(self._fold_window_state)
        window.yChanged.connect(self._fold_window_state)
        window.windowStateChanged.connect(self._fold_window_state)
        app.focusWindowChanged.connect(self._fold_focus_window)

        self._zoom_monitor = zoom_monitor = _DisplayZoomMonitor(window, self._fold_display_zoom_factor)
        window.installEventFilter(zoom_monitor)

        logger.debug("Wired up main window service")

    def install_event_filter(self, event_filter: QObject) -> None:
        self._active_window.installEventFilter(event_filter)

    def show(self) -> None:
        self._active_window.setVisible(True)

    def show_fullscreen(self) -> None:
        self._platform.enter_fullscreen(self._active_window)
        self._fold_window_state()

    def exit_fullscreen(self) -> None:
        self._platform.exit_fullscreen(self._active_window)
        self._fold_window_state()

    def show_maximized(self) -> None:
        self._platform.maximize(self._active_window)

    def show_normal(self) -> None:
        self._platform.show_normal(self._active_window)

    def minimize(self) -> None:
        self._platform.minimize(self._active_window)

    @property
    def _active_window(self) -> QWindow:
        if self._window is None:
            msg = "MainWindowService.initialize() has not been called yet"
            raise RuntimeError(msg)
        return self._window

    @property
    def window_geometry_width(self) -> int:
        return self._props.window_geometry_width

    @property
    def window_geometry_height(self) -> int:
        return self._props.window_geometry_height

    @property
    def drop_shadow_margin(self) -> int:
        return self._props.drop_shadow_margin

    @property
    def is_fullscreen(self) -> bool:
        return self._props.is_fullscreen

    @property
    def is_maximized(self) -> bool:
        return self._props.is_maximized

    @property
    def is_main_window_focused(self) -> bool:
        return self._props.is_main_window_focused

    @property
    def display_zoom_factor(self) -> float:
        return self._props.display_zoom_factor

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
    def _fold_surface_width(self, width: int) -> None:
        # The OS can take the window out of fullscreen through geometry alone
        # (snapping, display scale changes), without any window state event.
        state = self._platform.read_state(self._active_window)
        self._update(
            replace(
                self._inputs,
                surface_width=width,
                is_fullscreen=state.is_fullscreen,
                is_maximized=state.is_maximized,
            )
        )

    @Slot(int)
    def _fold_surface_height(self, height: int) -> None:
        state = self._platform.read_state(self._active_window)
        self._update(
            replace(
                self._inputs,
                surface_height=height,
                is_fullscreen=state.is_fullscreen,
                is_maximized=state.is_maximized,
            )
        )

    @Slot()
    def _fold_window_state(self) -> None:
        # The move signals refire this on every frame of a drag, and the re-read
        # almost always answers what the inputs already hold. On Windows the read
        # also retires an abandoned fullscreen session, which can re-enter here
        # before it returns, so it runs before the inputs are replaced.
        state = self._platform.read_state(self._active_window)
        inputs = replace(self._inputs, is_fullscreen=state.is_fullscreen, is_maximized=state.is_maximized)
        if inputs == self._inputs:
            return
        self._update(inputs)

    @Slot(int)
    def _fold_drop_shadow_margin(self, margin: int) -> None:
        self._update(replace(self._inputs, drop_shadow_margin=margin))

    @Slot(QWindow)
    def _fold_focus_window(self, focused: QWindow | None) -> None:
        is_focused = _is_main_window_focused(self._active_window, focused)
        self._update(replace(self._inputs, is_main_window_focused=is_focused))

    def _fold_display_zoom_factor(self, zoom_factor: float) -> None:
        self._update(replace(self._inputs, display_zoom_factor=zoom_factor))

    def _update(self, inputs: MainWindowInputs) -> None:
        self._inputs = inputs
        new, old = derive_main_window_props(inputs), self._props
        if new == old:
            return
        self._props = new
        if new.drop_shadow_margin != old.drop_shadow_margin:
            self.drop_shadow_margin_changed.emit(new.drop_shadow_margin)
        if new.window_geometry_width != old.window_geometry_width:
            self.window_geometry_width_changed.emit(new.window_geometry_width)
        if new.window_geometry_height != old.window_geometry_height:
            self.window_geometry_height_changed.emit(new.window_geometry_height)
        if new.is_fullscreen != old.is_fullscreen:
            self.is_fullscreen_changed.emit(new.is_fullscreen)
        if new.is_maximized != old.is_maximized:
            self.is_maximized_changed.emit(new.is_maximized)
        if new.is_main_window_focused != old.is_main_window_focused:
            self.is_main_window_focused_changed.emit(new.is_main_window_focused)
        if new.display_zoom_factor != old.display_zoom_factor:
            self.display_zoom_factor_changed.emit(new.display_zoom_factor)


def _is_main_window_focused(window: QWindow, focused: QWindow | None) -> bool:
    return focused is window or (focused is not None and not focused.isVisible())


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
