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
from PySide6.QtCore import Signal, Property, QObject
from PySide6.QtQml import QmlElement, QmlSingleton

from mpvqc.services import SettingsService, SettingsInitializerService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
@QmlSingleton
class SettingsPyObject(QObject):
    _settings = inject.attr(SettingsService)
    _settings_backend = inject.attr(SettingsInitializerService)

    def get_backing_object_file_name(self):
        return self._settings_backend.backing_object.fileName()

    backing_object_file_name_changed = Signal(str)
    backing_object_file_name = Property(str, get_backing_object_file_name, notify=backing_object_file_name_changed)

    @staticmethod
    def _fire_on_change(value_old: any, value_new: any, signal: Signal):
        if value_old != value_new:
            signal.emit(value_new)

    #
    # Config input
    #

    def get_config_input(self) -> str:
        return self._settings.config_input

    def set_config_input(self, value: str) -> None:
        old_value = self.get_config_input()
        self._settings.config_input = value
        self._fire_on_change(old_value, value, signal=self.config_input_changed)

    config_input_changed = Signal(str)
    config_input = Property(str, get_config_input, set_config_input, notify=config_input_changed)

    #
    # Config mpv
    #

    def get_config_mpv(self) -> str:
        return self._settings.config_mpv

    def set_config_mpv(self, value: str) -> None:
        old_value = self.get_config_mpv()
        self._settings.config_mpv = value
        self._fire_on_change(old_value, value, signal=self.config_mpv_changed)

    config_mpv_changed = Signal(str)
    config_mpv = Property(str, get_config_mpv, set_config_mpv, notify=config_mpv_changed)
