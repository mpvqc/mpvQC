# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, QUrl
from PySide6.QtQml import QmlElement

from mpvqc.services import ApplicationPathsService, ResourceService, TypeMapperService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcPlayerFilesPyObject(QObject):
    _paths: ApplicationPathsService = inject.attr(ApplicationPathsService)
    _type_mapper: TypeMapperService = inject.attr(TypeMapperService)
    _resources: ResourceService = inject.attr(ResourceService)

    @Property(QUrl, constant=True, final=True)
    def input_conf_url(self) -> QUrl:
        return self._type_mapper.map_path_to_url(self._paths.file_input_conf)

    @Property(QUrl, constant=True, final=True)
    def mpv_conf_url(self) -> QUrl:
        return self._type_mapper.map_path_to_url(self._paths.file_mpv_conf)

    @Property(str, constant=True, final=True)
    def default_input_conf_content(self) -> str:
        return self._resources.input_conf_content

    @Property(str, constant=True, final=True)
    def default_mpv_conf_content(self) -> str:
        return self._resources.mpv_conf_content
