# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from PySide6.QtCore import Property, QObject, Qt, Signal
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcWindowPropertiesBackend(QObject):
    appWidthChanged = Signal(int)
    appHeightChanged = Signal(int)

    isFullscreenChanged = Signal(bool)
    isMaximizedChanged = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._app_width = 0
        self._app_height = 0
        self._is_fullscreen = False
        self._is_maximized = False

        self._window = QGuiApplication.topLevelWindows()[0]

        self._calculate_app_width(self._window.width())
        self._calculate_app_height(self._window.height())
        self._update_window_states(self._window.windowState())

        self._width_connection = self._window.widthChanged.connect(lambda w: self._calculate_app_width(w))
        self._height_connection = self._window.heightChanged.connect(lambda h: self._calculate_app_height(h))
        self._window_state_connection = self._window.windowStateChanged.connect(lambda s: self._update_window_states(s))

    @Property(int, notify=appHeightChanged)
    def appHeight(self) -> int:
        return self._app_height

    def _calculate_app_height(self, app_height: int) -> None:
        if app_height != self._app_height:
            self._app_height = app_height
            self.appHeightChanged.emit(app_height)

    @Property(int, notify=appWidthChanged)
    def appWidth(self) -> int:
        return self._app_width

    def _calculate_app_width(self, app_width: int) -> None:
        if app_width != self._app_width:
            self._app_width = app_width
            self.appWidthChanged.emit(app_width)

    @Property(int, notify=isFullscreenChanged)
    def isFullscreen(self) -> bool:
        return self._is_fullscreen

    @Property(int, notify=isMaximizedChanged)
    def isMaximized(self) -> bool:
        return self._is_maximized

    def _update_window_states(self, state: Qt.WindowState) -> None:
        is_fullscreen = state == Qt.WindowState.WindowFullScreen
        is_maximized = state == Qt.WindowState.WindowMaximized

        if is_fullscreen != self._is_fullscreen:
            self._is_fullscreen = is_fullscreen
            self.isFullscreenChanged.emit(is_fullscreen)

        if is_maximized != self._is_maximized:
            self._is_maximized = is_maximized
            self.isMaximizedChanged.emit(is_maximized)
