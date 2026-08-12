# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable
    from pathlib import Path

    from mpvqc.shared import Comment


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


class DocumentRejectionReason(Enum):
    INVALID = auto()
    UNSUPPORTED_VERSION = auto()


@dataclass(frozen=True)
class RejectedDocument:
    path: Path
    reason: DocumentRejectionReason


@dataclass(frozen=True)
class ScanResult:
    videos: tuple[VideoSource, ...]
    subtitles: tuple[SubtitleSource, ...]
    comments: tuple[Comment, ...]
    rejected_documents: tuple[RejectedDocument, ...]


def collect_video_sources(
    *,
    explicitly_provided: Iterable[Path],
    found_in_document: Iterable[Path],
    found_in_subtitle: Iterable[Path],
) -> tuple[VideoSource, ...]:
    """Callers hand in resolved paths: merging keys on path equality, so same path must mean same file."""
    merged: dict[Path, VideoSource] = {}
    for path in explicitly_provided:
        merged[path] = replace(merged.get(path, VideoSource(path=path)), explicitly_provided=True)
    for path in found_in_document:
        merged[path] = replace(merged.get(path, VideoSource(path=path)), found_in_document=True)
    for path in found_in_subtitle:
        merged[path] = replace(merged.get(path, VideoSource(path=path)), found_in_subtitle=True)
    return tuple(merged.values())


def collect_subtitle_sources(
    *,
    explicitly_provided: Iterable[Path],
    found_in_document: Iterable[Path],
) -> tuple[SubtitleSource, ...]:
    """Callers hand in resolved paths: merging keys on path equality, so same path must mean same file."""
    merged: dict[Path, SubtitleSource] = {}
    for path in explicitly_provided:
        merged[path] = replace(merged.get(path, SubtitleSource(path=path)), explicitly_provided=True)
    for path in found_in_document:
        merged[path] = replace(merged.get(path, SubtitleSource(path=path)), found_in_document=True)
    return tuple(merged.values())
