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
from PySide6.QtCore import QObject, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services.player import PlayerService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvPlayerPropertiesPyObject(QObject):
    _player = inject.attr(PlayerService)

    @Slot(list)
    def subscribe(self, properties: list[str]):
        for mpv_property in properties:
            if hasattr(self._player.mpv, mpv_property):
                self._observe(mpv_property)

    def _observe(self, mpv_property: str):
        player = self._player.mpv

        def set_property(_, value):
            self.setProperty(mpv_property, value)

        player.observe_property(name=mpv_property.replace('_', '-'), handler=set_property)

        current_value = getattr(player, mpv_property)
        set_property(mpv_property, current_value)
