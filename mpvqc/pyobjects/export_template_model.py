# mpvQC
#
# Copyright (C) 2024 mpvQC developers
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
from PySide6.QtCore import QByteArray
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtQml import QmlElement

from mpvqc.services import ApplicationPathsService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcExportTemplateModelPyObject(QStandardItemModel):
    _app_paths = inject.attr(ApplicationPathsService)

    def __init__(self):
        super().__init__()
        self.setItemRoleNames(Role.MAPPING)
        self.setSortRole(Role.NAME)
        self._initialize_model()

    def _initialize_model(self):
        for template in self._app_paths.files_export_templates:
            item = QStandardItem()
            item.setData(str(template.absolute()), Role.PATH)
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
        NAME: QByteArray(b'name'),
        PATH: QByteArray(b'path'),
    }
