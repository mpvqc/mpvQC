# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, Signal
from PySide6.QtQml import QmlElement

from mpvqc.services import WindowPropertiesService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcWindowPropertiesBackend(QObject):
    _window_properties_service: WindowPropertiesService = inject.attr(WindowPropertiesService)

    appWidthChanged = Signal(int)
    appHeightChanged = Signal(int)

    isFullscreenChanged = Signal(bool)
    isMaximizedChanged = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._window_properties_service.width_changed.connect(self.appWidthChanged.emit)
        self._window_properties_service.height_changed.connect(self.appHeightChanged.emit)
        self._window_properties_service.is_fullscreen_changed.connect(self.isFullscreenChanged.emit)
        self._window_properties_service.is_maximized_changed.connect(self.isMaximizedChanged.emit)

    @Property(int, notify=appWidthChanged)
    def appWidth(self) -> int:
        return self._window_properties_service.width

    @Property(int, notify=appHeightChanged)
    def appHeight(self) -> int:
        return self._window_properties_service.height

    @Property(bool, notify=isFullscreenChanged)
    def isFullscreen(self) -> bool:
        return self._window_properties_service.is_fullscreen

    @Property(bool, notify=isMaximizedChanged)
    def isMaximized(self) -> bool:
        return self._window_properties_service.is_maximized
