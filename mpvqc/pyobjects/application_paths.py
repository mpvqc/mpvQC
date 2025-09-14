# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

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
