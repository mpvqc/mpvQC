# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass, replace

import inject
from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.window.services import MainWindowService, PlatformService

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1

_WINDOW_RADIUS = 8


@dataclass(frozen=True)
class WindowControlsInputs:
    window_geometry_width: int
    window_geometry_height: int
    is_fullscreen: bool
    is_maximized: bool
    drop_shadow_margin: int
    is_main_window_focused: bool
    keeps_native_frame: bool
    draws_drop_shadow: bool


@dataclass(frozen=True)
class WindowControlsProps:
    window_geometry_width: int
    window_geometry_height: int
    is_fullscreen: bool
    is_maximized: bool
    drop_shadow_margin: int
    radius: int
    is_main_window_focused: bool
    keeps_native_frame: bool
    draws_drop_shadow: bool


def derive_window_controls_props(inputs: WindowControlsInputs) -> WindowControlsProps:
    return WindowControlsProps(
        window_geometry_width=inputs.window_geometry_width,
        window_geometry_height=inputs.window_geometry_height,
        is_fullscreen=inputs.is_fullscreen,
        is_maximized=inputs.is_maximized,
        drop_shadow_margin=inputs.drop_shadow_margin,
        radius=_WINDOW_RADIUS if inputs.drop_shadow_margin > 0 else 0,
        is_main_window_focused=inputs.is_main_window_focused,
        keeps_native_frame=inputs.keeps_native_frame,
        draws_drop_shadow=inputs.draws_drop_shadow,
    )


@QmlElement
class MpvqcWindowControlsViewModel(QObject):
    _main_window = inject.attr(MainWindowService)
    _platform = inject.attr(PlatformService)

    windowGeometryWidthChanged = Signal(int)
    windowGeometryHeightChanged = Signal(int)
    isFullscreenChanged = Signal(bool)
    isMaximizedChanged = Signal(bool)
    dropShadowMarginChanged = Signal(int)
    radiusChanged = Signal(int)
    isMainWindowFocusedChanged = Signal(bool)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        main_window = self._main_window
        self._inputs = WindowControlsInputs(
            window_geometry_width=main_window.window_geometry_width,
            window_geometry_height=main_window.window_geometry_height,
            is_fullscreen=main_window.is_fullscreen,
            is_maximized=main_window.is_maximized,
            drop_shadow_margin=main_window.drop_shadow_margin,
            is_main_window_focused=main_window.is_main_window_focused,
            keeps_native_frame=self._platform.keeps_native_frame,
            draws_drop_shadow=self._platform.draws_drop_shadow,
        )
        self._props = derive_window_controls_props(self._inputs)

        main_window.window_geometry_width_changed.connect(self._fold_window_geometry_width)
        main_window.window_geometry_height_changed.connect(self._fold_window_geometry_height)
        main_window.is_fullscreen_changed.connect(self._fold_is_fullscreen)
        main_window.is_maximized_changed.connect(self._fold_is_maximized)
        main_window.drop_shadow_margin_changed.connect(self._fold_drop_shadow_margin)
        main_window.is_main_window_focused_changed.connect(self._fold_is_main_window_focused)

    @Slot(int)
    def _fold_window_geometry_width(self, value: int) -> None:
        self._update(replace(self._inputs, window_geometry_width=value))

    @Slot(int)
    def _fold_window_geometry_height(self, value: int) -> None:
        self._update(replace(self._inputs, window_geometry_height=value))

    @Slot(bool)
    def _fold_is_fullscreen(self, value: bool) -> None:
        self._update(replace(self._inputs, is_fullscreen=value))

    @Slot(bool)
    def _fold_is_maximized(self, value: bool) -> None:
        self._update(replace(self._inputs, is_maximized=value))

    @Slot(int)
    def _fold_drop_shadow_margin(self, value: int) -> None:
        self._update(replace(self._inputs, drop_shadow_margin=value))

    @Slot(bool)
    def _fold_is_main_window_focused(self, value: bool) -> None:
        self._update(replace(self._inputs, is_main_window_focused=value))

    def _update(self, inputs: WindowControlsInputs) -> None:
        self._inputs = inputs
        new, old = derive_window_controls_props(self._inputs), self._props
        if new == old:
            return
        self._props = new
        if new.window_geometry_width != old.window_geometry_width:
            self.windowGeometryWidthChanged.emit(new.window_geometry_width)
        if new.window_geometry_height != old.window_geometry_height:
            self.windowGeometryHeightChanged.emit(new.window_geometry_height)
        if new.is_fullscreen != old.is_fullscreen:
            self.isFullscreenChanged.emit(new.is_fullscreen)
        if new.is_maximized != old.is_maximized:
            self.isMaximizedChanged.emit(new.is_maximized)
        if new.drop_shadow_margin != old.drop_shadow_margin:
            self.dropShadowMarginChanged.emit(new.drop_shadow_margin)
        if new.radius != old.radius:
            self.radiusChanged.emit(new.radius)
        if new.is_main_window_focused != old.is_main_window_focused:
            self.isMainWindowFocusedChanged.emit(new.is_main_window_focused)

    @Property(int, notify=windowGeometryWidthChanged)
    def windowGeometryWidth(self) -> int:
        return self._props.window_geometry_width

    @Property(int, notify=windowGeometryHeightChanged)
    def windowGeometryHeight(self) -> int:
        return self._props.window_geometry_height

    @Property(bool, notify=isFullscreenChanged)
    def isFullscreen(self) -> bool:
        return self._props.is_fullscreen

    @Property(bool, notify=isMaximizedChanged)
    def isMaximized(self) -> bool:
        return self._props.is_maximized

    @Property(int, notify=dropShadowMarginChanged)
    def dropShadowMargin(self) -> int:
        return self._props.drop_shadow_margin

    @Property(int, notify=radiusChanged)
    def radius(self) -> int:
        return self._props.radius

    @Property(bool, notify=isMainWindowFocusedChanged)
    def isMainWindowFocused(self) -> bool:
        return self._props.is_main_window_focused

    @Property(bool, constant=True)
    def keepsNativeFrame(self) -> bool:
        return self._props.keeps_native_frame

    @Property(bool, constant=True)
    def drawsDropShadow(self) -> bool:
        return self._props.draws_drop_shadow

    @Slot()
    def minimize(self) -> None:
        self._main_window.minimize()

    @Slot()
    def toggleMaximized(self) -> None:
        if self._inputs.is_maximized:
            self._main_window.show_normal()
        else:
            self._main_window.show_maximized()

    @Slot()
    def toggleFullScreen(self) -> None:
        if self._inputs.is_fullscreen:
            self._main_window.exit_fullscreen()
        else:
            self._main_window.show_fullscreen()

    @Slot()
    def disableFullScreen(self) -> None:
        if self._inputs.is_fullscreen:
            self._main_window.exit_fullscreen()
