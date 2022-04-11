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

from mpvqc.services import ResourceService, BuildInfoService, PlayerService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
@QmlSingleton
class DialogAboutPyObject(QObject):
    _resources = inject.attr(ResourceService)
    _build_info = inject.attr(BuildInfoService)
    _player = inject.attr(PlayerService)

    def get_icon_resource(self) -> str:
        return self._resources.window_icon_path

    icon_resource_changed = Signal(str)
    icon_resource = Property(str, get_icon_resource, notify=icon_resource_changed)

    def get_tag(self) -> str:
        return self._build_info.tag

    tag_changed = Signal(str)
    tag = Property(str, get_tag, notify=tag_changed)

    def get_commit_id(self) -> str:
        return self._build_info.commit

    commit_id_changed = Signal(str)
    commit_id = Property(str, get_commit_id, notify=commit_id_changed)

    def get_mpv_version(self) -> str:
        return self._player.version_mpv()

    mpv_version_changed = Signal(str)
    mpv_version = Property(str, get_mpv_version, notify=mpv_version_changed)

    def get_ffmpeg_version(self) -> str:
        return self._player.version_ffmpeg()

    ffmpeg_version_changed = Signal(str)
    ffmpeg_version = Property(str, get_ffmpeg_version, notify=ffmpeg_version_changed)
