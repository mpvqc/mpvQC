#  mpvQC
#
#  Copyright (C) 2022 mpvQC developers
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


import inject
from PySide6.QtCore import Property, Signal, QObject
from PySide6.QtQml import QmlElement, QmlSingleton

from mpvqc.services.player import PlayerService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
@QmlSingleton
class MpvPlayerPropertiesPyObject(QObject):
    _player = inject.attr(PlayerService)

    def get_mpv_version(self) -> str:
        return self._player.version_mpv()

    mpv_version_changed = Signal(str)
    mpv_version = Property(str, get_mpv_version, notify=mpv_version_changed)

    def get_ffmpeg_version(self) -> str:
        return self._player.version_ffmpeg()

    ffmpeg_version_changed = Signal(str)
    ffmpeg_version = Property(str, get_ffmpeg_version, notify=ffmpeg_version_changed)
