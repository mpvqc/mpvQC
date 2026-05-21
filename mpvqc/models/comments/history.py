# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

from .commands import AddAndUpdateText, AddComment

if TYPE_CHECKING:
    from .commands import Command
    from .store import Store
    from .view_action import ViewAction


class _UndoStack:
    def __init__(self) -> None:
        self._undo: list[Command] = []
        self._redo: list[Command] = []

    def push(self, cmd: Command) -> None:
        self._redo.clear()
        self._undo.append(cmd)

    def replace_top(self, cmd: Command) -> None:
        self._undo[-1] = cmd

    @property
    def top_undo(self) -> Command | None:
        return self._undo[-1] if self._undo else None

    @property
    def top_redo(self) -> Command | None:
        return self._redo[-1] if self._redo else None

    def commit_undo(self) -> None:
        self._redo.append(self._undo.pop())

    def commit_redo(self) -> None:
        self._undo.append(self._redo.pop())


class History:
    def __init__(self, store: Store) -> None:
        self._store = store
        self._stack = _UndoStack()
        self._mergeable: AddComment | None = None

    def push(self, cmd: Command) -> ViewAction:
        self._mergeable = None
        action = cmd.initial(self._store)
        self._stack.push(cmd)
        return action

    def arm_merge(self, cmd: AddComment) -> None:
        self._mergeable = cmd

    def disarm_merge(self) -> None:
        self._mergeable = None

    def try_fuse_text(self, row: int, new_text: str) -> tuple[Command, ViewAction] | None:
        add = self._mergeable
        if add is None or add.row != row:
            return None
        fused = AddAndUpdateText.fuse(add, new_text)
        action = fused.apply_fusion(self._store)
        self._stack.replace_top(fused)
        self._mergeable = None
        return fused, action

    def has_undo(self) -> bool:
        return self._stack.top_undo is not None

    def undo_focus_target(self) -> int | None:
        cmd = self._stack.top_undo
        return cmd.focus_undo() if cmd is not None else None

    def commit_undo(self) -> tuple[Command, ViewAction]:
        cmd = self._stack.top_undo
        if cmd is None:
            msg = "commit_undo called with no top of stack; check has_undo first"
            raise RuntimeError(msg)
        action = cmd.undo(self._store)
        self._stack.commit_undo()
        return cmd, action

    def has_redo(self) -> bool:
        return self._stack.top_redo is not None

    def redo_focus_target(self) -> int | None:
        cmd = self._stack.top_redo
        return cmd.focus_redo() if cmd is not None else None

    def commit_redo(self) -> tuple[Command, ViewAction]:
        cmd = self._stack.top_redo
        if cmd is None:
            msg = "commit_redo called with no top of stack; check has_redo first"
            raise RuntimeError(msg)
        action = cmd.redo(self._store)
        self._stack.commit_redo()
        return cmd, action
