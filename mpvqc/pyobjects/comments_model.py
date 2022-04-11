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
from PySide6.QtCore import Slot, QByteArray
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtQml import QmlElement

from mpvqc.services import PlayerService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class CommentModelPyObject(QStandardItemModel):
    _player = inject.attr(PlayerService)

    def __init__(self):
        super().__init__()
        self.setItemRoleNames(Role.MAPPING)
        self.setSortRole(Role.TIME_INT)

    # Searching
    # match = self.match(self.index(0, 0), Role.COMMENT, "comment", 1000)
    # print(len(match))

    @Slot(int)
    def removeRow(self, row: int) -> bool:
        return super(CommentModelPyObject, self).removeRow(row)

    @Slot(str)
    def add_comment(self, comment_type: str):
        seconds, seconds_formatted = self._player.current_time
        item = QStandardItem()
        item.setData(seconds, Role.TIME_INT)
        item.setData(seconds_formatted, Role.TIME_STR)
        item.setData(comment_type, Role.TYPE)
        item.setData("", Role.COMMENT)
        self.appendRow(item)
        self.sort(0)


class Role:
    """
    See: https://doc.qt.io/qt-6/qstandarditem.html#ItemType-enum

    Roles above 1000 are user definable roles. We use a role per value.
    In the Qt & Python context the value or role '1020' maps to 'timeStr' in Qml
    """

    TIME_INT = 1010
    TIME_STR = 1020
    TYPE = 1030
    COMMENT = 1040

    MAPPING = {
        TIME_INT: QByteArray(b'timeInt'),
        TIME_STR: QByteArray(b'timeStr'),
        TYPE: QByteArray(b'type'),
        COMMENT: QByteArray(b'comment'),
    }
