# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, Qt, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import KeyCommandGeneratorService, PlayerService, SettingsService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcContentViewModel(QObject):
    _player = inject.attr(PlayerService)
    _settings = inject.attr(SettingsService)
    _command_generator = inject.attr(KeyCommandGeneratorService)

    appWindowSizeRequested = Signal(int, int)
    disableFullScreenRequested = Signal()
    toggleFullScreenRequested = Signal()
    openNewCommentMenuRequested = Signal()
    addNewCommentRequested = Signal(str)

    layoutOrientationChanged = Signal(int)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._settings.layoutOrientationChanged.connect(self.layoutOrientationChanged)

    @Property(int, notify=layoutOrientationChanged)
    def layoutOrientation(self) -> int:
        return self._settings.layout_orientation

    @Slot()
    def requestDisableFullScreen(self) -> None:
        self.disableFullScreenRequested.emit()

    @Slot()
    def requestToggleFullScreen(self) -> None:
        self.toggleFullScreenRequested.emit()

    @Slot()
    def requestOpenNewCommentMenu(self) -> None:
        self.openNewCommentMenuRequested.emit()

    @Slot(int, int)
    def requestResizeAppWindow(self, width: int, height: int) -> None:
        self.appWindowSizeRequested.emit(width, height)

    @Slot(str)
    def addNewEmptyComment(self, comment_type: str) -> None:
        self.addNewCommentRequested.emit(comment_type)

    @Slot(Qt.Key, Qt.KeyboardModifier)
    def forwardKeyToPlayer(self, key: Qt.Key, modifiers: Qt.KeyboardModifier) -> None:
        if command := self._command_generator.generate_command(key, modifiers):
            self._player.press_key(command)
