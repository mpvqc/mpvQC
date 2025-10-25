# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

import inject
from loguru import logger
from PySide6.QtCore import QObject, Signal

from mpvqc.datamodels import Comment, VideoSource

from .document_importer import DocumentImporterService
from .player import PlayerService
from .settings import SettingsService
from .state import StateService
from .subtitle_importer import SubtitleImporterService
from .type_mapper import TypeMapperService

DocumentImportResult = DocumentImporterService.DocumentImportResult
SubtitleImportResult = SubtitleImporterService.SubtitleImportResult


class ResourceScanner:
    _doc_importer: DocumentImporterService = inject.attr(DocumentImporterService)
    _sub_importer: SubtitleImporterService = inject.attr(SubtitleImporterService)

    def __init__(self, documents: list[Path], videos: list[Path], subtitles: list[Path]):
        self._document_paths = documents
        self._subtitle_paths = subtitles

        self._document_import_result: DocumentImportResult = self._doc_importer.NO_IMPORT
        self._document_subtitles_import_result: SubtitleImportResult = self._sub_importer.NO_IMPORT
        self._subtitle_import_result: SubtitleImportResult = self._sub_importer.NO_IMPORT

        self._found_subtitles: list[Path] = []
        self._found_videos: list[VideoSource] = [
            VideoSource(path=video, from_document=False, from_subtitle=False) for video in videos
        ]
        self._explicit_video_provided = bool(videos)

    @property
    def explicit_video_provided(self) -> bool:
        return self._explicit_video_provided

    @property
    def is_single_document_import(self) -> bool:
        return len(self._document_paths) == 1 and not self._explicit_video_provided and not self._subtitle_paths

    @property
    def found_videos(self) -> list[VideoSource]:
        return self._found_videos

    @property
    def found_subtitles(self) -> list[Path]:
        return self._found_subtitles

    @property
    def comments(self) -> list[Comment]:
        return self._document_import_result.comments

    @property
    def valid_documents(self) -> list[Path]:
        return self._document_import_result.valid_documents

    @property
    def invalid_documents(self) -> list[Path]:
        return self._document_import_result.invalid_documents

    def scan(self):
        if documents := self._document_paths:
            self._document_import_result = self._doc_importer.read(documents)
        if subtitles := self._document_import_result.existing_subtitles:
            self._document_subtitles_import_result = self._sub_importer.read(subtitles)
        if subtitles := self._subtitle_paths:
            self._subtitle_import_result = self._sub_importer.read(subtitles)

        self._found_subtitles.extend(self._subtitle_import_result.subtitles)
        self._found_subtitles.extend(self._document_import_result.existing_subtitles)
        self._found_subtitles = list(dict.fromkeys(self._found_subtitles))

        if not self._explicit_video_provided:
            self._found_videos.extend(self._collect_and_merge_videos())

    def _collect_and_merge_videos(self) -> list[VideoSource]:
        videos_from_documents = [
            VideoSource(path=video, from_document=True, from_subtitle=False)
            for video in self._document_import_result.existing_videos
        ]

        videos_from_subtitles = [
            VideoSource(path=video, from_document=False, from_subtitle=True)
            for video in self._subtitle_import_result.existing_videos
        ]

        videos_from_document_subtitles = [
            VideoSource(path=video, from_document=False, from_subtitle=True)
            for video in self._document_subtitles_import_result.existing_videos
        ]

        all_videos = videos_from_documents + videos_from_subtitles + videos_from_document_subtitles

        video_dict: dict[Path, VideoSource] = {}
        for imported_video in all_videos:
            if imported_video.path in video_dict:
                existing = video_dict[imported_video.path]
                video_dict[imported_video.path] = VideoSource(
                    path=imported_video.path,
                    from_document=existing.from_document or imported_video.from_document,
                    from_subtitle=existing.from_subtitle or imported_video.from_subtitle,
                )
            else:
                video_dict[imported_video.path] = imported_video

        return list(video_dict.values())


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

    # param 1: list[VideoSource] - found videos with source flags
    # param 2: list[Path] - found subtitles
    ask_user_what_to_import = Signal(list, list)

    def __init__(self):
        super().__init__()
        self._pending_scanner: ResourceScanner | None = None

    def open(self, documents: list[Path], videos: list[Path], subtitles: list[Path]) -> None:
        self._pending_scanner = None

        scanner = ResourceScanner(documents, videos, subtitles)
        scanner.scan()

        found_videos = scanner.found_videos

        # Case 1: User provided videos directly (those take precedence)
        if scanner.explicit_video_provided:
            if len(found_videos) == 1:
                self.finalize_import(found_videos[0].path, scanner.found_subtitles, scanner)
                return

            self._ask_user_what_to_import(scanner, found_videos)
            return

        # Case 2: No videos found during scan
        if not found_videos:
            self.finalize_import(None, scanner.found_subtitles, scanner)
            return

        # Case 3: Videos found during scan
        if self._any_video_is_current_video_from(found_videos):
            self.finalize_import(None, scanner.found_subtitles, scanner)
            return

        if len(found_videos) == 1:
            self._apply_video_import_preference(scanner, found_videos[0])
            return

        self._ask_user_what_to_import(scanner, found_videos)

    def _ask_user_what_to_import(self, scanner: ResourceScanner, videos: list[VideoSource]) -> None:
        self._pending_scanner = scanner
        self.ask_user_what_to_import.emit(videos, scanner.found_subtitles)

    def _any_video_is_current_video_from(self, found_videos: list[VideoSource]) -> bool:
        return any(self._player.is_video_loaded(v.path) for v in found_videos)

    def _apply_video_import_preference(self, scanner: ResourceScanner, video: VideoSource) -> None:
        setting = self._settings.import_found_video

        match setting:
            case SettingsService.ImportFoundVideo.ALWAYS.value:
                self.finalize_import(video.path, scanner.found_subtitles, scanner)
            case SettingsService.ImportFoundVideo.ASK_EVERY_TIME.value:
                self._ask_user_what_to_import(scanner, [video])
            case SettingsService.ImportFoundVideo.NEVER.value:
                self.finalize_import(None, scanner.found_subtitles, scanner)
            case _:
                msg = f"Unknown import_found_video setting: {setting}"
                raise ValueError(msg)

    def finalize_import(
        self,
        video: Path | None,
        subtitles: list[Path],
        scanner: ResourceScanner | None = None,
    ) -> None:
        scanner = scanner or self._pending_scanner

        if scanner is None:
            logger.error("Cannot finalize import: no import state available")
            return

        if comments := scanner.comments:
            self.comments_ready_for_import.emit(comments)

        if video is not None:
            self._player.open_video(video)

        if subtitles:
            self._player.open_subtitles(subtitles)

        if video is not None or scanner.valid_documents:
            self._state.import_documents(
                documents=scanner.valid_documents,
                video=video,
                video_from_subtitle=self._is_video_from_subtitle_only(video, scanner.found_videos),
            )

        if invalid_documents := scanner.invalid_documents:
            self.erroneous_documents_imported.emit([p.name for p in invalid_documents])

    @staticmethod
    def _is_video_from_subtitle_only(video: Path | None, videos: list[VideoSource]) -> bool:
        return video is not None and any(
            imported_video.path == video and not imported_video.from_document and imported_video.from_subtitle
            for imported_video in videos
        )
