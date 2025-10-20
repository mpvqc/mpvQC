# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, QPoint, Signal, Slot
from PySide6.QtGui import QCursor
from PySide6.QtQml import QmlElement

from mpvqc.services import PlayerService, SettingsService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcNewCommentMenuViewModel(QObject):
    _player: PlayerService = inject.attr(PlayerService)
    _settings: SettingsService = inject.attr(SettingsService)

    commentTypesChanged = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._settings.commentTypesChanged.connect(self.commentTypesChanged)

    @Property(list, notify=commentTypesChanged)
    def commentTypes(self) -> list[str]:
        return self._settings.comment_types

    @Slot(result=QPoint)
    def cursorPosition(self) -> QPoint:
        return QCursor.pos()

    @Slot()
    def pausePlayer(self) -> None:
        self._player.pause()
