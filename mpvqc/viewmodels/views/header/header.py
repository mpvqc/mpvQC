# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QCoreApplication, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.enums import MpvqcWindowTitleFormat
from mpvqc.services import PlayerService, SettingsService, StateService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1

WindowTitleFormat = MpvqcWindowTitleFormat.WindowTitleFormat


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcHeaderViewModel(QObject):
    _player = inject.attr(PlayerService)
    _settings = inject.attr(SettingsService)
    _state = inject.attr(StateService)

    windowTitleChanged = Signal(str)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._window_title = self._derive_window_title()
        self._player.video_loaded_changed.connect(self._update_window_title)
        self._player.path_changed.connect(self._update_window_title)
        self._player.filename_changed.connect(self._update_window_title)
        self._settings.windowTitleFormatChanged.connect(self._update_window_title)
        self._settings.languageChanged.connect(self._update_window_title)
        self._state.saved_changed.connect(self._update_window_title)

    @Property(str, notify=windowTitleChanged)
    def windowTitle(self) -> str:
        return self._derive_window_title()

    @Slot()
    def _update_window_title(self) -> None:
        new_value = self._derive_window_title()
        if new_value == self._window_title:
            return
        self._window_title = new_value
        self.windowTitleChanged.emit(new_value)

    def _derive_window_title(self) -> str:
        window_title_format = self._settings.window_title_format

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
