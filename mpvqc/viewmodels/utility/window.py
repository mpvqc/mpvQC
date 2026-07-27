# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import MainWindowService

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1

_WINDOW_RADIUS = 8


@QmlElement
class MpvqcWindowViewModel(QObject):
    _main_window = inject.attr(MainWindowService)

    windowGeometryWidthChanged = Signal(int)
    windowGeometryHeightChanged = Signal(int)
    isFullscreenChanged = Signal(bool)
    isMaximizedChanged = Signal(bool)
    dropShadowMarginChanged = Signal(int)
    radiusChanged = Signal()
    isMainWindowFocusedChanged = Signal(bool)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._main_window.window_geometry_width_changed.connect(self.windowGeometryWidthChanged)
        self._main_window.window_geometry_height_changed.connect(self.windowGeometryHeightChanged)
        self._main_window.is_fullscreen_changed.connect(self.isFullscreenChanged)
        self._main_window.is_maximized_changed.connect(self.isMaximizedChanged)
        self._main_window.drop_shadow_margin_changed.connect(self.dropShadowMarginChanged)
        self._main_window.drop_shadow_margin_changed.connect(self.radiusChanged)
        self._main_window.is_main_window_focused_changed.connect(self.isMainWindowFocusedChanged)

    @Property(int, notify=windowGeometryWidthChanged)
    def windowGeometryWidth(self) -> int:
        return self._main_window.window_geometry_width

    @Property(int, notify=windowGeometryHeightChanged)
    def windowGeometryHeight(self) -> int:
        return self._main_window.window_geometry_height

    @Property(bool, notify=isFullscreenChanged)
    def isFullscreen(self) -> bool:
        return self._main_window.is_fullscreen

    @Property(bool, notify=isMaximizedChanged)
    def isMaximized(self) -> bool:
        return self._main_window.is_maximized

    @Property(int, notify=dropShadowMarginChanged)
    def dropShadowMargin(self) -> int:
        return self._main_window.drop_shadow_margin

    @Property(int, notify=radiusChanged)
    def radius(self) -> int:
        return _WINDOW_RADIUS if self._main_window.drop_shadow_margin > 0 else 0

    @Property(bool, notify=isMainWindowFocusedChanged)
    def isMainWindowFocused(self) -> bool:
        return self._main_window.is_main_window_focused

    @Slot()
    def minimize(self) -> None:
        self._main_window.minimize()

    @Slot()
    def toggleMaximized(self) -> None:
        if self._main_window.is_maximized:
            self._main_window.show_normal()
        else:
            self._main_window.show_maximized()

    @Slot()
    def toggleFullScreen(self) -> None:
        if self._main_window.is_fullscreen:
            self._main_window.exit_fullscreen()
        else:
            self._main_window.show_fullscreen()

    @Slot()
    def disableFullScreen(self) -> None:
        if self._main_window.is_fullscreen:
            self._main_window.exit_fullscreen()
