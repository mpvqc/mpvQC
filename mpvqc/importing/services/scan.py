# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import TYPE_CHECKING

from .reader import read_documents
from .subtitle_videos import find_videos_in_subtitles

if TYPE_CHECKING:
    from collections.abc import Iterable
    from pathlib import Path

    from mpvqc.shared import Comment

    from .reader import RejectedDocument


@dataclass(frozen=True)
class VideoSource:
    path: Path
    explicitly_provided: bool = False
    found_in_document: bool = False
    found_in_subtitle: bool = False


@dataclass(frozen=True)
class SubtitleSource:
    path: Path
    explicitly_provided: bool = False
    found_in_document: bool = False


@dataclass(frozen=True)
class ScanResult:
    videos: tuple[VideoSource, ...]
    subtitles: tuple[SubtitleSource, ...]
    comments: tuple[Comment, ...]
    rejected_documents: tuple[RejectedDocument, ...]


def scan(documents: tuple[Path, ...], videos: tuple[Path, ...], subtitles: tuple[Path, ...]) -> ScanResult:
    doc_data = read_documents(documents)

    merged_subtitles = _merge_subtitle_sources(
        explicitly_provided=subtitles,
        found_in_document=doc_data.existing_subtitles,
    )
    merged_videos = _merge_video_sources(
        explicitly_provided=videos,
        found_in_document=doc_data.existing_videos,
        found_in_subtitle=find_videos_in_subtitles(tuple(s.path for s in merged_subtitles)),
    )

    return ScanResult(
        videos=merged_videos,
        subtitles=merged_subtitles,
        comments=doc_data.comments,
        rejected_documents=doc_data.rejected_documents,
    )


def _merge_video_sources(
    *,
    explicitly_provided: Iterable[Path],
    found_in_document: Iterable[Path],
    found_in_subtitle: Iterable[Path],
) -> tuple[VideoSource, ...]:
    merged: dict[Path, VideoSource] = {}
    for path in explicitly_provided:
        resolved = path.resolve()
        merged[resolved] = replace(merged.get(resolved, VideoSource(path=resolved)), explicitly_provided=True)
    for path in found_in_document:
        resolved = path.resolve()
        merged[resolved] = replace(merged.get(resolved, VideoSource(path=resolved)), found_in_document=True)
    for path in found_in_subtitle:
        resolved = path.resolve()
        merged[resolved] = replace(merged.get(resolved, VideoSource(path=resolved)), found_in_subtitle=True)
    return tuple(merged.values())


def _merge_subtitle_sources(
    *,
    explicitly_provided: Iterable[Path],
    found_in_document: Iterable[Path],
) -> tuple[SubtitleSource, ...]:
    merged: dict[Path, SubtitleSource] = {}
    for path in explicitly_provided:
        resolved = path.resolve()
        merged[resolved] = replace(merged.get(resolved, SubtitleSource(path=resolved)), explicitly_provided=True)
    for path in found_in_document:
        resolved = path.resolve()
        merged[resolved] = replace(merged.get(resolved, SubtitleSource(path=resolved)), found_in_document=True)
    return tuple(merged.values())
