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

from mpvqc.services import SettingsService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
@QmlSingleton
class SettingsPyObject(QObject):
    _settings_backend = inject.attr(SettingsService)

    def get_backing_object_file_name(self):
        return self._settings_backend.backing_object.fileName()

    backing_object_file_name_changed = Signal(str)
    backing_object_file_name = Property(str, get_backing_object_file_name, notify=backing_object_file_name_changed)
