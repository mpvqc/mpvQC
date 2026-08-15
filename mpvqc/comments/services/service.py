# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, assert_never

import inject
from PySide6.QtCore import QObject, Signal

from mpvqc.services import StateService

from .history import Applied, FocusFirst, History, NoStep
from .search import CommentSearchEngine
from .selection import SelectionCell
from .steps import (
    AddComment,
    ImportComments,
    RemoveComment,
    UpdateTime,
    UpdateType,
)
from .view_action import AnimatedSelection, NoViewAction, QuickSelection, QuickSelectionAndEdit

if TYPE_CHECKING:
    from collections.abc import Sequence

    from mpvqc.shared import Comment

    from .history import StepOutcome
    from .search import SearchOutcome
    from .store import Store
    from .view_action import ViewAction


class CommentsService(QObject):
    _state = inject.attr(StateService)

    view_action = Signal(object)  # ViewAction union; Qt sigs can't carry type aliases
    dirty = Signal()
    comments_changed = Signal()
    about_to_import = Signal()

    def __init__(self, store: Store, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._store = store
        self._selection = SelectionCell(parent=self)
        self._history = History(self._store, self._selection)
        self._search = CommentSearchEngine(self._store, self._selection)
        self.dirty.connect(self._state.record_change)

    @property
    def selection(self) -> SelectionCell:
        return self._selection

    @property
    def count(self) -> int:
        return self._store.rowCount()

    @property
    def distinct_comment_types(self) -> frozenset[str]:
        return self._store.distinct_comment_types()

    def comments(self) -> tuple[Comment, ...]:
        return self._store.comments()

    def comment_at(self, row: int) -> Comment:
        return self._store.item(row).comment

    def search(self, query: str, *, include_current_row: bool, top_down: bool) -> SearchOutcome:
        return self._search.search(query, include_current_row=include_current_row, top_down=top_down)

    def add_row(self, time: int, comment_type: str) -> None:
        step = AddComment.build(self._store, time=time, comment_type=comment_type)
        self._emit_applied(self._history.push(step))

    def update_comment(self, row: int, comment: str) -> None:
        self._emit_applied(self._history.update_text(row, comment))

    def update_comment_type(self, row: int, comment_type: str) -> None:
        step = UpdateType.build(self._store, row=row, new_comment_type=comment_type)
        self._emit_applied(self._history.push(step))

    def update_time(self, row: int, new_time: int) -> None:
        step = UpdateTime.build(self._store, row=row, new_time=new_time)
        self._emit_applied(self._history.push(step))

    def remove_row(self, row: int) -> None:
        step = RemoveComment.build(self._store, row=row)
        self._emit_applied(self._history.push(step))

    def import_comments(self, comments: Sequence[Comment]) -> None:
        if not comments:
            return
        self.about_to_import.emit()
        step = ImportComments.build(
            self._store,
            comments=comments,
            previously_selected_row=self._selection.row,
        )
        self._emit_applied(self._history.push(step))

    def reset(self) -> None:
        self._history.clear()
        self._search.invalidate()
        self._store.reset(())
        self._selection.clear_row()
        self.comments_changed.emit()

    def undo(self) -> None:
        self._dispatch_step(self._history.undo())

    def redo(self) -> None:
        self._dispatch_step(self._history.redo())

    def _dispatch_step(self, outcome: StepOutcome) -> None:
        match outcome:
            case NoStep():
                pass
            case FocusFirst(action=action):
                self._emit_view_action(action)
            case Applied() as applied:
                self._emit_applied(applied)
            case _ as unreachable:
                assert_never(unreachable)

    def _emit_applied(self, applied: Applied) -> None:
        self._search.invalidate()
        self.dirty.emit()
        self.comments_changed.emit()
        self._emit_view_action(applied.action)

    def _emit_view_action(self, action: ViewAction) -> None:
        match action:
            case QuickSelection(row=row) | AnimatedSelection(row=row) | QuickSelectionAndEdit(row=row):
                self._selection.set_row(row)
            case NoViewAction():
                pass
            case _ as unreachable:
                assert_never(unreachable)
        self.view_action.emit(action)
