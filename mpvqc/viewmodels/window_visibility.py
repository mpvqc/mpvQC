# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import QObject, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import MainWindowService

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcWindowVisibilityViewModel(QObject):
    _main_window = inject.attr(MainWindowService)

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
