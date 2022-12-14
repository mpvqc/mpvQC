#  mpvQC
#
#  Copyright (C) 2022 mpvQC developers
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


import inject
from PySide6.QtCore import QObject, Signal, Property, QUrl
from PySide6.QtQml import QmlElement, QmlSingleton

from mpvqc.services import FilePathService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcFilePathsPyObject(QObject):
    _paths = inject.attr(FilePathService)

    #

    def get_config_input(self) -> str:
        return str(self._paths.file_input_conf.absolute())

    input_conf_changed = Signal(str)
    input_conf = Property(str, get_config_input, notify=input_conf_changed)

    #

    def get_config_mpv(self) -> str:
        return str(self._paths.file_mpv_conf.absolute())

    mpv_conf_changed = Signal(str)
    mpv_conf = Property(str, get_config_mpv, notify=mpv_conf_changed)

    #

    def get_dir_backup(self) -> QUrl:
        return QUrl.fromLocalFile(self._paths.dir_backup.absolute())

    dir_backup_changed = Signal(QUrl)
    dir_backup = Property(QUrl, get_dir_backup, notify=dir_backup_changed)

    #

    def get_settings(self) -> str:
        return str(self._paths.file_settings.absolute())

    settings_changed = Signal(str)
    settings = Property(str, get_settings, notify=settings_changed)
