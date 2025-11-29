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
class MpvqcApplicationViewModel(QObject):
    _window_properties: WindowPropertiesService = inject.attr(WindowPropertiesService)

    windowBorderChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._window_border = self._compute_window_border()
        self._window_properties.is_fullscreen_changed.connect(lambda _: self._update_window_border())
        self._window_properties.is_maximized_changed.connect(lambda _: self._update_window_border())

    def _compute_window_border(self) -> int:
        if self._window_properties.is_fullscreen or self._window_properties.is_maximized:
            return 0
        return 1

    def _update_window_border(self) -> None:
        new_value = self._compute_window_border()
        if new_value != self._window_border:
            self._window_border = new_value
            self.windowBorderChanged.emit(new_value)

    @Property(int, notify=windowBorderChanged)
    def windowBorder(self) -> int:
        return self._window_border
