# mpvQC
#
# Copyright (C) 2022 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import inject
from PySide6.QtCore import Slot, QUrl, QObject
from PySide6.QtQml import QmlElement

from mpvqc.services import PlayerService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcMpvPlayerPyObject(QObject):
    _player = inject.attr(PlayerService)

    @Slot(QUrl)
    def open_video(self, video: QUrl) -> None:
        self._player.open_video(video.toString())
        self._player.play()

    @Slot(list)
    def open_subtitles(self, subtitles: list[str]) -> None:
        subtitles = map(lambda url_str: QUrl(url_str).toLocalFile(), subtitles)
        # noinspection PyTypeChecker
        self._player.open_subtitles(tuple(subtitles))

    @Slot()
    def pause(self) -> None:
        self._player.pause()

    @Slot(str)
    def execute(self, command) -> None:
        self._player.execute(command)

    @Slot(int)
    def jump_to(self, seconds: int) -> None:
        self._player.jump_to(seconds)

    @Slot(int, int)
    def move_mouse(self, x, y) -> None:
        self._player.move_mouse(x, y)

    @Slot()
    def scroll_up(self) -> None:
        self._player.scroll_up()

    @Slot()
    def scroll_down(self) -> None:
        self._player.scroll_down()

    @Slot()
    def press_mouse_left(self) -> None:
        self._player.press_mouse_left()

    @Slot()
    def press_mouse_middle(self) -> None:
        self._player.press_mouse_middle()

    @Slot()
    def release_mouse_left(self) -> None:
        self._player.release_mouse_left()
