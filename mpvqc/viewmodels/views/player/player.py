# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import PlayerService
from mpvqc.window.services import MainWindowService, PlatformService

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcPlayerViewModel(QObject):
    _main_window = inject.attr(MainWindowService)
    _player = inject.attr(PlayerService)
    _platform = inject.attr(PlatformService)

    @Property(bool, constant=True)
    def embedsNativePlayer(self) -> bool:
        return self._platform.capabilities.embeds_native_player

    @Slot(int, int)
    def moveMouse(self, x: int, y: int) -> None:
        zoom_factor = self._main_window.display_zoom_factor
        self._player.move_mouse(int(x * zoom_factor), int(y * zoom_factor))

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

    @Slot()
    def pressMouseBack(self) -> None:
        self._player.press_mouse_back()

    @Slot()
    def pressMouseForward(self) -> None:
        self._player.press_mouse_forward()
