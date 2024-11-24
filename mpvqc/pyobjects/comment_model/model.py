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

from typing import Any

import inject
from PySide6.QtCore import Property, QCoreApplication, QModelIndex, Qt, Signal, Slot
from PySide6.QtGui import QClipboard, QStandardItemModel
from PySide6.QtQml import QmlElement

from mpvqc.models import Comment
from mpvqc.services import PlayerService, TimeFormatterService

from .roles import Role
from .searcher import Searcher
from .undo import (
    AddAndUpdateCommentCommand,
    AddComment,
    ClearComments,
    ImportComments,
    MpvqcUndoStack,
    RemoveComment,
    UpdateComment,
    UpdateTime,
    UpdateType,
)
from .utils import retrieve_comments_from

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcCommentModelPyObject(QStandardItemModel):
    _player = inject.attr(PlayerService)
    _time_formatter = inject.attr(TimeFormatterService)

    commentsImported = Signal(int)  # param: row of last imported comment
    commentsImportedUndone = Signal(int)  # param: row of previously selected comment before comments have been imported

    commentsCleared = Signal()
    commentsClearedUndone = Signal()

    newCommentAddedInitially = Signal(int)  # param: row of new comment
    newCommentAddedUndone = Signal(int)  # param: row of previously selected comment before comment has been added
    newCommentAddedRedone = Signal(int)  # param: row of new redone comment

    commentRemoved = Signal()
    commentRemovedUndone = Signal(int)  # param: row of comment that has been added back to the model

    timeUpdatedInitially = Signal(int)  # param: row index after time update
    timeUpdatedUndone = Signal(int)  # param: row index after time update restore
    timeUpdatedRedone = Signal(int)  # param: row index after time update

    commentTypeUpdated = Signal(int)
    commentTypeUpdatedUndone = Signal(int)

    commentUpdated = Signal(int)
    commentUpdatedUndone = Signal(int)

    def get_selected_row(self) -> int:
        return self._selected_row

    def set_selected_row(self, index: int) -> None:
        if self._selected_row != index:
            self._selected_row = index
            self.selectedRowChanged.emit(index)
            self._undo_stack.prevent_add_update_merge()

    selectedRowChanged = Signal(int)
    selectedRow = Property(int, get_selected_row, set_selected_row, notify=selectedRowChanged)

    def __init__(self):
        super().__init__()
        self.setItemRoleNames(Role.MAPPING)
        self.setSortRole(Role.TIME)
        self.setObjectName("mpvqcCommentModel")

        self._clipboard = QClipboard()

        self._searcher = Searcher()
        self._undo_stack = MpvqcUndoStack(self)
        self._selected_row = -1

    def import_comments(self, comments: list[Comment]) -> None:
        if not comments:
            return

        def on_after_undo(row: int):
            self._invalidate_search()
            self.commentsImportedUndone.emit(row)

        def on_after_redo(index: QModelIndex):
            self._invalidate_search()
            self.sort(0)
            self.commentsImported.emit(index.row())

        self._undo_stack.push(
            ImportComments(
                model=self,
                comments=comments,
                on_after_undo=on_after_undo,
                on_after_redo=on_after_redo,
                previously_selected_row=self._selected_row,
            )
        )

    def clear_comments(self) -> None:
        def on_after_undo():
            self._invalidate_search()
            self.commentsClearedUndone.emit()

        def on_after_redo():
            self._invalidate_search()
            self.commentsCleared.emit()

        self._undo_stack.push(
            ClearComments(
                model=self,
                on_after_undo=on_after_undo,
                on_after_redo=on_after_redo,
            )
        )

    @Slot(str)
    def add_row(self, comment_type: str) -> None:
        def on_after_undo(row: int):
            self.newCommentAddedUndone.emit(row)
            self._invalidate_search()

        def on_after_redo(index: QModelIndex, added_initially: bool):
            self.sort(0)

            signal = self.newCommentAddedInitially if added_initially else self.newCommentAddedRedone
            signal.emit(index.row())

            self._invalidate_search()

        command = AddAndUpdateCommentCommand(
            add_comment=AddComment(
                model=self,
                comment_type=comment_type,
                time=round(self._player.current_time),
                previously_selected_row=self._selected_row,
                on_after_undo=on_after_undo,
                on_after_redo=on_after_redo,
            )
        )
        self._undo_stack.push(command)

    @Slot(int)
    def remove_row(self, row: int) -> None:
        def on_after_undo(_row: int):
            self.sort(0)
            self.commentRemovedUndone.emit(_row)
            self._invalidate_search()

        def on_after_redo():
            self.commentRemoved.emit()
            self._invalidate_search()

        self._undo_stack.push(
            RemoveComment(
                model=self,
                row=row,
                on_after_undo=on_after_undo,
                on_after_redo=on_after_redo,
            )
        )

    @Slot(int, int)
    def update_time(self, row: int, new_time: int) -> None:
        def on_after_undo(_row: int):
            self._invalidate_search()
            self.sort(0)
            self.timeUpdatedUndone.emit(_row)

        def on_after_redo(index: QModelIndex, added_initially: bool):
            self._invalidate_search()
            self.sort(0)
            signal = self.timeUpdatedInitially if added_initially else self.timeUpdatedRedone
            signal.emit(index.row())

        self._undo_stack.push(
            UpdateTime(
                model=self,
                row=row,
                new_time=new_time,
                on_after_undo=on_after_undo,
                on_after_redo=on_after_redo,
            )
        )

    @Slot(int, str)
    def update_comment_type(self, row: int, comment_type: str) -> None:
        def on_after_undo(_row: int):
            self.commentTypeUpdatedUndone.emit(_row)

        def on_after_redo(_row: int):
            self.commentTypeUpdated.emit(_row)

        self._undo_stack.push(
            UpdateType(
                model=self,
                row=row,
                new_comment_type=comment_type,
                on_after_undo=on_after_undo,
                on_after_redo=on_after_redo,
            )
        )

    @Slot(int, str)
    def update_comment(self, row: int, comment: str) -> None:
        def on_after_undo(_row: int):
            self._invalidate_search()
            self.commentUpdatedUndone.emit(_row)

        def on_after_redo(_row: int):
            self._invalidate_search()
            self.commentUpdated.emit(_row)

        self._undo_stack.push(
            UpdateComment(
                model=self,
                row=row,
                new_text=comment,
                on_after_undo=on_after_undo,
                on_after_redo=on_after_redo,
            )
        )

    @Slot()
    def undo(self) -> None:
        if self._undo_stack.canUndo():
            self._undo_stack.undo()

    @Slot()
    def redo(self) -> None:
        if self._undo_stack.canRedo():
            self._undo_stack.redo()

    def comments(self) -> list[dict[str, Any]]:
        return retrieve_comments_from(self)

    @Slot(str, bool, bool, int, result=dict)
    def search(self, query: str, include_current_row: bool, top_down: bool, selected_index: int) -> dict:
        return self._searcher.search(query, include_current_row, top_down, selected_index, search_func=self._search)

    def _search(self, query: str) -> list[int]:
        from_beginning = self.index(0, 0)
        role = Role.COMMENT
        flags = Qt.MatchFlag.MatchContains | Qt.MatchFlag.MatchWrap
        all_results = -1  # Search everything
        results = self.match(from_beginning, role, query, all_results, flags)
        results = sorted(results)
        return list(map(lambda model_index: model_index.row(), results))

    def _invalidate_search(self) -> None:
        self._searcher.invalidate()

    @Slot(int)
    def copy_to_clipboard(self, row: int):
        item = self.item(row, column=0)

        time = item.data(Role.TIME)
        time = self._time_formatter.format_time_to_string(int(time), long_format=True)

        comment_type = f"{item.data(Role.TYPE)}"
        comment_type = QCoreApplication.translate("CommentTypes", comment_type)

        comment = f"{item.data(Role.COMMENT)}"

        self._clipboard.setText(f"[{time}] [{comment_type}] {comment}")
