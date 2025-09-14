# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QByteArray, Signal
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtQml import QmlElement

from mpvqc.services import ApplicationPathsService, TypeMapperService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcExportTemplateModelPyObject(QStandardItemModel):
    _app_paths: ApplicationPathsService = inject.attr(ApplicationPathsService)
    _type_mapper: TypeMapperService = inject.attr(TypeMapperService)

    countChanged = Signal(int)

    @Property(int, notify=countChanged)
    def count(self) -> int:
        return self.rowCount()

    def __init__(self):
        super().__init__()
        self.setItemRoleNames(Role.MAPPING)
        self.setSortRole(Role.NAME)
        self._initialize_model()

    def _initialize_model(self):
        for template in self._app_paths.files_export_templates:
            url = self._type_mapper.map_path_to_url(template)

            item = QStandardItem()
            item.setData(url, Role.PATH)
            item.setData(template.stem, Role.NAME)
            self.appendRow(item)
        self.sort(0)


class Role:
    """
    See: https://doc.qt.io/qt-6/qstandarditem.html#ItemType-enum
    """

    NAME = 1010
    PATH = 1020

    MAPPING = {
        NAME: QByteArray(b"name"),
        PATH: QByteArray(b"path"),
    }
