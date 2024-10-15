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

from typing import Callable

from PySide6.QtCore import QPersistentModelIndex
from PySide6.QtGui import QStandardItem, QStandardItemModel, QUndoCommand

from mpvqc.models import Comment

from .roles import Role


class MpvqcModelImportCommand(QUndoCommand):
    def __init__(
        self,
        model: QStandardItemModel,
        comments: list[Comment],
        selected_row: int,
        on_redo: Callable,
        on_undo: Callable,
    ):
        super().__init__()
        self._model = model
        self._comments = comments
        self._on_redo = on_redo
        self._on_undo = on_undo
        self._previously_selected_row = selected_row

        self._persistent_indices = []

    def undo(self):
        for index in self._persistent_indices:
            self._model.removeRow(index.row())

        self._on_undo(self._previously_selected_row)

    def redo(self):
        persistent_indices = []
        model_index = None

        for comment in self._comments:
            item = QStandardItem()

            item.setData(comment.time, Role.TIME)
            item.setData(comment.comment_type, Role.TYPE)
            item.setData(comment.comment, Role.COMMENT)

            self._model.appendRow(item)

            model_index = QPersistentModelIndex(item.index())
            persistent_indices.append(model_index)

        self._persistent_indices = persistent_indices
        self._on_redo(model_index)
