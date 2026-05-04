# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import QObject, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import MainWindowService

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcWindowVisibilityViewModel(QObject):
    _main_window = inject.attr(MainWindowService)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._was_maximized_before = False

    @Slot()
    def toggleMaximized(self) -> None:
        if self._main_window.is_maximized:
            self._main_window.show_normal()
        else:
            self._main_window.show_maximized()

    @Slot()
    def toggleFullScreen(self) -> None:
        if self._main_window.is_fullscreen:
            self.disableFullScreen()
        else:
            self._enable_fullscreen()

    @Slot()
    def disableFullScreen(self) -> None:
        if self._main_window.is_fullscreen and self._was_maximized_before:
            self._main_window.show_maximized()
        elif self._main_window.is_fullscreen:
            self._main_window.show_normal()

    def _enable_fullscreen(self) -> None:
        if not self._main_window.is_fullscreen:
            self._was_maximized_before = self._main_window.is_maximized
            self._main_window.show_fullscreen()
