# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import QObject, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import WindowPropertiesService

from .window_utils import get_main_window

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcWindowVisibilityHandler(QObject):
    _window_properties_service: WindowPropertiesService = inject.attr(WindowPropertiesService)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._window = get_main_window()
        self._was_maximized_before = False

    @Slot()
    def toggleMaximized(self) -> None:
        if self._window_properties_service.is_maximized:
            self._window.showNormal()
        else:
            self._window.showMaximized()

    @Slot()
    def toggleFullScreen(self) -> None:
        if self._window_properties_service.is_fullscreen:
            self.disableFullScreen()
        else:
            self._enable_fullscreen()

    @Slot()
    def disableFullScreen(self) -> None:
        if self._window_properties_service.is_fullscreen and self._was_maximized_before:
            self._window.showMaximized()
        elif self._window_properties_service.is_fullscreen:
            self._window.showNormal()

    def _enable_fullscreen(self) -> None:
        if not self._window_properties_service.is_fullscreen:
            self._was_maximized_before = self._window_properties_service.is_maximized
            self._window.showFullScreen()
