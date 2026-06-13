# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import bisect
import itertools
from dataclasses import dataclass
from operator import attrgetter
from typing import TYPE_CHECKING, Any, Protocol, override

from PySide6.QtCore import QAbstractListModel, QModelIndex, QPersistentModelIndex, Qt, Signal

from .roles import ROLE_NAMES, Role

if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence

    from PySide6.QtCore import QByteArray, QObject

    from mpvqc.datamodels import Comment

_seq_counter = itertools.count()


@dataclass(frozen=True, slots=True)
class StoreItem:
    comment: Comment
    seq: int

    @property
    def sort_key(self) -> tuple[int, int]:
        return self.comment.time, self.seq


_sort_key = attrgetter("sort_key")


class Store(Protocol):
    def rowCount(self) -> int: ...
    def item(self, row: int) -> StoreItem: ...
    def snapshot(self) -> tuple[StoreItem, ...]: ...
    def search_rows(self, query: str) -> list[int]: ...
    def mint(self, comment: Comment) -> StoreItem: ...
    def insert_position_for_new(self, time: int) -> int: ...
    def insert_position_for_retimed(self, excluded_row: int, new_time: int) -> int: ...
    def insert(self, row: int, item: StoreItem) -> None: ...
    def remove(self, row: int) -> None: ...
    def replace(self, row: int, new_comment: Comment, role: Role) -> None: ...
    def move_replace(self, src: int, dst: int, new_comment: Comment, role: Role) -> None: ...
    def reset(self, items: Sequence[StoreItem]) -> None: ...


class CommentStore(QAbstractListModel):
    aboutToInsertRow = Signal(int)
    aboutToRemoveRow = Signal(int)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._rows: list[StoreItem] = []

    @override
    def rowCount(self, parent: QModelIndex | QPersistentModelIndex | None = None) -> int:
        if parent is not None and parent.isValid():
            return 0
        return len(self._rows)

    @override
    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid() or index.row() >= self.rowCount():
            return None
        comment = self._rows[index.row()].comment
        match role:
            case Role.TIME:
                return comment.time
            case Role.TYPE:
                return comment.comment_type
            case Role.COMMENT:
                return comment.comment
        return None

    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return ROLE_NAMES

    def item(self, row: int) -> StoreItem:
        if not 0 <= row < len(self._rows):
            msg = f"row {row} out of range (rowCount={len(self._rows)})"
            raise IndexError(msg)
        return self._rows[row]

    def snapshot(self) -> tuple[StoreItem, ...]:
        return tuple(self._rows)

    def iter_comments(self) -> Iterator[Comment]:
        return (r.comment for r in self._rows)

    def search_rows(self, query: str) -> list[int]:
        if not query:
            return []
        needle = query.casefold()
        return [i for i, r in enumerate(self._rows) if needle in r.comment.comment.casefold()]

    def mint(self, comment: Comment) -> StoreItem:
        return StoreItem(comment=comment, seq=next(_seq_counter))

    def insert_position_for_new(self, time: int) -> int:
        return bisect.bisect_right(self._rows, time, key=lambda r: r.comment.time)

    def insert_position_for_retimed(self, excluded_row: int, new_time: int) -> int:
        key = (new_time, self._rows[excluded_row].seq)
        n = len(self._rows)
        if excluded_row > 0 and _sort_key(self._rows[excluded_row - 1]) > key:
            return bisect.bisect_left(self._rows, key, hi=excluded_row, key=_sort_key)
        if excluded_row < n - 1 and _sort_key(self._rows[excluded_row + 1]) < key:
            return bisect.bisect_left(self._rows, key, lo=excluded_row + 1, key=_sort_key) - 1
        return excluded_row

    def insert(self, row: int, item: StoreItem) -> None:
        self.aboutToInsertRow.emit(row)
        self.beginInsertRows(QModelIndex(), row, row)
        self._rows.insert(row, item)
        self.endInsertRows()

    def remove(self, row: int) -> None:
        self.aboutToRemoveRow.emit(row)
        self.beginRemoveRows(QModelIndex(), row, row)
        del self._rows[row]
        self.endRemoveRows()

    def replace(self, row: int, new_comment: Comment, role: Role) -> None:
        self._rows[row] = StoreItem(new_comment, self._rows[row].seq)
        idx = self.index(row)
        self.dataChanged.emit(idx, idx, [role])

    def move_replace(self, src: int, dst: int, new_comment: Comment, role: Role) -> None:
        seq = self._rows[src].seq
        if src == dst:
            self._rows[src] = StoreItem(new_comment, seq)
            idx = self.index(src)
            self.dataChanged.emit(idx, idx, [role])
            return
        destination_child = dst if dst < src else dst + 1
        self.beginMoveRows(QModelIndex(), src, src, QModelIndex(), destination_child)
        self._rows.pop(src)
        self._rows.insert(dst, StoreItem(new_comment, seq))
        self.endMoveRows()
        new_idx = self.index(dst)
        self.dataChanged.emit(new_idx, new_idx, [role])

    def reset(self, items: Sequence[StoreItem]) -> None:
        self.beginResetModel()
        self._rows = list(items)
        self.endResetModel()
