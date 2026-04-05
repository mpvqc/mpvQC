# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import typing
from typing import TYPE_CHECKING

from PySide6.QtCore import QPersistentModelIndex, Slot
from PySide6.QtGui import QUndoCommand, QUndoStack

from .item import CommentItem
from .roles import Role
from .utils import create_item_from

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence
    from typing import Any

    from PySide6.QtCore import QObject

    from mpvqc.datamodels import Comment

    from .model import MpvqcCommentModel


class ImportComments(QUndoCommand):
    def __init__(
        self,
        model: MpvqcCommentModel,
        comments: Sequence[dict[str, Any] | Comment],
        previously_selected_row: int,
        on_after_undo: Callable,
        on_after_redo: Callable,
    ) -> None:
        super().__init__()
        self._model = model
        self._comments = comments
        self._on_after_undo = on_after_undo
        self._on_after_redo = on_after_redo
        self._previously_selected_row = previously_selected_row

        self._added_initially = True
        self._rows: list[int] = []

    @typing.override
    def undo(self) -> None:
        for row in sorted(self._rows, reverse=True):
            self._model.removeRow(row)

        self._on_after_undo(self._previously_selected_row)

    @typing.override
    def redo(self) -> None:
        indices = []
        model_index = None

        for comment in self._comments:
            item = create_item_from(comment)
            self._model.appendRow(item)
            model_index = QPersistentModelIndex(item.index())
            indices.append(model_index)

        self._on_after_redo(model_index, self._added_initially)
        self._rows = [index.row() for index in indices]

        self._added_initially = False


class ClearComments(QUndoCommand):
    def __init__(
        self,
        model: MpvqcCommentModel,
        on_after_undo: Callable,
        on_after_redo: Callable,
    ) -> None:
        super().__init__()
        self._model = model
        self._on_after_undo = on_after_undo
        self._on_after_redo = on_after_redo

        self._comments: list[Comment] = []

    @typing.override
    def undo(self) -> None:
        for comment in self._comments:
            item = create_item_from(comment)
            self._model.appendRow(item)
        self._on_after_undo()

    @typing.override
    def redo(self) -> None:
        self._comments = list(self._model.retrieve_comments())
        self._model.removeRows(0, self._model.rowCount())
        self._on_after_redo()


class AddComment(QUndoCommand):
    def __init__(
        self,
        model: MpvqcCommentModel,
        comment_type: str,
        time: int,
        previously_selected_row: int,
        on_after_undo: Callable,
        on_after_redo: Callable,
    ) -> None:
        super().__init__()
        self._model = model
        self._comment_type = comment_type
        self._time = time
        self._previously_selected_row = previously_selected_row
        self._on_after_undo = on_after_undo
        self._on_after_redo = on_after_redo

        self._added_initially = True
        self._added_row: int | None = None

    @typing.override
    def undo(self) -> None:
        if (added_row := self._added_row) is not None:
            self._model.removeRow(added_row)
            self._on_after_undo(self._previously_selected_row)

    @typing.override
    def redo(self) -> None:
        item = CommentItem()
        item.time = self._time
        item.comment_type = self._comment_type
        item.comment = ""

        self._model.appendRow(item)
        index = QPersistentModelIndex(item.index())
        self._on_after_redo(index, self._added_initially)

        self._added_initially = False
        self._added_row = index.row()


class RemoveComment(QUndoCommand):
    def __init__(
        self,
        model: MpvqcCommentModel,
        row: int,
        on_after_undo: Callable,
        on_after_redo: Callable,
    ) -> None:
        super().__init__()
        self._model = model
        self._row = row
        self._on_after_undo = on_after_undo
        self._on_after_redo = on_after_redo

        self._comment: Comment | None = None

    @typing.override
    def undo(self) -> None:
        if (comment := self._comment) is not None:
            item = create_item_from(comment)
            self._model.appendRow(item)
            self._on_after_undo(self._row)

    @typing.override
    def redo(self) -> None:
        self._comment = self._model.comment_at(self._row)
        self._model.removeRow(self._row)
        self._on_after_redo()


class UpdateTime(QUndoCommand):
    def __init__(
        self,
        model: MpvqcCommentModel,
        row: int,
        new_time: int,
        on_after_undo: Callable,
        on_after_redo: Callable,
    ) -> None:
        super().__init__()
        self._model = model
        self._row = row
        self._new_time = new_time
        self._on_after_undo = on_after_undo
        self._on_after_redo = on_after_redo

        self._added_initially = True
        self._old_time: int | None = None
        self._new_row: int | None = None

    @typing.override
    def undo(self) -> None:
        if (new_row := self._new_row) is not None:
            index = self._model.index(new_row, 0)
            self._model.setData(index, self._old_time, Role.TIME)
            self._on_after_undo(self._row)

    @typing.override
    def redo(self) -> None:
        index = QPersistentModelIndex(self._model.index(self._row, 0))
        self._old_time = self._model.data(index, Role.TIME)
        self._model.setData(index, self._new_time, Role.TIME)
        self._on_after_redo(index, self._added_initially)

        self._added_initially = False
        self._new_row = index.row()


class UpdateType(QUndoCommand):
    def __init__(
        self,
        model: MpvqcCommentModel,
        row: int,
        new_comment_type: str,
        on_after_undo: Callable,
        on_after_redo: Callable,
    ) -> None:
        super().__init__()
        self.setText(f"update comment type | row:{row} new-comment-time:{new_comment_type}")
        self._model = model
        self._row = row
        self._new_comment_type = new_comment_type
        self._on_after_undo = on_after_undo
        self._on_after_redo = on_after_redo

        self._old_comment_type: str | None = None

    @typing.override
    def undo(self) -> None:
        index = self._model.index(self._row, 0)
        self._model.setData(index, self._old_comment_type, Role.TYPE)
        self._on_after_undo(self._row)

    @typing.override
    def redo(self) -> None:
        index = self._model.index(self._row, 0)
        self._old_comment_type = self._model.data(index, Role.TYPE)
        self._model.setData(index, self._new_comment_type, Role.TYPE)
        self._on_after_redo(self._row)


class UpdateComment(QUndoCommand):
    def __init__(
        self,
        model: MpvqcCommentModel,
        row: int,
        new_text: str,
        on_after_undo: Callable,
        on_after_redo: Callable,
    ) -> None:
        super().__init__()
        self._model = model
        self._row = row
        self._new_text = new_text
        self._on_after_undo = on_after_undo
        self._on_after_redo = on_after_redo

        self._old_comment: str | None = None

    @typing.override
    def undo(self) -> None:
        index = self._model.index(self._row, 0)
        self._model.setData(index, self._old_comment, Role.COMMENT)
        self._on_after_undo(self._row)

    @typing.override
    def redo(self) -> None:
        index = self._model.index(self._row, 0)
        self._old_comment = self._model.data(index, Role.COMMENT)
        self._model.setData(index, self._new_text, Role.COMMENT)
        self._on_after_redo(self._row)


class AddAndUpdateCommentCommand(QUndoCommand):
    def __init__(self, add_comment: AddComment) -> None:
        super().__init__()
        self._add_comment = add_comment
        self._update_comment: UpdateComment | None = None
        self.allow_update_from_row = None

    def merge_with(self, update_comment: UpdateComment) -> None:
        self._update_comment = update_comment
        self._update_comment.redo()

    @typing.override
    def undo(self) -> None:
        if self._update_comment is not None:
            self._update_comment.undo()
        self._add_comment.undo()

    @typing.override
    def redo(self) -> None:
        self._add_comment.redo()
        if self._update_comment is not None:
            self._update_comment.redo()


class MpvqcUndoStack(QUndoStack):
    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.indexChanged.connect(self.prevent_add_update_merge)
        self._last_add_command: AddAndUpdateCommentCommand | None = None

    @Slot()
    def prevent_add_update_merge(self) -> None:
        self._last_add_command = None

    @typing.override
    def push(self, command: QUndoCommand) -> None:
        match command:
            case AddAndUpdateCommentCommand():
                super().push(command)
                self._last_add_command = command
            case UpdateComment() if self._last_add_command:
                # noinspection PyTypeChecker
                self._last_add_command.merge_with(command)
                self.prevent_add_update_merge()
            case _:
                super().push(command)
