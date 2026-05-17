# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import typing
from dataclasses import dataclass
from typing import assert_never

from PySide6.QtCore import Property, QAbstractItemModel, QAbstractListModel, QByteArray, QObject, Qt, Signal
from PySide6.QtQml import QmlElement, QmlUncreatable

from mpvqc.services.importer.concerns import video

if typing.TYPE_CHECKING:
    from pathlib import Path
    from typing import Any

    from PySide6.QtCore import QModelIndex, QPersistentModelIndex

    from mpvqc.datamodels import VideoSource


QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


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

    @typing.override
    def rowCount(self, parent: QModelIndex | QPersistentModelIndex | None = None) -> int:
        return len(self._items)

    @typing.override
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

    @typing.override
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


@QmlElement
@QmlUncreatable("constructed by MpvqcImportWizardViewModel")
class MpvqcImportWizardVideoStepViewModel(QObject):
    selectedIndexChanged = Signal(int)

    def __init__(self, parent: QObject, inputs: video.Unresolved) -> None:
        super().__init__(parent)
        self._candidates = MpvqcImportVideosModel(inputs.candidates)
        self._selected_index = 0

    @Property(QAbstractItemModel, constant=True, final=True)
    def candidates(self) -> MpvqcImportVideosModel:
        return self._candidates

    @Property(int, notify=selectedIndexChanged, final=True)
    def selectedIndex(self) -> int:
        return self._selected_index

    @selectedIndex.setter
    def selectedIndex(self, value: int) -> None:
        if self._selected_index == value:
            return
        self._selected_index = value
        self.selectedIndexChanged.emit(value)

    @property
    def selected_path(self) -> Path | None:
        return self._candidates.path_at(self._selected_index)


def build_video_step(parent: QObject, concern: video.Concern) -> MpvqcImportWizardVideoStepViewModel | None:
    if isinstance(concern, video.Unresolved):
        return MpvqcImportWizardVideoStepViewModel(parent, concern)
    return None


def resolve_video(video_step: MpvqcImportWizardVideoStepViewModel | None, concern: video.Concern) -> video.Resolved:
    match concern:
        case video.Load() | video.Skip():
            return concern
        case video.Unresolved() if video_step is not None:
            if path := video_step.selected_path:
                return video.Load(path=path)
            return video.Skip()
        case video.Unresolved():
            msg = "video.Unresolved reached commit without a video step view-model"
            raise RuntimeError(msg)
        case _:
            assert_never(concern)
