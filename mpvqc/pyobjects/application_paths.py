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
from PySide6.QtCore import Property, QObject, QUrl
from PySide6.QtQml import QmlElement

from mpvqc.services import ApplicationPathsService, TypeMapperService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcApplicationPathsPyObject(QObject):
    _paths = inject.attr(ApplicationPathsService)
    _type_mapper: TypeMapperService = inject.attr(TypeMapperService)

    @Property(str, constant=True, final=True)
    def input_conf(self) -> str:
        return self._type_mapper.map_path_to_str(self._paths.file_input_conf)

    @Property(str, constant=True, final=True)
    def mpv_conf(self) -> str:
        return self._type_mapper.map_path_to_str(self._paths.file_mpv_conf)

    @Property(QUrl, constant=True, final=True)
    def dir_backup(self) -> QUrl:
        return self._type_mapper.map_path_to_url(self._paths.dir_backup)

    @Property(QUrl, constant=True, final=True)
    def settings(self) -> QUrl:
        return self._type_mapper.map_path_to_url(self._paths.file_settings)
