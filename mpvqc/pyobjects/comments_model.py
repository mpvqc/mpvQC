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
from PySide6.QtCore import Signal, Slot, QByteArray
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtQml import QmlElement

from mpvqc.services import PlayerService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class CommentModelPyObject(QStandardItemModel):
    _player = inject.attr(PlayerService)

    newItemAdded = Signal(int)  # param: row_index
    timeUpdated = Signal(int)  # param: row_index
    requestHighlight = Signal(int)  # param: row_index
    modelChanged = Signal()

    def __init__(self):
        super().__init__()
        self.setItemRoleNames(Role.MAPPING)
        self.setSortRole(Role.TIME)
        self.rowsInserted.connect(self.modelChanged)
        self.dataChanged.connect(self.modelChanged)
        self.rowsRemoved.connect(self.modelChanged)

    # Searching
    # match = self.match(self.index(0, 0), Role.COMMENT, "comment", 1000)
    # print(len(match))

    @Slot(str)
    def add_row(self, comment_type: str):
        seconds = self._player.current_time
        item = QStandardItem()
        item.setData(seconds, Role.TIME)
        item.setData(comment_type, Role.TYPE)
        item.setData("", Role.COMMENT)
        self.appendRow(item)
        self.sort(0)

        index = self.indexFromItem(item)
        index_row = index.row()
        self.newItemAdded.emit(index_row)

    @Slot(list)
    def import_comments(self, comments: list):
        if not comments:
            return

        item = None
        for comment in comments:
            item = QStandardItem()
            item.setData(comment['time'], Role.TIME)
            item.setData(comment['commentType'], Role.TYPE)
            item.setData(comment['comment'], Role.COMMENT)
            self.appendRow(item)

        self.sort(0)

        index = self.indexFromItem(item)
        index_row = index.row()
        self.requestHighlight.emit(index_row)

    @Slot(int)
    def remove_row(self, row: int):
        self.removeRow(row)

    @Slot(int, int)
    def update_time(self, row: int, time: int):
        index = self.index(row, 0)
        item = self.itemFromIndex(index)

        self.setData(index, time, Role.TIME)
        self.sort(0)

        self.timeUpdated.emit(item.row())

    @Slot(int, str)
    def update_comment_type(self, index: int, comment_type: str):
        self.setData(self.index(index, 0), comment_type, Role.TYPE)

    @Slot(int, str)
    def update_comment(self, index: int, comment: str):
        self.setData(self.index(index, 0), comment, Role.COMMENT)

    # noinspection PyTypeChecker
    @Slot(result=list)
    def comments(self) -> list:
        comments = []
        for row in range(0, self.rowCount()):
            item = self.item(row, column=0)
            comment = self._create_comment_from(item)
            comments.append(comment)
        return comments

    @staticmethod
    def _create_comment_from(item):
        return {
            'time': item.data(Role.TIME),
            'commentType': item.data(Role.TYPE),
            'comment': item.data(Role.COMMENT)
        }


class Role:
    """
    See: https://doc.qt.io/qt-6/qstandarditem.html#ItemType-enum

    Roles above 1000 are user definable roles. We use a role per value.
    In the Qt & Python context the value or role '1020' maps to 'timeStr' in Qml
    """

    TIME = 1010
    TYPE = 1020
    COMMENT = 1030

    MAPPING = {
        TIME: QByteArray(b'time'),
        TYPE: QByteArray(b'commentType'),
        COMMENT: QByteArray(b'comment'),
    }
