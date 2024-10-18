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
from PySide6.QtCore import Property, QModelIndex, Qt, Signal, Slot
from PySide6.QtGui import QStandardItemModel, QUndoStack
from PySide6.QtQml import QmlElement

from mpvqc.models import Comment
from mpvqc.services import PlayerService

from .roles import Role
from .searcher import Searcher
from .undo_redo import MpvqcModelAddCommentCommand, MpvqcModelImportCommand

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcCommentModelPyObject(QStandardItemModel):
    _player = inject.attr(PlayerService)

    newCommentAddedInitially = Signal(int)  # param: row of new comment
    newCommentAddedRedone = Signal(int)  # param: row of new redone comment
    newCommentAddedUndone = Signal(int)  # param: row of previously selected comment before comment has been added
    timeUpdated = Signal(int)  # param: row index after time update
    commentsImported = Signal(int)  # param: row of last imported comment
    commentsImportedUndone = Signal(int)  # param: row of previously selected comment before comments have been imported
    commentsChanged = Signal()

    def get_selected_row(self) -> int:
        return self._selected_row

    def set_selected_row(self, index: int) -> None:
        self._selected_row = index

    selectedRowChanged = Signal(int)
    selectedRow = Property(int, get_selected_row, set_selected_row, notify=selectedRowChanged)

    def __init__(self):
        super().__init__()
        self.setItemRoleNames(Role.MAPPING)
        self.setSortRole(Role.TIME)
        self.setObjectName("mpvqcCommentModel")
        self.dataChanged.connect(self.commentsChanged)
        self._searcher = Searcher()

        self._undo_stack = QUndoStack(self)
        self._selected_row = -1

    def import_comments(self, comments: list[Comment]) -> None:
        if not comments:
            return

        def on_after_undo(row: int):
            self.invalidate_search()
            self.commentsImportedUndone.emit(row)

        def on_after_redo(index: QModelIndex):
            self.invalidate_search()
            self.sort(0)
            self.commentsImported.emit(index.row())

        self._undo_stack.push(
            MpvqcModelImportCommand(
                model=self,
                comments=comments,
                on_after_undo=on_after_undo,
                on_after_redo=on_after_redo,
                previously_selected_row=self._selected_row,
            )
        )

    @Slot(str)
    def add_row(self, comment_type: str) -> None:
        def on_after_undo(row: int):
            self.newCommentAddedUndone.emit(row)
            self.commentsChanged.emit()
            self.invalidate_search()

        def on_after_redo(index: QModelIndex, added_initially: bool):
            self.sort(0)

            signal = self.newCommentAddedInitially if added_initially else self.newCommentAddedRedone
            signal.emit(index.row())

            self.commentsChanged.emit()
            self.invalidate_search()

        self._undo_stack.push(
            MpvqcModelAddCommentCommand(
                model=self,
                comment_type=comment_type,
                time=round(self._player.current_time),
                previously_selected_row=self._selected_row,
                on_after_undo=on_after_undo,
                on_after_redo=on_after_redo,
            )
        )

    @Slot(int)
    def remove_row(self, row: int) -> None:
        self.removeRow(row)
        self.commentsChanged.emit()
        self.invalidate_search()

    @Slot(int, int)
    def update_time(self, row: int, time: int) -> None:
        index = self.index(row, 0)
        item = self.itemFromIndex(index)

        self.setData(index, time, Role.TIME)
        self.sort(0)

        self.timeUpdated.emit(item.row())
        self.invalidate_search()

    @Slot(int, str)
    def update_comment_type(self, index: int, comment_type: str) -> None:
        self.setData(self.index(index, 0), comment_type, Role.TYPE)

    @Slot(int, str)
    def update_comment(self, index: int, comment: str) -> None:
        self.setData(self.index(index, 0), comment, Role.COMMENT)
        self.invalidate_search()

    def clear_comments(self) -> None:
        self.clear()
        self.invalidate_search()

    @Slot()
    def undo(self):
        if self._undo_stack.canUndo():
            self._undo_stack.undo()

    @Slot()
    def redo(self):
        if self._undo_stack.canRedo():
            self._undo_stack.redo()

    def comments(self) -> list:
        comments = []
        for row in range(0, self.rowCount()):
            item = self.item(row, column=0)
            comment = self._create_comment_from(item)
            comments.append(comment)
        return comments

    @staticmethod
    def _create_comment_from(item) -> dict[str, str]:
        return {
            "time": int(item.data(Role.TIME)),
            "commentType": item.data(Role.TYPE),
            "comment": item.data(Role.COMMENT),
        }

    @Slot(str, bool, bool, int, result=dict)
    def search(self, query: str, include_current_row: bool, top_down: bool, selected_index: int):
        return self._searcher.search(query, include_current_row, top_down, selected_index, search_func=self._search)

    def _search(self, query: str) -> list[int]:
        from_beginning = self.index(0, 0)
        role = Role.COMMENT
        flags = Qt.MatchContains | Qt.MatchWrap
        all_results = -1  # Search everything
        results = self.match(from_beginning, role, query, all_results, flags)
        results = sorted(results)
        return list(map(lambda model_index: model_index.row(), results))

    @Slot()
    def invalidate_search(self):
        self._searcher.invalidate()
