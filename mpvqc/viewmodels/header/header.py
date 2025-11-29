# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys

import inject
from PySide6.QtCore import Property, QCoreApplication, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import PlayerService, SettingsService, StateService

from .menu_bar import MpvqcMenuBarViewModel

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcHeaderViewModel(QObject):
    _player: PlayerService = inject.attr(PlayerService)
    _settings: SettingsService = inject.attr(SettingsService)
    _state: StateService = inject.attr(StateService)

    windowTitleChanged = Signal(str)

    windowDragRequested = Signal()
    minimizeAppRequested = Signal()
    toggleMaximizeAppRequested = Signal()
    closeAppRequested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._player.video_loaded_changed.connect(lambda _: self.windowTitleChanged.emit(self.windowTitle))
        self._player.path_changed.connect(lambda _: self.windowTitleChanged.emit(self.windowTitle))
        self._player.filename_changed.connect(lambda _: self.windowTitleChanged.emit(self.windowTitle))
        self._settings.windowTitleFormatChanged.connect(lambda _: self.windowTitleChanged.emit(self.windowTitle))
        self._settings.languageChanged.connect(lambda _: self.windowTitleChanged.emit(self.windowTitle))
        self._state.saved_changed.connect(lambda _: self.windowTitleChanged.emit(self.windowTitle))

    @Property(bool, constant=True, final=True)
    def isWindows(self) -> bool:
        return sys.platform == "win32"

    @Property(str, notify=windowTitleChanged)
    def windowTitle(self) -> str:
        window_title_format = self._settings.window_title_format
        WindowTitleFormat = MpvqcMenuBarViewModel.WindowTitleFormat

        if not self._player.video_loaded or window_title_format == WindowTitleFormat.DEFAULT:
            title = QCoreApplication.applicationName()
        elif window_title_format == WindowTitleFormat.FILE_NAME:
            title = self._player.filename or ""
        elif window_title_format == WindowTitleFormat.FILE_PATH:
            title = self._player.path or ""
        else:
            msg = "Cannot determine window title: configuration not known"
            raise ValueError(msg)

        if self._state.saved:
            return title

        #: %1 will be the title of the application (one of: mpvQC, file name, file path)
        return QCoreApplication.translate("MainWindow", "%1 (unsaved)").replace("%1", title)

    @Slot()
    def requestWindowDrag(self) -> None:
        self.windowDragRequested.emit()

    @Slot()
    def requestMinimize(self) -> None:
        self.minimizeAppRequested.emit()

    @Slot()
    def requestToggleMaximize(self) -> None:
        self.toggleMaximizeAppRequested.emit()

    @Slot()
    def requestClose(self) -> None:
        self.closeAppRequested.emit()
