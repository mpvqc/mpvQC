# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, override

from PySide6.QtCore import QAbstractListModel, QByteArray, Qt

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Any

    from PySide6.QtCore import QModelIndex, QPersistentModelIndex


@dataclass(frozen=True, slots=True)
class _SubtitleEntry:
    path: Path
    checked: bool


class SubtitlesModel(QAbstractListModel):
    FilenameRole = Qt.ItemDataRole.UserRole + 1
    FullPathRole = Qt.ItemDataRole.UserRole + 2
    IsCheckedRole = Qt.ItemDataRole.UserRole + 3

    def __init__(self, subtitles: tuple[Path, ...]) -> None:
        super().__init__()
        self._items: list[_SubtitleEntry] = [_SubtitleEntry(path=subtitle, checked=True) for subtitle in subtitles]

    @property
    def checked_paths(self) -> tuple[Path, ...]:
        return tuple(item.path for item in self._items if item.checked)

    @property
    def checked_count(self) -> int:
        return sum(1 for item in self._items if item.checked)

    @override
    def rowCount(self, parent: QModelIndex | QPersistentModelIndex | None = None) -> int:
        if parent is not None and parent.isValid():
            return 0
        return len(self._items)

    @override
    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        items = self._items
        if not index.isValid() or index.row() >= len(items):
            return None

        item = items[index.row()]

        match role:
            case self.FilenameRole:
                return item.path.name
            case self.FullPathRole:
                return str(item.path)
            case self.IsCheckedRole:
                return item.checked

        return None

    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return {
            self.FilenameRole: QByteArray(b"filename"),
            self.FullPathRole: QByteArray(b"fullPath"),
            self.IsCheckedRole: QByteArray(b"isChecked"),
        }

    def toggle(self, index: int) -> None:
        if not 0 <= index < len(self._items):
            return

        item = self._items[index]
        self._items[index] = replace(item, checked=not item.checked)

        model_index = self.index(index, 0)
        self.dataChanged.emit(model_index, model_index, [self.IsCheckedRole])

    def set_all_checked(self, value: bool) -> None:
        if not self._items:
            return

        self._items = [replace(item, checked=value) for item in self._items]

        first_index = self.index(0, 0)
        last_index = self.index(len(self._items) - 1, 0)
        self.dataChanged.emit(first_index, last_index, [self.IsCheckedRole])
