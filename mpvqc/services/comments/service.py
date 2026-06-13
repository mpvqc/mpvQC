# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, assert_never, cast

import inject
from PySide6.QtCore import QAbstractItemModel, QObject, Signal

from mpvqc.services.state import StateService

from .commands import (
    AddComment,
    ImportComments,
    RemoveComment,
    UpdateText,
    UpdateTime,
    UpdateType,
)
from .history import History
from .search import CommentSearchEngine
from .selection import SelectionState
from .store import CommentStore
from .view_action import AnimatedSelection, NoViewAction, QuickSelection, QuickSelectionAndEdit

if TYPE_CHECKING:
    from collections.abc import Sequence

    from mpvqc.datamodels import Comment, SearchResult

    from .commands import Command
    from .view_action import ViewAction


class CommentsService(QObject):
    _state = inject.attr(StateService)

    view_action = Signal(object)  # ViewAction union; Qt sigs can't carry type aliases
    dirty = Signal()
    about_to_import = Signal()

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._store = CommentStore(parent=self)
        self._selection = SelectionState(parent=self)
        self._history = History(self._store)
        self._search = CommentSearchEngine(self._store, self._selection)
        self._selection.selectedRowChanged.connect(self._history.disarm_merge)
        self.dirty.connect(self._state.record_change)

    @property
    def store(self) -> QAbstractItemModel:
        return self._store

    @property
    def selection(self) -> SelectionState:
        return self._selection

    @property
    def count(self) -> int:
        return self._store.rowCount()

    def comments(self) -> tuple[Comment, ...]:
        return self._store.comments()

    def comment_at(self, row: int) -> Comment:
        return self._store.item(row).comment

    def search(self, query: str, *, include_current_row: bool, top_down: bool) -> SearchResult:
        return self._search.search(query, include_current_row=include_current_row, top_down=top_down)

    def add_row(self, time: int, comment_type: str) -> None:
        cmd = AddComment.build(self._store, time=time, comment_type=comment_type)
        action = self._history.push(cmd)
        self._emit_apply(cmd, action)
        self._history.arm_merge(cmd)

    def update_comment(self, row: int, comment: str) -> None:
        if fused := self._history.try_fuse_text(row, comment):
            self._emit_apply(*fused)
            return
        cmd = UpdateText.build(self._store, row=row, new_text=comment)
        action = self._history.push(cmd)
        self._emit_apply(cmd, action)

    def update_comment_type(self, row: int, comment_type: str) -> None:
        cmd = UpdateType.build(self._store, row=row, new_comment_type=comment_type)
        action = self._history.push(cmd)
        self._emit_apply(cmd, action)

    def update_time(self, row: int, new_time: int) -> None:
        cmd = UpdateTime.build(self._store, row=row, new_time=new_time)
        action = self._history.push(cmd)
        self._emit_apply(cmd, action)

    def remove_row(self, row: int) -> None:
        cmd = RemoveComment.build(self._store, row=row)
        action = self._history.push(cmd)
        self._emit_apply(cmd, action)

    def import_comments(self, comments: Sequence[Comment]) -> None:
        if not comments:
            return
        self.about_to_import.emit()
        cmd = ImportComments.build(
            self._store,
            comments=comments,
            previously_selected_row=cast("int", self._selection.selectedRow),
        )
        action = self._history.push(cmd)
        self._emit_apply(cmd, action)

    def reset(self) -> None:
        self._history.clear()
        self._search.invalidate()
        self._store.reset(())
        # pyrefly: ignore [bad-assignment]
        self._selection.selectedRow = -1

    def undo(self) -> None:
        self._history.disarm_merge()
        if not self._history.has_undo():
            return
        target = self._history.undo_focus_target()
        if target is not None and self._needs_focus_phase(target):
            self._emit_view_action(AnimatedSelection(row=target))
            return
        self._emit_apply(*self._history.commit_undo())

    def redo(self) -> None:
        self._history.disarm_merge()
        if not self._history.has_redo():
            return
        target = self._history.redo_focus_target()
        if target is not None and self._needs_focus_phase(target):
            self._emit_view_action(AnimatedSelection(row=target))
            return
        self._emit_apply(*self._history.commit_redo())

    def _needs_focus_phase(self, target: int) -> bool:
        return cast("int", self._selection.selectedRow) != target or not self._selection.selectedRowVisible

    def _emit_apply(self, cmd: Command, action: ViewAction) -> None:
        if cmd.invalidates_search:
            self._search.invalidate()
        self.dirty.emit()
        self._emit_view_action(action)

    def _emit_view_action(self, action: ViewAction) -> None:
        match action:
            case QuickSelection(row=row) | AnimatedSelection(row=row) | QuickSelectionAndEdit(row=row):
                # pyrefly: ignore [bad-assignment]
                self._selection.selectedRow = row
            case NoViewAction():
                pass
            case _ as unreachable:
                assert_never(unreachable)
        self.view_action.emit(action)
