# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, QUrl, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import ApplicationPathsService, DesktopService, ResourceService, TypeMapperService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker,PyCallingNonCallable,PyArgumentList
@QmlElement
class MpvqcEditMpvDialogViewModel(QObject):
    _desktop = inject.attr(DesktopService)
    _paths = inject.attr(ApplicationPathsService)
    _resources = inject.attr(ResourceService)
    _type_mapper = inject.attr(TypeMapperService)

    @Property(QUrl, constant=True, final=True)
    def mpvFileUrl(self) -> QUrl:
        return self._type_mapper.map_path_to_url(self._paths.file_mpv_conf)

    @Property(str, constant=True, final=True)
    def defaultMpvConfiguration(self) -> str:
        return self._resources.mpv_conf_content

    @Slot(QUrl)
    def openLink(self, link: QUrl) -> None:
        self._desktop.open_url(link)
