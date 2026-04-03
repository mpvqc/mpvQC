# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
from dataclasses import dataclass, field
from pathlib import Path

import inject
from PySide6.QtCore import QObject, Signal

from mpvqc.datamodels import Comment, VideoSource

from .document_importer import DocumentImporterService
from .player import PlayerService
from .settings import SettingsService
from .state import StateService
from .subtitle_importer import SubtitleImporterService

DocumentImportResult = DocumentImporterService.DocumentImportResult
SubtitleImportResult = SubtitleImporterService.SubtitleImportResult


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ScanResult:
    explicit_video_provided: bool
    found_videos: tuple[VideoSource, ...] = field(default_factory=tuple)
    found_subtitles: tuple[Path, ...] = field(default_factory=tuple)
    comments: tuple[Comment, ...] = field(default_factory=tuple)
    valid_documents: tuple[Path, ...] = field(default_factory=tuple)
    invalid_documents: tuple[Path, ...] = field(default_factory=tuple)


class ResourceScanner:
    _doc_importer = inject.attr(DocumentImporterService)
    _sub_importer = inject.attr(SubtitleImporterService)

    def scan(
        self,
        documents: list[Path],
        videos: list[Path],
        subtitles: list[Path],
    ) -> ScanResult:
        explicit_video_provided = bool(videos)

        document_result = self._doc_importer.NO_IMPORT
        doc_subtitles_result = self._sub_importer.NO_IMPORT
        subtitle_result = self._sub_importer.NO_IMPORT

        if documents:
            document_result = self._doc_importer.read(documents)
        if subs_from_docs := document_result.existing_subtitles:
            doc_subtitles_result = self._sub_importer.read(subs_from_docs)
        if subtitles:
            subtitle_result = self._sub_importer.read(subtitles)

        # dict.fromkeys preserves insertion order while deduplicating
        found_subtitles = tuple(
            dict.fromkeys(
                [
                    *subtitle_result.subtitles,
                    *document_result.existing_subtitles,
                ]
            )
        )

        if explicit_video_provided:
            found_videos = tuple(VideoSource(path=v, from_document=False, from_subtitle=False) for v in videos)
        else:
            found_videos = tuple(self._collect_videos(document_result, subtitle_result, doc_subtitles_result))

        return ScanResult(
            explicit_video_provided=explicit_video_provided,
            found_videos=found_videos,
            found_subtitles=found_subtitles,
            comments=document_result.comments,
            valid_documents=document_result.valid_documents,
            invalid_documents=document_result.invalid_documents,
        )

    def _collect_videos(
        self,
        document_result: DocumentImportResult,
        subtitle_result: SubtitleImportResult,
        doc_subtitles_result: SubtitleImportResult,
    ) -> list[VideoSource]:
        videos_from_documents = [
            VideoSource(path=video, from_document=True, from_subtitle=False)
            for video in document_result.existing_videos
        ]

        videos_from_subtitles = [
            VideoSource(path=video, from_document=False, from_subtitle=True)
            for video in subtitle_result.existing_videos
        ]

        videos_from_document_subtitles = [
            VideoSource(path=video, from_document=False, from_subtitle=True)
            for video in doc_subtitles_result.existing_videos
        ]

        all_videos = videos_from_documents + videos_from_subtitles + videos_from_document_subtitles
        return self._deduplicate_and_merge_video_sources(all_videos)

    @staticmethod
    def _deduplicate_and_merge_video_sources(videos: list[VideoSource]) -> list[VideoSource]:
        video_dict: dict[Path, VideoSource] = {}
        for video in videos:
            if existing := video_dict.get(video.path):
                video_dict[video.path] = VideoSource(
                    path=video.path,
                    from_document=existing.from_document or video.from_document,
                    from_subtitle=existing.from_subtitle or video.from_subtitle,
                )
            else:
                video_dict[video.path] = video
        return list(video_dict.values())


class ImporterService(QObject):
    _player = inject.attr(PlayerService)
    _settings = inject.attr(SettingsService)
    _state = inject.attr(StateService)

    # note: we actually emit with tuples but this would fall back to dynamic slot registration
    comments_ready_for_import = Signal(list)

    # param: tuple[str, ...] - tuple of file names that could not be processed
    erroneous_documents_imported = Signal(tuple)

    # param 1: tuple[VideoSource, ...] - found videos with source flags
    # param 2: tuple[Path, ...] - found subtitles
    ask_user_what_to_import = Signal(list, list)

    def __init__(self) -> None:
        super().__init__()
        self._scanner = ResourceScanner()
        self._pending_result: ScanResult | None = None

    def open(self, documents: list[Path], videos: list[Path], subtitles: list[Path]) -> None:
        self._pending_result = None

        result = self._scanner.scan(documents, videos, subtitles)

        if result.explicit_video_provided:
            self._handle_explicit_video_import(result)
            return

        if not result.found_videos:
            self.finalize_import(None, result.found_subtitles, result)
            return

        self._handle_found_videos(result)

    def _handle_explicit_video_import(self, result: ScanResult) -> None:
        found_videos = result.found_videos

        if len(found_videos) == 1:
            self.finalize_import(found_videos[0].path, result.found_subtitles, result)
            return

        self._ask_user_what_to_import(result)

    def _handle_found_videos(self, result: ScanResult) -> None:
        found_videos = result.found_videos

        if self._should_skip_video_import_because_already_loaded(found_videos):
            self.finalize_import(None, result.found_subtitles, result)
            return

        if len(found_videos) == 1:
            self._apply_video_import_preference(result, found_videos[0])
            return

        self._ask_user_what_to_import(result)

    def _should_skip_video_import_because_already_loaded(self, found_videos: tuple[VideoSource, ...]) -> bool:
        return any(self._player.is_video_loaded(v.path) for v in found_videos)

    def _apply_video_import_preference(self, result: ScanResult, video: VideoSource) -> None:
        setting = self._settings.import_found_video

        match setting:
            case SettingsService.ImportFoundVideo.ALWAYS.value:
                self.finalize_import(video.path, result.found_subtitles, result)
            case SettingsService.ImportFoundVideo.ASK_EVERY_TIME.value:
                self._ask_user_what_to_import(result)
            case SettingsService.ImportFoundVideo.NEVER.value:
                self.finalize_import(None, result.found_subtitles, result)
            case _:
                msg = f"Unknown import_found_video setting: {setting}"
                raise ValueError(msg)

    def _ask_user_what_to_import(self, result: ScanResult) -> None:
        self._pending_result = result
        self.ask_user_what_to_import.emit(result.found_videos, result.found_subtitles)

    def finalize_import(
        self,
        video: Path | None,
        subtitles: tuple[Path, ...],
        result: ScanResult | None = None,
    ) -> None:
        result = result or self._pending_result

        if result is None:
            logger.error("Cannot finalize import: no import state available")
            return

        if comments := result.comments:
            self.comments_ready_for_import.emit(comments)

        if video is not None:
            self._player.open_video(video)

        if subtitles:
            self._player.open_subtitles(subtitles)

        if video is not None or result.valid_documents:
            self._state.import_documents(
                documents=list(result.valid_documents),
                video=video,
                video_from_subtitle=self._is_video_from_subtitle_only(video, result.found_videos),
            )

        if invalid_documents := result.invalid_documents:
            self.erroneous_documents_imported.emit([p.name for p in invalid_documents])

    @staticmethod
    def _is_video_from_subtitle_only(video: Path | None, videos: tuple[VideoSource, ...]) -> bool:
        return video is not None and any(
            imported_video.path == video and not imported_video.from_document and imported_video.from_subtitle
            for imported_video in videos
        )
