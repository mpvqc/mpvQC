# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .video import VideoSkip, VideoUnresolved

if TYPE_CHECKING:
    from pathlib import Path

    from .scan import ScanResult, SubtitleSource, VideoSource
    from .video import VideoConcern


@dataclass(frozen=True)
class SubtitlesLoad:
    paths: tuple[Path, ...]


@dataclass(frozen=True)
class SubtitlesSkip:
    pass


@dataclass(frozen=True)
class SubtitlesUnresolved:
    candidates: tuple[Path, ...]


type SubtitlesResolved = SubtitlesLoad | SubtitlesSkip
type SubtitlesConcern = SubtitlesResolved | SubtitlesUnresolved


def resolve_subtitles(scan: ScanResult, *, video_concern: VideoConcern) -> SubtitlesConcern:
    explicit = tuple(s for s in scan.subtitles if s.explicitly_provided)
    if explicit:
        return _from_explicit(explicit)
    return _from_scan(scan, video_concern)


def _from_explicit(candidates: tuple[SubtitleSource, ...]) -> SubtitlesConcern:
    return SubtitlesLoad(paths=tuple(c.path for c in candidates))


def _from_scan(scan: ScanResult, video_concern: VideoConcern) -> SubtitlesConcern:
    candidates = scan.subtitles
    if isinstance(video_concern, VideoSkip) or not candidates:
        return SubtitlesSkip()
    if isinstance(video_concern, VideoUnresolved):
        return SubtitlesUnresolved(candidates=tuple(c.path for c in candidates))
    if _explicit_video_overrides_doc(scan.videos):
        return SubtitlesUnresolved(candidates=tuple(c.path for c in candidates))
    return SubtitlesLoad(paths=tuple(c.path for c in candidates))


def _explicit_video_overrides_doc(videos: tuple[VideoSource, ...]) -> bool:
    explicit_paths = {v.path for v in videos if v.explicitly_provided}
    if not explicit_paths:
        return False
    doc_paths = {v.path for v in videos if v.found_in_document}
    return explicit_paths.isdisjoint(doc_paths)
