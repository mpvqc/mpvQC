# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, Signal
from PySide6.QtQml import QmlElement

from mpvqc.services import MainWindowService

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcWindowPropertiesViewModel(QObject):
    _main_window = inject.attr(MainWindowService)

    appWidthChanged = Signal(int)
    appHeightChanged = Signal(int)

    isFullscreenChanged = Signal(bool)
    isMaximizedChanged = Signal(bool)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._main_window.content_width_changed.connect(self.appWidthChanged)
        self._main_window.content_height_changed.connect(self.appHeightChanged)
        self._main_window.is_fullscreen_changed.connect(self.isFullscreenChanged)
        self._main_window.is_maximized_changed.connect(self.isMaximizedChanged)

    @Property(int, notify=appWidthChanged)
    def appWidth(self) -> int:
        return self._main_window.content_width

    @Property(int, notify=appHeightChanged)
    def appHeight(self) -> int:
        return self._main_window.content_height

    @Property(bool, notify=isFullscreenChanged)
    def isFullscreen(self) -> bool:
        return self._main_window.is_fullscreen

    @Property(bool, notify=isMaximizedChanged)
    def isMaximized(self) -> bool:
        return self._main_window.is_maximized
