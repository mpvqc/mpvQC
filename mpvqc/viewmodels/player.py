# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import QObject, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import PlayerService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming
@QmlElement
class MpvqcPlayerViewModel(QObject):
    _player: PlayerService = inject.attr(PlayerService)

    @Slot(int, int)
    def moveMouse(self, x, y) -> None:
        self._player.move_mouse(x, y)

    @Slot()
    def scrollUp(self) -> None:
        self._player.scroll_up()

    @Slot()
    def scrollDown(self) -> None:
        self._player.scroll_down()

    @Slot()
    def pressMouseLeft(self) -> None:
        self._player.press_mouse_left()

    @Slot()
    def pressMouseMiddle(self) -> None:
        self._player.press_mouse_middle()

    @Slot()
    def releaseMouseLeft(self) -> None:
        self._player.release_mouse_left()
