# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, QUrl, Slot
from PySide6.QtGui import QDesktopServices
from PySide6.QtQml import QmlAttached, QmlElement

from mpvqc.controllers._attachment_dialog_size import DialogDimensionsAttached
from mpvqc.services import ApplicationPathsService, ResourceService, TypeMapperService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker,PyCallingNonCallable,PyArgumentList
@QmlElement
@QmlAttached(DialogDimensionsAttached)
class MpvqcEditInputDialogControllerPyObject(QObject):
    _paths: ApplicationPathsService = inject.attr(ApplicationPathsService)
    _resources: ResourceService = inject.attr(ResourceService)
    _type_mapper: TypeMapperService = inject.attr(TypeMapperService)

    @Property(QUrl, constant=True, final=True)
    def inputFileUrl(self) -> QUrl:
        return self._type_mapper.map_path_to_url(self._paths.file_input_conf)

    @Property(str, constant=True, final=True)
    def defaultInputConfiguration(self) -> str:
        return self._resources.input_conf_content

    @Slot(QUrl)
    def openLink(self, link: QUrl) -> None:
        QDesktopServices.openUrl(link)

    @staticmethod
    def qmlAttachedProperties(_, parent) -> DialogDimensionsAttached:
        return DialogDimensionsAttached(
            calculate_width=lambda w: min(1080, w * 0.75),
            calculate_height=lambda h: min(1080, h * 0.70),
            parent=parent,
        )
