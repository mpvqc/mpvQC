# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

import inject
from PySide6.QtCore import Property, QModelIndex, Signal, Slot
from PySide6.QtGui import QStandardItemModel
from PySide6.QtQml import QmlElement

from mpvqc.services import PlayerService

from .mutation import AnimatedSelection, LastRowSelection, NoViewAction, QuickSelection, RowAddEdit
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
    from collections.abc import Iterator, Sequence

    from PySide6.QtCore import QObject

    from mpvqc.datamodels import Comment

    from .item import CommentItem

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyTypeChecker,PyPep8Naming
@QmlElement
class MpvqcCommentModel(QStandardItemModel):
    _player = inject.attr(PlayerService)

    selectedRowChanged = Signal(int)

    mutated = Signal(object)
    search_invalidated = Signal()

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.setItemRoleNames(Role.MAPPING)
        self.setSortRole(Role.TIME)

        self._undo_stack = MpvqcUndoStack(self)
        self._selected_row = -1

        self.selectedRowChanged.connect(self._undo_stack.prevent_add_update_merge)

    @Property(int, notify=selectedRowChanged)
    def selectedRow(self) -> int:
        return self._selected_row

    @selectedRow.setter
    def selectedRow(self, index: int) -> None:
        if self._selected_row != index:
            self._selected_row = index
            self.selectedRowChanged.emit(index)

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
            self.mutated.emit(QuickSelection(row=row))

        def on_after_redo(index: QModelIndex, added_initially: bool) -> None:
            self.layoutChanged.emit()
            self.search_invalidated.emit()
            self.sort(0)
            self.mutated.emit(QuickSelection(row=index.row(), marks_unsaved=not added_initially))

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
            self.mutated.emit(LastRowSelection())

        def on_after_redo() -> None:
            self.layoutChanged.emit()
            self.search_invalidated.emit()
            self.mutated.emit(NoViewAction(marks_unsaved=False))

        self._undo_stack.push(
            ClearComments(
                model=self,
                on_after_undo=on_after_undo,
                on_after_redo=on_after_redo,
            )
        )

    def add_row(self, comment_type: str) -> None:
        def on_after_undo(row: int) -> None:
            self.mutated.emit(QuickSelection(row=row))
            self.search_invalidated.emit()

        def on_after_redo(index: QModelIndex, added_initially: bool) -> None:
            self.sort(0)
            mutation = RowAddEdit(row=index.row()) if added_initially else QuickSelection(row=index.row())
            self.mutated.emit(mutation)
            self.search_invalidated.emit()

        command = AddAndUpdateCommentCommand(
            add_comment=AddComment(
                model=self,
                comment_type=comment_type,
                time=self._player.current_time,
                previously_selected_row=self._selected_row,
                on_after_undo=on_after_undo,
                on_after_redo=on_after_redo,
            )
        )
        self._undo_stack.push(command)

    def remove_row(self, row: int) -> None:
        def on_after_undo(_row: int) -> None:
            self.sort(0)
            self.mutated.emit(QuickSelection(row=_row))
            self.search_invalidated.emit()

        def on_after_redo() -> None:
            self.mutated.emit(NoViewAction(marks_unsaved=True))
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
            self.mutated.emit(QuickSelection(row=_row))

        def on_after_redo(index: QModelIndex, added_initially: bool) -> None:
            self.search_invalidated.emit()
            self.sort(0)
            mutation = AnimatedSelection(row=index.row()) if added_initially else QuickSelection(row=index.row())
            self.mutated.emit(mutation)

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
        def on_mutation(_row: int) -> None:
            self.mutated.emit(QuickSelection(row=_row))

        self._undo_stack.push(
            UpdateType(
                model=self,
                row=row,
                new_comment_type=comment_type,
                on_after_undo=on_mutation,
                on_after_redo=on_mutation,
            )
        )

    def update_comment(self, row: int, comment: str) -> None:
        def on_mutation(_row: int) -> None:
            self.search_invalidated.emit()
            self.mutated.emit(QuickSelection(row=_row))

        self._undo_stack.push(
            UpdateComment(
                model=self,
                row=row,
                new_text=comment,
                on_after_undo=on_mutation,
                on_after_redo=on_mutation,
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
