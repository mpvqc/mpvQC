# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, assert_never

from .steps import AddAndUpdateText, AddComment, UpdateText
from .view_action import AnimatedSelection

if TYPE_CHECKING:
    from .selection import SelectionCell
    from .steps import FreshStep, Step
    from .store import Store
    from .view_action import ViewAction


@dataclass(frozen=True)
class NoStep:
    pass


@dataclass(frozen=True)
class FocusFirst:
    action: AnimatedSelection


@dataclass(frozen=True)
class NoFocusNeeded:
    pass


@dataclass(frozen=True)
class Applied:
    action: ViewAction


type StepOutcome = NoStep | FocusFirst | Applied
type FocusOutcome = FocusFirst | NoFocusNeeded


class _UndoStack:
    def __init__(self) -> None:
        self._undo: list[Step] = []
        self._redo: list[Step] = []

    def push(self, step: Step) -> None:
        self._redo.clear()
        self._undo.append(step)

    def clear(self) -> None:
        self._undo.clear()
        self._redo.clear()

    def replace_top(self, step: Step) -> None:
        self._undo[-1] = step

    @property
    def top_undo(self) -> Step | None:
        return self._undo[-1] if self._undo else None

    @property
    def top_redo(self) -> Step | None:
        return self._redo[-1] if self._redo else None

    def commit_undo(self) -> None:
        self._redo.append(self._undo.pop())

    def commit_redo(self) -> None:
        self._undo.append(self._redo.pop())


class History:
    def __init__(self, store: Store, selection: SelectionCell) -> None:
        self._store = store
        self._selection = selection
        self._stack = _UndoStack()
        self._armed_add: AddComment | None = None
        self._selection.row_selected.connect(self._disarm_merge)

    def push(self, step: FreshStep) -> Applied:
        self._disarm_merge()
        action = step.initial(self._store)
        self._stack.push(step)
        if isinstance(step, AddComment):
            self._armed_add = step
        return Applied(action=action)

    def clear(self) -> None:
        self._disarm_merge()
        self._stack.clear()

    def _disarm_merge(self) -> None:
        self._armed_add = None

    def update_text(self, row: int, new_text: str) -> Applied:
        add = self._armed_add
        if add is None or add.row != row:
            return self.push(UpdateText.build(self._store, row=row, new_text=new_text))
        merged = AddAndUpdateText.merge(add, new_text)
        action = merged.apply_merge(self._store)
        self._stack.replace_top(merged)
        self._disarm_merge()
        return Applied(action=action)

    def undo(self) -> StepOutcome:
        self._disarm_merge()
        step = self._stack.top_undo
        if step is None:
            return NoStep()
        focus = self._focus_first(step.focus_undo())
        match focus:
            case FocusFirst():
                return focus
            case NoFocusNeeded():
                action = step.undo(self._store)
                self._stack.commit_undo()
                return Applied(action=action)
            case _ as unreachable:
                assert_never(unreachable)

    def redo(self) -> StepOutcome:
        self._disarm_merge()
        step = self._stack.top_redo
        if step is None:
            return NoStep()
        focus = self._focus_first(step.focus_redo())
        match focus:
            case FocusFirst():
                return focus
            case NoFocusNeeded():
                action = step.redo(self._store)
                self._stack.commit_redo()
                return Applied(action=action)
            case _ as unreachable:
                assert_never(unreachable)

    def _focus_first(self, target: int | None) -> FocusOutcome:
        if target is None:
            return NoFocusNeeded()
        if self._selection.row == target and self._selection.row_visible:
            return NoFocusNeeded()
        return FocusFirst(action=AnimatedSelection(row=target))
