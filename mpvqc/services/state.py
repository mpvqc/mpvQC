# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from pathlib import Path

import inject
from PySide6.QtCore import Property, QObject, Signal

from .type_mapper import TypeMapperService


class StateService(QObject):
    saved_changed = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._state = ApplicationState(document=None, video=None, saved=True)

    # noinspection PyTypeChecker
    @Property(bool, notify=saved_changed)
    def saved(self) -> bool:
        return self._state.saved

    @property
    def document(self) -> Path | None:
        return self._state.document

    def _update_state(self, new_state: "ApplicationState") -> None:
        old_saved = self._state.saved
        self._state = new_state
        if old_saved != self._state.saved:
            self.saved_changed.emit(self._state.saved)

    def save(self, document: Path) -> None:
        new_state = reduce(self._state, SaveAction(document))
        self._update_state(new_state)

    def change(self) -> None:
        new_state = reduce(self._state, CHANGE_ACTION)
        self._update_state(new_state)

    def reset(self) -> None:
        new_state = reduce(self._state, RESET_ACTION)
        self._update_state(new_state)

    def import_documents(self, documents: list[Path], video: Path | None, video_from_subtitle: bool) -> None:
        change = ImportChange(documents, video, video_from_subtitle)
        new_state = reduce(self._state, ImportAction(change))
        self._update_state(new_state)


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


@dataclass(frozen=True)
class ApplicationState:
    document: Path | None
    video: Path | None
    saved: bool


@dataclass(frozen=True)
class ImportAction:
    change: ImportChange


@dataclass(frozen=True)
class SaveAction:
    document: Path


@dataclass(frozen=True)
class ChangeAction:
    pass


@dataclass(frozen=True)
class ResetAction:
    pass


CHANGE_ACTION = ChangeAction()
RESET_ACTION = ResetAction()

type Action = ImportAction | SaveAction | ChangeAction | ResetAction


def reduce(state: ApplicationState, action: Action) -> ApplicationState:
    match action:
        case SaveAction(document):
            return ApplicationState(document, state.video, saved=True)

        case ChangeAction():
            return ApplicationState(state.document, state.video, saved=False)

        case ResetAction():
            return ApplicationState(None, state.video, saved=True)

        case ImportAction(change):
            return _handle_import(state, change)


def _handle_import(state: ApplicationState, change: ImportChange) -> ApplicationState:
    is_initial_state = state.document is None and state.saved

    if is_initial_state:
        if change.only_video_imported:
            return ApplicationState(None, change.video, saved=True)

        video = change.video or state.video

        if change.exactly_one_document_imported:
            if change.video_from_subtitle:
                return ApplicationState(None, video, saved=True)
            return ApplicationState(change.imported_document, video, saved=True)

        return ApplicationState(None, video, saved=False)

    if state.video and change.only_video_imported and _is_same_video(state.video, change.video):
        return ApplicationState(state.document, state.video, state.saved)

    video = change.video or state.video
    return ApplicationState(None, video, saved=False)


def _is_same_video(current_video: Path | None, imported_video: Path | None) -> bool:
    if current_video is None or imported_video is None:
        return False

    mapper: TypeMapperService = inject.instance(TypeMapperService)
    current = mapper.map_path_to_str(current_video)
    imported = mapper.map_path_to_str(imported_video)
    return current == imported
