# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal, Slot

if TYPE_CHECKING:
    from pathlib import Path


@dataclass(frozen=True)
class ApplicationState:
    document: Path | None
    saved: bool

    @property
    def has_unsaved_document(self) -> bool:
        return not self.saved and self.document is not None


class StateService(QObject):
    saved_changed = Signal(bool)
    has_unsaved_document_changed = Signal(bool)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._state = ApplicationState(document=None, saved=True)

    @property
    def saved(self) -> bool:
        return self._state.saved

    @property
    def has_unsaved_document(self) -> bool:
        return self._state.has_unsaved_document

    @property
    def document(self) -> Path | None:
        return self._state.document

    def record_save(self, document: Path) -> None:
        new_state = replace(self._state, document=document, saved=True)
        self._set(new_state)

    @Slot()
    def record_change(self) -> None:
        new_state = replace(self._state, saved=False)
        self._set(new_state)

    def record_reset(self) -> None:
        new_state = replace(self._state, document=None, saved=True)
        self._set(new_state)

    def record_import(self) -> None:
        new_state = replace(self._state, document=None, saved=False)
        self._set(new_state)

    def _set(self, new_state: ApplicationState) -> None:
        was_saved = self._state.saved
        was_unsaved_document = self._state.has_unsaved_document
        self._state = new_state
        if was_saved != new_state.saved:
            self.saved_changed.emit(new_state.saved)
        if was_unsaved_document != new_state.has_unsaved_document:
            self.has_unsaved_document_changed.emit(new_state.has_unsaved_document)
