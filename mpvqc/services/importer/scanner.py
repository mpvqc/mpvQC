# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import inject

from mpvqc.datamodels import SubtitleSource, VideoSource
from mpvqc.services.importer.documents import DocumentImporterService
from mpvqc.services.subtitle_importer import SubtitleImporterService

if TYPE_CHECKING:
    from pathlib import Path

    from mpvqc.datamodels import Comment


@dataclass(frozen=True)
class ScanResult:
    videos: tuple[VideoSource, ...]
    subtitles: tuple[SubtitleSource, ...]
    comments: tuple[Comment, ...]
    valid_documents: tuple[Path, ...]
    invalid_documents: tuple[Path, ...]


class ResourceScanner:
    _doc_importer = inject.attr(DocumentImporterService)
    _sub_importer = inject.attr(SubtitleImporterService)

    def scan(self, documents: list[Path], videos: list[Path], subtitles: list[Path]) -> ScanResult:
        doc_data = self._doc_importer.read(documents)

        subtitle_sources = [
            *(SubtitleSource(path=sub, explicitly_provided=True) for sub in subtitles),
            *(SubtitleSource(path=sub, found_in_document=True) for sub in doc_data.existing_subtitles),
        ]
        merged_subtitles = _merge_subtitle_sources(subtitle_sources)
        sub_data = self._sub_importer.read(tuple(s.path for s in merged_subtitles))

        video_sources = [
            *(VideoSource(path=video, explicitly_provided=True) for video in videos),
            *(VideoSource(path=video, found_in_document=True) for video in doc_data.existing_videos),
            *(VideoSource(path=video, found_in_subtitle=True) for video in sub_data.existing_videos),
        ]

        return ScanResult(
            videos=_merge_video_sources(video_sources),
            subtitles=merged_subtitles,
            comments=doc_data.comments,
            valid_documents=doc_data.valid_documents,
            invalid_documents=doc_data.invalid_documents,
        )


def _merge_video_sources(sources: list[VideoSource]) -> tuple[VideoSource, ...]:
    merged: dict[Path, VideoSource] = {}
    for source in sources:
        if existing := merged.get(source.path):
            merged[source.path] = VideoSource(
                path=source.path,
                explicitly_provided=existing.explicitly_provided or source.explicitly_provided,
                found_in_document=existing.found_in_document or source.found_in_document,
                found_in_subtitle=existing.found_in_subtitle or source.found_in_subtitle,
            )
        else:
            merged[source.path] = source
    return tuple(merged.values())


def _merge_subtitle_sources(sources: list[SubtitleSource]) -> tuple[SubtitleSource, ...]:
    merged: dict[Path, SubtitleSource] = {}
    for source in sources:
        if existing := merged.get(source.path):
            merged[source.path] = SubtitleSource(
                path=source.path,
                explicitly_provided=existing.explicitly_provided or source.explicitly_provided,
                found_in_document=existing.found_in_document or source.found_in_document,
            )
        else:
            merged[source.path] = source
    return tuple(merged.values())
