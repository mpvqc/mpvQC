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

from typing import Any, Callable, Optional

from PySide6.QtCore import QPersistentModelIndex
from PySide6.QtGui import QStandardItemModel, QUndoCommand

from mpvqc.models import Comment

from .item import CommentItem
from .roles import Role
from .utils import create_comment_from, create_item_from, retrieve_comments_from


class ImportComments(QUndoCommand):
    def __init__(
        self,
        model: QStandardItemModel,
        comments: list[Comment],
        previously_selected_row: int,
        on_after_undo: Callable,
        on_after_redo: Callable,
    ):
        super().__init__()
        self.setText(f"import comments | size:{len(comments)}")
        self._model = model
        self._comments = comments
        self._on_after_undo = on_after_undo
        self._on_after_redo = on_after_redo
        self._previously_selected_row = previously_selected_row

        self._rows: list[int] = []

    def undo(self):
        for row in reversed(self._rows):
            self._model.removeRow(row)

        self._on_after_undo(self._previously_selected_row)

    def redo(self):
        indices = []
        model_index = None

        for comment in self._comments:
            item = create_item_from(comment)
            self._model.appendRow(item)
            model_index = QPersistentModelIndex(item.index())
            indices.append(model_index)

        self._on_after_redo(model_index)
        self._rows = [index.row() for index in indices]


class ClearComments(QUndoCommand):
    def __init__(
        self,
        model: QStandardItemModel,
        on_after_undo: Callable,
        on_after_redo: Callable,
    ):
        super().__init__()
        self.setText("clear comments")
        self._model = model
        self._on_after_undo = on_after_undo
        self._on_after_redo = on_after_redo

        self._comments: list[dict[str, Any]] = []

    def undo(self):
        for comment in self._comments:
            item = create_item_from(comment)
            self._model.appendRow(item)
        self._on_after_undo()

    def redo(self):
        self._comments = retrieve_comments_from(self._model)
        self._model.clear()
        self._on_after_redo()


class AddComment(QUndoCommand):
    def __init__(
        self,
        model: QStandardItemModel,
        comment_type: str,
        time: int,
        previously_selected_row: int,
        on_after_undo: Callable,
        on_after_redo: Callable,
    ):
        super().__init__()
        self.setText(f"add comment | {time}:{comment_type}")
        self._model = model
        self._comment_type = comment_type
        self._time = time
        self._previously_selected_row = previously_selected_row
        self._on_after_undo = on_after_undo
        self._on_after_redo = on_after_redo

        self._added_initially = True
        self._added_row: int | None = None

    def undo(self):
        self._model.removeRow(self._added_row)
        self._on_after_undo(self._previously_selected_row)

    def redo(self):
        item = CommentItem()
        item.setData(self._time, Role.TIME)
        item.setData(self._comment_type, Role.TYPE)
        item.setData("", Role.COMMENT)

        self._model.appendRow(item)
        index = QPersistentModelIndex(item.index())
        self._on_after_redo(index, self._added_initially)

        self._added_initially = False
        self._added_row = index.row()


class RemoveComment(QUndoCommand):
    def __init__(
        self,
        model: QStandardItemModel,
        row: int,
        on_after_undo: Callable,
        on_after_redo: Callable,
    ):
        super().__init__()
        self.setText(f"remove comment | row: {row}")
        self._model = model
        self._row = row
        self._on_after_undo = on_after_undo
        self._on_after_redo = on_after_redo

        self._comment: Optional[dict[str, Any]] = None

    def undo(self):
        item = create_item_from(self._comment)
        self._model.appendRow(item)
        self._on_after_undo(self._row)

    def redo(self):
        item = self._model.item(self._row)
        self._comment = create_comment_from(item)
        self._model.removeRow(self._row)
        self._on_after_redo()


class UpdateTime(QUndoCommand):
    def __init__(
        self,
        model: QStandardItemModel,
        row: int,
        new_time: int,
        on_after_undo: Callable,
        on_after_redo: Callable,
    ):
        super().__init__()
        self.setText(f"update time | row:{row} new-time:{new_time}")
        self._model = model
        self._row = row
        self._new_time = new_time
        self._on_after_undo = on_after_undo
        self._on_after_redo = on_after_redo

        self._added_initially = True
        self._old_time: int | None = None
        self._new_row: int | None = None

    def undo(self):
        item = self._model.item(self._new_row)
        item.setData(self._old_time, Role.TIME)
        self._on_after_undo(self._row)

    def redo(self):
        index = QPersistentModelIndex(self._model.index(self._row, 0))
        self._old_time = self._model.data(index, Role.TIME)
        self._model.setData(index, self._new_time, Role.TIME)
        self._on_after_redo(index, self._added_initially)

        self._added_initially = False
        self._new_row = index.row()


class UpdateType(QUndoCommand):
    def __init__(
        self,
        model: QStandardItemModel,
        row: int,
        new_comment_type: str,
        on_after_undo: Callable,
        on_after_redo: Callable,
    ):
        super().__init__()
        self.setText(f"update comment type | row:{row} new-comment-time:{new_comment_type}")
        self._model = model
        self._row = row
        self._new_comment_type = new_comment_type
        self._on_after_undo = on_after_undo
        self._on_after_redo = on_after_redo

        self._old_comment_type: str | None = None

    def undo(self):
        index = self._model.index(self._row, 0)
        self._model.setData(index, self._old_comment_type, Role.TYPE)
        self._on_after_undo(self._row)

    def redo(self):
        index = self._model.index(self._row, 0)
        self._old_comment_type = self._model.data(index, Role.TYPE)
        self._model.setData(index, self._new_comment_type, Role.TYPE)
        self._on_after_redo(self._row)


class UpdateComment(QUndoCommand):
    def __init__(
        self,
        model: QStandardItemModel,
        row: int,
        new_text: str,
        on_after_undo: Callable,
        on_after_redo: Callable,
    ):
        super().__init__()
        self._model = model
        self._row = row
        self._new_text = new_text
        self._on_after_undo = on_after_undo
        self._on_after_redo = on_after_redo

        self._old_comment: str | None = None

    def undo(self):
        index = self._model.index(self._row, 0)
        self._model.setData(index, self._old_comment, Role.COMMENT)
        self._on_after_undo(self._row)

    def redo(self):
        index = self._model.index(self._row, 0)
        self._old_comment = self._model.data(index, Role.COMMENT)
        self._model.setData(index, self._new_text, Role.COMMENT)
        self._on_after_redo(self._row)


class AddAndUpdateCommentCommand(QUndoCommand):
    def __init__(self, add_comment: AddComment):
        super().__init__()
        self._add_comment = add_comment
        self._update_comment = None
        self.allow_update_from_row = None

    def merge_with(self, update_comment: UpdateComment):
        self._update_comment = update_comment
        self._update_comment.redo()

    def undo(self):
        if self._update_comment is not None:
            self._update_comment.undo()
        self._add_comment.undo()

    def redo(self):
        self._add_comment.redo()
        if self._update_comment is not None:
            self._update_comment.redo()
