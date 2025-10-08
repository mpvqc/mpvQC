# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any

import inject
from PySide6.QtCore import Property, QCoreApplication, QModelIndex, Signal, Slot
from PySide6.QtGui import QGuiApplication, QStandardItemModel
from PySide6.QtQml import QmlElement

from mpvqc.datamodels import Comment
from mpvqc.services import ImporterService, PlayerService, ResetService, StateService, TimeFormatterService

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
from .utils import retrieve_comments_from

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyTypeChecker,PyPep8Naming
@QmlElement
class MpvqcCommentModel(QStandardItemModel):
    _player = inject.attr(PlayerService)
    _time_formatter = inject.attr(TimeFormatterService)
    _state: StateService = inject.attr(StateService)
    _importer: ImporterService = inject.attr(ImporterService)
    _resetter: ResetService = inject.attr(ResetService)

    commentsImportedInitially = Signal(int)  # param: row of last imported comment
    commentsImportedUndone = Signal(int)  # param: row of previously selected comment before comments have been imported
    commentsImportedRedone = Signal(int)  # param: row of last imported comment

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

    searchInvalidated = Signal()
    copiedToClipboard = Signal(str)  # param: content - for tests only

    selectedRowChanged = Signal(int)

    _commentsChanged = Signal()

    def __init__(self):
        super().__init__()
        self.setItemRoleNames(Role.MAPPING)
        self.setSortRole(Role.TIME)
        self.setObjectName("mpvqcCommentModel")

        self._clipboard = QGuiApplication.clipboard()

        self._undo_stack = MpvqcUndoStack(self)
        self._selected_row = -1

        self._resetter.perform_reset.connect(self.clear_comments)
        self._importer.comments_ready_for_import.connect(self.import_comments)

        self.commentsClearedUndone.connect(self._commentsChanged)
        self.commentsImportedRedone.connect(self._commentsChanged)
        self.commentsImportedUndone.connect(self._commentsChanged)
        self.newCommentAddedInitially.connect(self._commentsChanged)
        self.newCommentAddedUndone.connect(self._commentsChanged)
        self.newCommentAddedRedone.connect(self._commentsChanged)
        self.commentRemoved.connect(self._commentsChanged)
        self.commentRemovedUndone.connect(self._commentsChanged)
        self.timeUpdatedInitially.connect(self._commentsChanged)
        self.timeUpdatedUndone.connect(self._commentsChanged)
        self.timeUpdatedRedone.connect(self._commentsChanged)
        self.commentTypeUpdated.connect(self._commentsChanged)
        self.commentTypeUpdatedUndone.connect(self._commentsChanged)
        self.commentUpdated.connect(self._commentsChanged)
        self.commentUpdatedUndone.connect(self._commentsChanged)
        self._commentsChanged.connect(lambda: self._state.change())

    @Property(int, notify=selectedRowChanged)
    def selectedRow(self) -> int:
        return self._selected_row

    @selectedRow.setter
    def selectedRow(self, index: int) -> None:
        if self._selected_row != index:
            self._selected_row = index
            self.selectedRowChanged.emit(index)
            self._undo_stack.prevent_add_update_merge()

    @Slot(list)
    def import_comments(self, comments: list[Comment]) -> None:
        if not comments:
            return

        def on_after_undo(row: int):
            self.searchInvalidated.emit()
            self.commentsImportedUndone.emit(row)

        def on_after_redo(index: QModelIndex, added_initially: bool):
            self.searchInvalidated.emit()
            self.sort(0)

            signal = self.commentsImportedInitially if added_initially else self.commentsImportedRedone
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

    def clear_comments(self) -> None:
        def on_after_undo():
            self.searchInvalidated.emit()
            self.commentsClearedUndone.emit()

        def on_after_redo():
            self.searchInvalidated.emit()
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
            self.searchInvalidated.emit()

        def on_after_redo(index: QModelIndex, added_initially: bool):
            self.sort(0)

            signal = self.newCommentAddedInitially if added_initially else self.newCommentAddedRedone
            signal.emit(index.row())

            self.searchInvalidated.emit()

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
            self.searchInvalidated.emit()

        def on_after_redo():
            self.commentRemoved.emit()
            self.searchInvalidated.emit()

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
            self.searchInvalidated.emit()
            self.sort(0)
            self.timeUpdatedUndone.emit(_row)

        def on_after_redo(index: QModelIndex, added_initially: bool):
            self.searchInvalidated.emit()
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
            self.searchInvalidated.emit()
            self.commentUpdatedUndone.emit(_row)

        def on_after_redo(_row: int):
            self.searchInvalidated.emit()
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

    @Slot(result=list)
    def comments(self) -> list[dict[str, Any]]:
        return retrieve_comments_from(self)

    @Slot(int)
    def copy_to_clipboard(self, row: int):
        item = self.item(row, column=0)

        time = item.data(Role.TIME)
        time = self._time_formatter.format_time_to_string(int(time), long_format=True)

        comment_type = f"{item.data(Role.TYPE)}"
        comment_type = QCoreApplication.translate("CommentTypes", comment_type)

        content = f"[{time}] [{comment_type}] {item.data(Role.COMMENT)}"

        self._clipboard.setText(content)
        self.copiedToClipboard.emit(content)
