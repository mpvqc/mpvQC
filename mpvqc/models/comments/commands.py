# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import bisect
from dataclasses import dataclass, replace
from operator import attrgetter
from typing import TYPE_CHECKING, ClassVar, Protocol

from mpvqc.datamodels import Comment

from .roles import Role
from .view_action import AnimatedSelection, NoViewAction, QuickSelection, QuickSelectionAndEdit, ViewAction

if TYPE_CHECKING:
    from collections.abc import Sequence

    from .store import Store, StoreItem


_sort_key = attrgetter("sort_key")


class Command(Protocol):
    invalidates_search: ClassVar[bool]

    def initial(self, store: Store, /) -> ViewAction: ...
    def focus_undo(self) -> int | None: ...
    def undo(self, store: Store, /) -> ViewAction: ...
    def focus_redo(self) -> int | None: ...
    def redo(self, store: Store, /) -> ViewAction: ...


@dataclass(frozen=True)
class AddComment:
    invalidates_search: ClassVar[bool] = True

    payload: StoreItem
    row: int

    @classmethod
    def build(cls, store: Store, *, time: int, comment_type: str) -> AddComment:
        return cls(
            payload=store.mint(Comment(time=time, comment_type=comment_type, comment="")),
            row=store.insert_position_for_new(time),
        )

    def initial(self, store: Store) -> ViewAction:
        store.insert(self.row, self.payload)
        return QuickSelectionAndEdit(row=self.row)

    def focus_undo(self) -> int | None:
        return self.row

    def undo(self, store: Store) -> ViewAction:
        store.remove(self.row)
        return NoViewAction()

    def focus_redo(self) -> int | None:
        return None

    def redo(self, store: Store) -> ViewAction:
        store.insert(self.row, self.payload)
        return QuickSelection(row=self.row)


@dataclass(frozen=True)
class RemoveComment:
    invalidates_search: ClassVar[bool] = True

    payload: StoreItem
    row: int

    @classmethod
    def build(cls, store: Store, *, row: int) -> RemoveComment:
        return cls(payload=store.item(row), row=row)

    def initial(self, store: Store) -> ViewAction:
        return self.redo(store)

    def focus_undo(self) -> int | None:
        return None

    def undo(self, store: Store) -> ViewAction:
        store.insert(self.row, self.payload)
        return QuickSelection(row=self.row)

    def focus_redo(self) -> int | None:
        return self.row

    def redo(self, store: Store) -> ViewAction:
        store.remove(self.row)
        return NoViewAction()


@dataclass(frozen=True)
class UpdateTime:
    invalidates_search: ClassVar[bool] = True

    old: Comment
    new: Comment
    src_row: int
    dst_row: int

    @classmethod
    def build(cls, store: Store, *, row: int, new_time: int) -> UpdateTime:
        old = store.item(row).comment
        new = replace(old, time=new_time)
        return cls(old=old, new=new, src_row=row, dst_row=store.insert_position_for_retimed(row, new_time))

    def initial(self, store: Store) -> ViewAction:
        return self.redo(store)

    def focus_undo(self) -> int | None:
        return self.dst_row

    def undo(self, store: Store) -> ViewAction:
        store.move_replace(self.dst_row, self.src_row, self.old, Role.TIME)
        return AnimatedSelection(row=self.src_row)

    def focus_redo(self) -> int | None:
        return self.src_row

    def redo(self, store: Store) -> ViewAction:
        store.move_replace(self.src_row, self.dst_row, self.new, Role.TIME)
        return AnimatedSelection(row=self.dst_row)


@dataclass(frozen=True)
class UpdateType:
    invalidates_search: ClassVar[bool] = False

    old: Comment
    new: Comment
    row: int

    @classmethod
    def build(cls, store: Store, *, row: int, new_comment_type: str) -> UpdateType:
        old = store.item(row).comment
        return cls(old=old, new=replace(old, comment_type=new_comment_type), row=row)

    def initial(self, store: Store) -> ViewAction:
        store.replace(self.row, self.new, Role.TYPE)
        return QuickSelection(row=self.row)

    def focus_undo(self) -> int | None:
        return self.row

    def undo(self, store: Store) -> ViewAction:
        store.replace(self.row, self.old, Role.TYPE)
        return AnimatedSelection(row=self.row)

    def focus_redo(self) -> int | None:
        return self.row

    def redo(self, store: Store) -> ViewAction:
        store.replace(self.row, self.new, Role.TYPE)
        return AnimatedSelection(row=self.row)


@dataclass(frozen=True)
class UpdateText:
    invalidates_search: ClassVar[bool] = True

    old: Comment
    new: Comment
    row: int

    @classmethod
    def build(cls, store: Store, *, row: int, new_text: str) -> UpdateText:
        old = store.item(row).comment
        return cls(old=old, new=replace(old, comment=new_text), row=row)

    def initial(self, store: Store) -> ViewAction:
        store.replace(self.row, self.new, Role.COMMENT)
        return QuickSelection(row=self.row)

    def focus_undo(self) -> int | None:
        return self.row

    def undo(self, store: Store) -> ViewAction:
        store.replace(self.row, self.old, Role.COMMENT)
        return AnimatedSelection(row=self.row)

    def focus_redo(self) -> int | None:
        return self.row

    def redo(self, store: Store) -> ViewAction:
        store.replace(self.row, self.new, Role.COMMENT)
        return AnimatedSelection(row=self.row)


@dataclass(frozen=True)
class AddAndUpdateText:
    invalidates_search: ClassVar[bool] = True

    payload: StoreItem
    row: int

    @classmethod
    def fuse(cls, add: AddComment, new_text: str) -> AddAndUpdateText:
        return cls(
            payload=replace(add.payload, comment=replace(add.payload.comment, comment=new_text)),
            row=add.row,
        )

    def initial(self, _: Store) -> ViewAction:
        msg = "Must never be called. It must never be pushed onto the stack in a normal operation"
        raise AssertionError(msg)

    def apply_fusion(self, store: Store) -> ViewAction:
        store.replace(self.row, self.payload.comment, Role.COMMENT)
        return QuickSelection(row=self.row)

    def focus_undo(self) -> int | None:
        return self.row

    def undo(self, store: Store) -> ViewAction:
        store.remove(self.row)
        return NoViewAction()

    def focus_redo(self) -> int | None:
        return None

    def redo(self, store: Store) -> ViewAction:
        store.insert(self.row, self.payload)
        return QuickSelection(row=self.row)


@dataclass(frozen=True)
class ClearComments:
    invalidates_search: ClassVar[bool] = True

    snapshot: tuple[StoreItem, ...]

    @classmethod
    def build(cls, store: Store) -> ClearComments:
        return cls(snapshot=store.snapshot())

    def initial(self, store: Store) -> ViewAction:
        return self.redo(store)

    def focus_undo(self) -> int | None:
        return None

    def undo(self, store: Store) -> ViewAction:
        store.reset(self.snapshot)
        return NoViewAction()

    def focus_redo(self) -> int | None:
        return None

    def redo(self, store: Store) -> ViewAction:
        store.reset([])
        return NoViewAction()


@dataclass(frozen=True)
class ImportComments:
    invalidates_search: ClassVar[bool] = True

    before: tuple[StoreItem, ...]
    after: tuple[StoreItem, ...]
    last_row: int
    previously_selected_row: int

    @classmethod
    def build(cls, store: Store, *, comments: Sequence[Comment], previously_selected_row: int) -> ImportComments:
        before = store.snapshot()
        new_rows = sorted((store.mint(c) for c in comments), key=_sort_key)
        after = tuple(sorted([*before, *new_rows], key=_sort_key))
        last_row = bisect.bisect_left(after, new_rows[-1].sort_key, key=_sort_key)
        return cls(before=before, after=after, last_row=last_row, previously_selected_row=previously_selected_row)

    def initial(self, store: Store) -> ViewAction:
        return self.redo(store)

    def focus_undo(self) -> int | None:
        return None

    def undo(self, store: Store) -> ViewAction:
        store.reset(self.before)
        return QuickSelection(row=self.previously_selected_row)

    def focus_redo(self) -> int | None:
        return None

    def redo(self, store: Store) -> ViewAction:
        store.reset(self.after)
        return QuickSelection(row=self.last_row)
