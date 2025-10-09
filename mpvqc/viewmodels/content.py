# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, Qt, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import PlayerService, SettingsService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcContentViewModel(QObject):
    _player: PlayerService = inject.attr(PlayerService)
    _settings: SettingsService = inject.attr(SettingsService)

    appWindowSizeRequested = Signal(int, int)
    disableFullScreenRequested = Signal()
    toggleFullScreenRequested = Signal()
    openNewCommentMenuRequested = Signal()
    addNewCommentRequested = Signal(str)

    layoutOrientationChanged = Signal(int)
    commentTypesChanged = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._settings.layoutOrientationChanged.connect(self.layoutOrientationChanged)
        self._settings.commentTypesChanged.connect(self.commentTypesChanged)

    @Property(int, constant=True, final=True)
    def minContainerHeight(self) -> int:
        return 200

    @Property(int, constant=True, final=True)
    def minContainerWidth(self) -> int:
        return 500

    @Property(float, constant=True, final=True)
    def defaultSplitRatio(self) -> float:
        return 0.4

    @Property(int, notify=layoutOrientationChanged)
    def layoutOrientation(self) -> int:
        return self._settings.layout_orientation

    @Property(list, notify=commentTypesChanged)
    def commentTypes(self) -> list[str]:
        return self._settings.comment_types

    @Slot()
    def pausePlayer(self) -> None:
        self._player.pause()

    @Slot()
    def requestDisableFullScreen(self) -> None:
        self.disableFullScreenRequested.emit()

    @Slot()
    def requestToggleFullScreen(self) -> None:
        self.toggleFullScreenRequested.emit()

    @Slot(int, int)
    def requestResizeAppWindow(self, width: int, height: int) -> None:
        self.appWindowSizeRequested.emit(width, height)

    @Slot(str)
    def addNewEmptyComment(self, comment_type: str) -> None:
        self.addNewCommentRequested.emit(comment_type)

    @Slot(Qt.Key, Qt.KeyboardModifier, bool)
    def onKeyPressed(self, key: Qt.Key, modifiers: Qt.KeyboardModifier, is_auto_repeat: bool) -> None:  # noqa: C901
        plain_press = not is_auto_repeat and modifiers == Qt.KeyboardModifier.NoModifier
        no_modifier = modifiers == Qt.KeyboardModifier.NoModifier
        ctrl_modifier = (modifiers & Qt.KeyboardModifier.ControlModifier) != 0

        match key:
            case Qt.Key.Key_E if plain_press:
                self.openNewCommentMenuRequested.emit()
                return
            case Qt.Key.Key_F if plain_press:
                self.toggleFullScreenRequested.emit()
                return
            case Qt.Key.Key_Up | Qt.Key.Key_Down:
                return
            case Qt.Key.Key_Return if no_modifier:
                return
            case Qt.Key.Key_Escape if no_modifier:
                return
            case Qt.Key.Key_Delete if no_modifier:
                return
            case Qt.Key.Key_Backspace if no_modifier:
                return
            case Qt.Key.Key_F if ctrl_modifier:
                return
            case Qt.Key.Key_C if ctrl_modifier:
                return
            case Qt.Key.Key_Z if ctrl_modifier:
                return

        self._player.handle_key_event(key, modifiers)

    @Slot(int, int, result=dict)
    def calculatePreferredSplitSizes(self, split_view_width: int, split_view_height: int) -> dict:
        return {
            "width": round(split_view_width * self.defaultSplitRatio),
            "height": round(split_view_height * self.defaultSplitRatio),
        }
