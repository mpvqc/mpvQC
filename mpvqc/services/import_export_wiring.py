# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

import inject
from loguru import logger
from PySide6.QtCore import QObject, Signal

from .document_exporter import DocumentExportService
from .document_importer import DocumentImporterService
from .player import PlayerService
from .settings import SettingsService
from .state import StateService
from .subtitle_importer import SubtitleImporterService
from .type_mapper import TypeMapperService

DocumentImportSetting = SettingsService.ImportWhenVideoLinkedInDocument
SubtitleImportSetting = SettingsService.ImportWhenVideoLinkedInSubtitle


@dataclass
class ImportState:
    imported_documents: DocumentImporterService.DocumentImportResult
    imported_subtitles: SubtitleImporterService.SubtitleImportResult
    dropped_videos: list[Path]
    document_videos: list[Path]
    subtitle_videos: list[Path]
    selected_video: Path | None = None
    asking_about_document: bool = False
    asking_about_subtitle: bool = False


class ImportExportWiringService(QObject):
    _document_importer: DocumentImporterService = inject.attr(DocumentImporterService)
    _exporter: DocumentExportService = inject.attr(DocumentExportService)
    _player: PlayerService = inject.attr(PlayerService)
    _settings: SettingsService = inject.attr(SettingsService)
    _subtitle_importer: SubtitleImporterService = inject.attr(SubtitleImporterService)
    _type_mapper: TypeMapperService = inject.attr(TypeMapperService)
    _state: StateService = inject.attr(StateService)

    # param: str | None - selected video path - ONLY REQUIRED FOR TESTS
    import_about_to_finish = Signal(object)

    # param: list[Comment] - list of comments to import
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

        self.comments_ready_for_import.emit(imported_documents.comments)

        state = ImportState(
            imported_documents=imported_documents,
            imported_subtitles=imported_subtitles,
            dropped_videos=videos,
            document_videos=imported_documents.existing_videos,
            subtitle_videos=imported_subtitles.existing_videos,
        )

        if self._determine_video(state):
            self._continue_with_import(state)

    def _determine_video(self, state: ImportState) -> bool:
        """Returns True if import can continue immediately, False if waiting for user input."""
        if state.dropped_videos:
            state.selected_video = state.dropped_videos[0]
            return True

        if state.document_videos:
            video_import_setting = self._settings.import_when_video_linked_in_document

            match video_import_setting:
                case DocumentImportSetting.ALWAYS.value:
                    state.selected_video = state.document_videos[0]
                    return True
                case DocumentImportSetting.NEVER.value if state.subtitle_videos:
                    return self._check_subtitle_video(state)
                case DocumentImportSetting.NEVER.value:
                    return True
                case DocumentImportSetting.ASK_EVERY_TIME.value:
                    import_id = str(uuid4())
                    state.asking_about_document = True
                    self._pending_imports[import_id] = state
                    self.ask_user_document_video_import.emit(import_id, state.document_videos[0].name)
                    return False

        if state.subtitle_videos:
            return self._check_subtitle_video(state)

        return True

    def _check_subtitle_video(self, state: ImportState) -> bool:
        """Returns True if import can continue immediately, False if waiting for user input."""
        subtitle_import_setting = self._settings.import_when_video_linked_in_subtitle

        match subtitle_import_setting:
            case SubtitleImportSetting.ALWAYS.value:
                state.selected_video = state.subtitle_videos[0]
                return True
            case SubtitleImportSetting.NEVER.value:
                return True
            case SubtitleImportSetting.ASK_EVERY_TIME.value:
                import_id = str(uuid4())
                state.asking_about_subtitle = True
                self._pending_imports[import_id] = state
                self.ask_user_subtitle_video_import.emit(import_id, state.subtitle_videos[0].name)
                return False
            case _:
                msg = f"Cannot handle subtitle import setting: {subtitle_import_setting}"
                raise ValueError(msg)

    def continue_video_determination(self, import_id: str, user_accepted: bool) -> None:
        if import_id not in self._pending_imports:
            logger.warning("No pending import state found for import_id: {}", import_id)
            return

        state = self._pending_imports.pop(import_id)

        if user_accepted:
            if state.asking_about_document:
                state.selected_video = state.document_videos[0]
            elif state.asking_about_subtitle:
                state.selected_video = state.subtitle_videos[0]
        elif state.asking_about_document and state.subtitle_videos:
            state.asking_about_document = False
            if self._check_subtitle_video(state):
                self._continue_with_import(state)
            return

        self._continue_with_import(state)

    def _continue_with_import(self, state: ImportState) -> None:
        self.import_about_to_finish.emit(state.selected_video)

        imported_video = state.selected_video

        if imported_video is not None:
            self._player.open_video(f"{imported_video}")

        if subtitles := state.imported_subtitles.subtitles:
            self._player.open_subtitles(subtitles=self._type_mapper.map_paths_to_str(subtitles))

        if imported_video is not None or state.imported_documents.valid_documents:
            self._state.import_documents(
                documents=state.imported_documents.valid_documents,
                video=imported_video,
            )

        if invalid_documents := state.imported_documents.invalid_documents:
            self.erroneous_documents_imported.emit([p.name for p in invalid_documents])
