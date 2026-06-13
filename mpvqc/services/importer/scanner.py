# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from mpvqc.datamodels import SubtitleSource, VideoSource

from .reader import read_documents
from .subtitle_videos import find_videos_in_subtitles

if TYPE_CHECKING:
    from pathlib import Path

    from mpvqc.datamodels import Comment, RejectedDocument


@dataclass(frozen=True)
class ScanResult:
    videos: tuple[VideoSource, ...]
    subtitles: tuple[SubtitleSource, ...]
    comments: tuple[Comment, ...]
    rejected_documents: tuple[RejectedDocument, ...]


def scan(documents: list[Path], videos: list[Path], subtitles: list[Path]) -> ScanResult:
    doc_data = read_documents(documents)

    subtitle_sources = [
        *(SubtitleSource(path=sub.resolve(), explicitly_provided=True) for sub in subtitles),
        *(SubtitleSource(path=sub.resolve(), found_in_document=True) for sub in doc_data.existing_subtitles),
    ]
    merged_subtitles = _merge_subtitle_sources(subtitle_sources)
    subtitle_videos = find_videos_in_subtitles(tuple(s.path for s in merged_subtitles))

    video_sources = [
        *(VideoSource(path=video.resolve(), explicitly_provided=True) for video in videos),
        *(VideoSource(path=video.resolve(), found_in_document=True) for video in doc_data.existing_videos),
        *(VideoSource(path=video, found_in_subtitle=True) for video in subtitle_videos),
    ]

    return ScanResult(
        videos=_merge_video_sources(video_sources),
        subtitles=merged_subtitles,
        comments=doc_data.comments,
        rejected_documents=doc_data.rejected_documents,
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
