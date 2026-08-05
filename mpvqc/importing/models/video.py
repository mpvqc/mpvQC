# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, override

from PySide6.QtCore import QAbstractListModel, QByteArray, Qt

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Any

    from PySide6.QtCore import QModelIndex, QPersistentModelIndex

    from mpvqc.importing.domain import VideoSource


@dataclass(frozen=True, slots=True)
class _VideoEntry:
    path: Path | None
    found_in_document: bool
    found_in_subtitle: bool


_SKIP_VIDEO_ENTRY = _VideoEntry(path=None, found_in_document=False, found_in_subtitle=False)


class MpvqcImportVideosModel(QAbstractListModel):
    FilenameRole = Qt.ItemDataRole.UserRole + 1
    FullPathRole = Qt.ItemDataRole.UserRole + 2
    FoundInDocumentRole = Qt.ItemDataRole.UserRole + 3
    FoundInSubtitleRole = Qt.ItemDataRole.UserRole + 4
    IsNoVideoRole = Qt.ItemDataRole.UserRole + 5

    def __init__(self, videos: tuple[VideoSource, ...]) -> None:
        super().__init__()
        self._items: list[_VideoEntry] = [
            _VideoEntry(
                path=source.path,
                found_in_document=source.found_in_document,
                found_in_subtitle=source.found_in_subtitle,
            )
            for source in videos
        ]
        self._items.append(_SKIP_VIDEO_ENTRY)

    @override
    def rowCount(self, parent: QModelIndex | QPersistentModelIndex | None = None) -> int:
        if parent is not None and parent.isValid():
            return 0
        return len(self._items)

    @override
    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid() or index.row() >= self.rowCount():
            return None

        item = self._items[index.row()]

        match role:
            case self.FilenameRole if item.path:
                return item.path.name
            case self.FilenameRole:
                return ""

            case self.FullPathRole if item.path:
                return str(item.path)
            case self.FullPathRole:
                return ""

            case self.FoundInDocumentRole:
                return item.found_in_document
            case self.FoundInSubtitleRole:
                return item.found_in_subtitle
            case self.IsNoVideoRole:
                return item.path is None

        return None

    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return {
            self.FilenameRole: QByteArray(b"filename"),
            self.FoundInDocumentRole: QByteArray(b"foundInDocument"),
            self.FoundInSubtitleRole: QByteArray(b"foundInSubtitle"),
            self.IsNoVideoRole: QByteArray(b"isNoVideo"),
            self.FullPathRole: QByteArray(b"fullPath"),
        }

    def path_at(self, index: int) -> Path | None:
        if 0 <= index < len(self._items):
            return self._items[index].path
        return None
