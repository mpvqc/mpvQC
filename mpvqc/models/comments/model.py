# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Iterator, Sequence
from typing import TYPE_CHECKING, Any, cast

import inject
from PySide6.QtCore import Property, QModelIndex, Signal, Slot
from PySide6.QtGui import QStandardItemModel
from PySide6.QtQml import QmlElement

from mpvqc.datamodels import Comment
from mpvqc.services import ImporterService, PlayerService, ResetService, StateService

from .roles import Role
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

if TYPE_CHECKING:
    from .item import CommentItem

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyTypeChecker,PyPep8Naming
@QmlElement
class MpvqcCommentModel(QStandardItemModel):
    _player = inject.attr(PlayerService)
    _state: StateService = inject.attr(StateService)
    _importer: ImporterService = inject.attr(ImporterService)
    _resetter: ResetService = inject.attr(ResetService)

    selectedRowChanged = Signal(int)

    comments_imported_initial = Signal(int)  # param: row of last imported comment
    comments_imported_undo = Signal(int)  # param: row of previously selected comment before comments have been imported
    comments_imported_redo = Signal(int)  # param: row of last imported comment

    comments_cleared_initial = Signal()
    comments_cleared_undo = Signal()

    comment_added_initial = Signal(int)  # param: row of new comment
    comment_added_undo = Signal(int)  # param: row of previously selected comment before comment has been added
    comment_added_redo = Signal(int)  # param: row of new redone comment

    comment_removed_initial = Signal()
    comment_removed_undo = Signal(int)  # param: row of comment that has been added back to the model

    time_updated_initial = Signal(int)  # param: row index after time update
    time_updated_undo = Signal(int)  # param: row index after time update restore
    time_updated_redo = Signal(int)  # param: row index after time update

    comment_type_updated_initial = Signal(int)
    comment_type_updated_undo = Signal(int)

    comment_updated_initial = Signal(int)
    comment_updated_undo = Signal(int)

    search_invalidated = Signal()

    _comments_changed = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setItemRoleNames(Role.MAPPING)
        self.setSortRole(Role.TIME)

        self._undo_stack = MpvqcUndoStack(self)
        self._selected_row = -1

        self._resetter.perform_reset.connect(self.clear_comments)
        self._importer.comments_ready_for_import.connect(self.import_comments)

        self.comments_cleared_undo.connect(self._comments_changed)
        self.comments_imported_redo.connect(self._comments_changed)
        self.comments_imported_undo.connect(self._comments_changed)
        self.comment_added_initial.connect(self._comments_changed)
        self.comment_added_undo.connect(self._comments_changed)
        self.comment_added_redo.connect(self._comments_changed)
        self.comment_removed_initial.connect(self._comments_changed)
        self.comment_removed_undo.connect(self._comments_changed)
        self.time_updated_initial.connect(self._comments_changed)
        self.time_updated_undo.connect(self._comments_changed)
        self.time_updated_redo.connect(self._comments_changed)
        self.comment_type_updated_initial.connect(self._comments_changed)
        self.comment_type_updated_undo.connect(self._comments_changed)
        self.comment_updated_initial.connect(self._comments_changed)
        self.comment_updated_undo.connect(self._comments_changed)
        self._comments_changed.connect(lambda: self._state.change())

    @Property(int, notify=selectedRowChanged)
    def selectedRow(self) -> int:
        return self._selected_row

    @selectedRow.setter
    def selectedRow(self, index: int) -> None:
        if self._selected_row != index:
            self._selected_row = index
            self.selectedRowChanged.emit(index)
            self._undo_stack.prevent_add_update_merge()

    @Slot(result=list)
    def comments(self) -> list[dict[str, Any]]:
        return [{"time": c.time, "commentType": c.comment_type, "comment": c.comment} for c in self.retrieve_comments()]

    @Slot(list)
    def import_comments(self, comments: Sequence[dict[str, Any] | Comment]) -> None:
        if not comments:
            return

        def on_after_undo(row: int) -> None:
            self.layoutChanged.emit()
            self.search_invalidated.emit()
            self.comments_imported_undo.emit(row)

        def on_after_redo(index: QModelIndex, added_initially: bool) -> None:
            self.layoutChanged.emit()
            self.search_invalidated.emit()
            self.sort(0)

            signal = self.comments_imported_initial if added_initially else self.comments_imported_redo
            signal.emit(index.row())

        self._undo_stack.push(
            ImportComments(
                model=self,
                comments=comments,
                on_after_undo=on_after_undo,
                on_after_redo=on_after_redo,
                previously_selected_row=self._selected_row,
            )
        )

    @Slot()
    def clear_comments(self) -> None:
        def on_after_undo() -> None:
            self.layoutChanged.emit()
            self.search_invalidated.emit()
            self.comments_cleared_undo.emit()

        def on_after_redo() -> None:
            self.layoutChanged.emit()
            self.search_invalidated.emit()
            self.comments_cleared_initial.emit()

        self._undo_stack.push(
            ClearComments(
                model=self,
                on_after_undo=on_after_undo,
                on_after_redo=on_after_redo,
            )
        )

    def add_row(self, comment_type: str) -> None:
        def on_after_undo(row: int) -> None:
            self.comment_added_undo.emit(row)
            self.search_invalidated.emit()

        def on_after_redo(index: QModelIndex, added_initially: bool) -> None:
            self.sort(0)

            signal = self.comment_added_initial if added_initially else self.comment_added_redo
            signal.emit(index.row())

            self.search_invalidated.emit()

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

    def remove_row(self, row: int) -> None:
        def on_after_undo(_row: int) -> None:
            self.sort(0)
            self.comment_removed_undo.emit(_row)
            self.search_invalidated.emit()

        def on_after_redo() -> None:
            self.comment_removed_initial.emit()
            self.search_invalidated.emit()

        self._undo_stack.push(
            RemoveComment(
                model=self,
                row=row,
                on_after_undo=on_after_undo,
                on_after_redo=on_after_redo,
            )
        )

    def update_time(self, row: int, new_time: int) -> None:
        def on_after_undo(_row: int) -> None:
            self.search_invalidated.emit()
            self.sort(0)
            self.time_updated_undo.emit(_row)

        def on_after_redo(index: QModelIndex, added_initially: bool) -> None:
            self.search_invalidated.emit()
            self.sort(0)

            signal = self.time_updated_initial if added_initially else self.time_updated_redo
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

    def update_comment_type(self, row: int, comment_type: str) -> None:
        def on_after_undo(_row: int) -> None:
            self.comment_type_updated_undo.emit(_row)

        def on_after_redo(_row: int) -> None:
            self.comment_type_updated_initial.emit(_row)

        self._undo_stack.push(
            UpdateType(
                model=self,
                row=row,
                new_comment_type=comment_type,
                on_after_undo=on_after_undo,
                on_after_redo=on_after_redo,
            )
        )

    def update_comment(self, row: int, comment: str) -> None:
        def on_after_undo(_row: int) -> None:
            self.search_invalidated.emit()
            self.comment_updated_undo.emit(_row)

        def on_after_redo(_row: int) -> None:
            self.search_invalidated.emit()
            self.comment_updated_initial.emit(_row)

        self._undo_stack.push(
            UpdateComment(
                model=self,
                row=row,
                new_text=comment,
                on_after_undo=on_after_undo,
                on_after_redo=on_after_redo,
            )
        )

    def undo(self) -> None:
        if self._undo_stack.canUndo():
            self._undo_stack.undo()

    def redo(self) -> None:
        if self._undo_stack.canRedo():
            self._undo_stack.redo()

    def comment_at(self, row: int) -> Comment:
        return cast("CommentItem", self.item(row, column=0)).to_comment()

    def retrieve_comments(self) -> Iterator[Comment]:
        for row in range(self.rowCount()):
            yield self.comment_at(row)
