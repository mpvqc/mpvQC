# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import TYPE_CHECKING

from PySide6.QtCore import Property, QObject, Signal

if TYPE_CHECKING:
    from pathlib import Path


@dataclass(frozen=True)
class ApplicationState:
    document: Path | None
    video: Path | None
    saved: bool


@dataclass(frozen=True)
class ImportChange:
    documents: list[Path]
    video: Path | None
    video_from_subtitle: bool

    @property
    def only_video_imported(self) -> bool:
        return self.video is not None and not self.documents

    @property
    def exactly_one_document_imported(self) -> bool:
        return len(self.documents) == 1

    @property
    def imported_document(self) -> Path:
        return self.documents[0]


class StateService(QObject):
    saved_changed = Signal(bool)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._state = ApplicationState(document=None, video=None, saved=True)

    @Property(bool, notify=saved_changed)
    def saved(self) -> bool:
        return self._state.saved

    @property
    def document(self) -> Path | None:
        return self._state.document

    def save(self, document: Path) -> None:
        new_state = replace(self._state, document=document, saved=True)
        self._set(new_state)

    def change(self) -> None:
        new_state = replace(self._state, saved=False)
        self._set(new_state)

    def reset(self) -> None:
        new_state = replace(self._state, document=None, saved=True)
        self._set(new_state)

    def import_documents(self, documents: list[Path], video: Path | None, video_from_subtitle: bool) -> None:
        change = ImportChange(documents, video, video_from_subtitle)
        new_state = _apply_import(self._state, change)
        self._set(new_state)

    def _set(self, new_state: ApplicationState) -> None:
        was_saved = self._state.saved
        self._state = new_state
        if was_saved != new_state.saved:
            self.saved_changed.emit(new_state.saved)


def _apply_import(state: ApplicationState, change: ImportChange) -> ApplicationState:
    if _is_blank_state(state):
        return _apply_blank_state_import(state, change)
    if _is_redundant_video_reimport(state, change):
        return state
    return ApplicationState(None, change.video or state.video, saved=False)


def _is_blank_state(state: ApplicationState) -> bool:
    return state.document is None and state.saved


def _apply_blank_state_import(state: ApplicationState, change: ImportChange) -> ApplicationState:
    if change.only_video_imported:
        return ApplicationState(None, change.video, saved=True)

    video = change.video or state.video

    if change.exactly_one_document_imported:
        if change.video_from_subtitle:
            return ApplicationState(None, video, saved=True)
        return ApplicationState(change.imported_document, video, saved=True)

    return ApplicationState(None, video, saved=False)


def _is_redundant_video_reimport(state: ApplicationState, change: ImportChange) -> bool:
    return change.only_video_imported and _is_same_video(state.video, change.video)


def _is_same_video(current_video: Path | None, imported_video: Path | None) -> bool:
    if current_video is None or imported_video is None:
        return False
    return current_video.resolve() == imported_video.resolve()
