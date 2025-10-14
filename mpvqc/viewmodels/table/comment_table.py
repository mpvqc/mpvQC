# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import PlayerService, SettingsService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyTypeChecker,PyPep8Naming
@QmlElement
class MpvqcCommentTableViewModel(QObject):
    _player: PlayerService = inject.attr(PlayerService)
    _settings: SettingsService = inject.attr(SettingsService)

    commentTypesChanged = Signal(list)
    videoDurationChanged = Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._settings.commentTypesChanged.connect(self.commentTypesChanged)
        self._player.duration_changed.connect(self.videoDurationChanged)

    @Property(list, notify=commentTypesChanged)
    def commentTypes(self) -> list[str]:
        return self._settings.comment_types

    @Property(float, notify=videoDurationChanged)
    def videoDuration(self) -> float:
        return self._player.duration

    @Slot(int)
    def jumpToTime(self, seconds: int) -> None:
        self._player.jump_to(seconds)

    @Slot()
    def pauseVideo(self) -> None:
        self._player.pause()
