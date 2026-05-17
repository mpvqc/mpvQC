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

    def apply_import(self, *, video: Path | None, has_comments: bool) -> None:
        new_state = _apply_import(self._state, video=video, has_comments=has_comments)
        self._set(new_state)

    def _set(self, new_state: ApplicationState) -> None:
        was_saved = self._state.saved
        self._state = new_state
        if was_saved != new_state.saved:
            self.saved_changed.emit(new_state.saved)


def _apply_import(state: ApplicationState, *, video: Path | None, has_comments: bool) -> ApplicationState:
    if not has_comments and _is_same_video(state.video, video):
        return state
    return replace(state, document=None, video=video or state.video)


def _is_same_video(current: Path | None, incoming: Path | None) -> bool:
    if current is None or incoming is None:
        return False
    return current.resolve() == incoming.resolve()
