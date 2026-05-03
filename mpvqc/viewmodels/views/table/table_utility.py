# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, Signal
from PySide6.QtQml import QmlElement

from mpvqc.services.player import PlayerService

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcTableUtilityViewModel(QObject):
    _player = inject.attr(PlayerService)

    durationChanged = Signal(float)

    def __init__(self, /) -> None:
        super().__init__()
        self._player.duration_changed.connect(self.durationChanged)

    @Property(float, notify=durationChanged)
    def duration(self) -> float:
        return self._player.duration
