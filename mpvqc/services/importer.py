# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from uuid import uuid4

import inject
from loguru import logger
from PySide6.QtCore import QObject, Signal

from .document_importer import DocumentImporterService
from .player import PlayerService
from .settings import SettingsService
from .state import StateService
from .subtitle_importer import SubtitleImporterService
from .type_mapper import TypeMapperService


class AskingAbout(Enum):
    DOCUMENT = "document"
    SUBTITLE = "subtitle"


@dataclass
class ImportState:
    document_video: Path | None
    subtitle_video: Path | None
    dropped_videos: list[Path]
    valid_documents: list[Path]
    invalid_documents: list[Path]
    subtitles: list[Path]
    selected_video: Path | None = None
    asking_about: AskingAbout | None = None
    video_source: AskingAbout | None = None


class ImporterService(QObject):
    _document_importer: DocumentImporterService = inject.attr(DocumentImporterService)
    _player: PlayerService = inject.attr(PlayerService)
    _settings: SettingsService = inject.attr(SettingsService)
    _subtitle_importer: SubtitleImporterService = inject.attr(SubtitleImporterService)
    _type_mapper: TypeMapperService = inject.attr(TypeMapperService)
    _state: StateService = inject.attr(StateService)

    comments_ready_for_import = Signal(list)

    # param: list[str] - list of file names that could not be processed
    erroneous_documents_imported = Signal(list)

    # param 1: str - import ID (UUID)
    # param 2: str - file name of the video from document to potentially import
    ask_user_document_video_import = Signal(str, str)

    # param 1: str - import ID (UUID)
    # param 2: str - file name of the video from subtitle to potentially import
    ask_user_subtitle_video_import = Signal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pending_imports: dict[str, ImportState] = {}

    def open(self, documents: list[Path], videos: list[Path], subtitles: list[Path]) -> None:
        imported_documents = self._document_importer.read(documents)
        imported_subtitles = self._subtitle_importer.read(subtitles)

        if comments := imported_documents.comments:
            self.comments_ready_for_import.emit(comments)

        state = ImportState(
            document_video=self._get_importable_video(imported_documents.existing_videos),
            subtitle_video=self._get_importable_video(imported_subtitles.existing_videos),
            dropped_videos=videos,
            valid_documents=imported_documents.valid_documents,
            invalid_documents=imported_documents.invalid_documents,
            subtitles=imported_subtitles.subtitles,
        )

        if self._determine_video(state):
            self._continue_with_import(state)

    def _get_importable_video(self, videos: list[Path]) -> Path | None:
        if not videos:
            return None

        first_video = videos[0]
        if self._player.is_video_loaded(first_video):
            return None

        return first_video

    def _determine_video(self, state: ImportState) -> bool:
        """Returns True if import can continue immediately, False if waiting for user input."""
        if state.dropped_videos:
            state.selected_video = state.dropped_videos[0]
            return True

        if state.document_video:
            import_setting = self._settings.import_found_video

            match import_setting:
                case SettingsService.ImportFoundVideo.ALWAYS.value:
                    state.selected_video = state.document_video
                    return True
                case SettingsService.ImportFoundVideo.NEVER.value if state.subtitle_video:
                    return self._check_subtitle_video(state)
                case SettingsService.ImportFoundVideo.NEVER.value:
                    return True
                case SettingsService.ImportFoundVideo.ASK_EVERY_TIME.value:
                    import_id = str(uuid4())
                    state.asking_about = AskingAbout.DOCUMENT
                    self._pending_imports[import_id] = state
                    self.ask_user_document_video_import.emit(import_id, state.document_video.name)
                    return False

        if state.subtitle_video:
            return self._check_subtitle_video(state)

        return True

    def _check_subtitle_video(self, state: ImportState) -> bool:
        """Returns True if import can continue immediately, False if waiting for user input."""
        import_setting = self._settings.import_found_video

        match import_setting:
            case SettingsService.ImportFoundVideo.ALWAYS.value:
                state.selected_video = state.subtitle_video
                return True
            case SettingsService.ImportFoundVideo.NEVER.value:
                return True
            case SettingsService.ImportFoundVideo.ASK_EVERY_TIME.value:
                import_id = str(uuid4())
                state.asking_about = AskingAbout.SUBTITLE
                self._pending_imports[import_id] = state
                self.ask_user_subtitle_video_import.emit(import_id, state.subtitle_video.name)
                return False
            case _:
                msg = f"Cannot handle subtitle import setting: {import_setting}"
                raise ValueError(msg)

    def continue_video_determination(self, import_id: str, user_accepted: bool) -> None:
        if import_id not in self._pending_imports:
            logger.warning("No pending import state found for import_id: {}", import_id)
            return

        state = self._pending_imports.pop(import_id)

        match (user_accepted, state.asking_about):
            case (True, AskingAbout.DOCUMENT):
                state.selected_video = state.document_video
                state.video_source = AskingAbout.DOCUMENT
            case (True, AskingAbout.SUBTITLE):
                state.selected_video = state.subtitle_video
                state.video_source = AskingAbout.SUBTITLE
            case (False, AskingAbout.DOCUMENT) if state.subtitle_video:
                if not self._check_subtitle_video(state):
                    return

        self._continue_with_import(state)

    def _continue_with_import(self, state: ImportState) -> None:
        imported_video = state.selected_video

        if imported_video is not None:
            self._player.open_video(imported_video)

        if subtitles := state.subtitles:
            self._player.open_subtitles(subtitles=subtitles)

        if imported_video is not None or state.valid_documents:
            self._state.import_documents(
                documents=state.valid_documents,
                video=imported_video,
                video_from_subtitle=state.video_source == AskingAbout.SUBTITLE,
            )

        if invalid_documents := state.invalid_documents:
            self.erroneous_documents_imported.emit([p.name for p in invalid_documents])
