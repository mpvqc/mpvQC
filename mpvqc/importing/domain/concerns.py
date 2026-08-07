# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import TYPE_CHECKING, assert_never

if TYPE_CHECKING:
    from pathlib import Path

    from .scan import ScanResult, SubtitleSource, VideoSource


@dataclass(frozen=True)
class SessionMerge:
    pass


@dataclass(frozen=True)
class SessionReplace:
    pass


@dataclass(frozen=True)
class SessionUnresolved:
    incoming_comment_count: int


type SessionResolved = SessionMerge | SessionReplace
type SessionConcern = SessionResolved | SessionUnresolved


class LoadFoundVideo(IntEnum):
    ALWAYS = 0
    ASK_EVERY_TIME = 1
    NEVER = 2


@dataclass(frozen=True)
class VideoLoad:
    path: Path


@dataclass(frozen=True)
class VideoSkip:
    pass


@dataclass(frozen=True)
class VideoUnresolved:
    candidates: tuple[VideoSource, ...]


type VideoResolved = VideoLoad | VideoSkip
type VideoConcern = VideoResolved | VideoUnresolved


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


def resolve_session(scan: ScanResult, *, has_existing_comments: bool) -> SessionConcern:
    if has_existing_comments and scan.comments:
        return SessionUnresolved(incoming_comment_count=len(scan.comments))
    return SessionMerge()


def resolve_video(
    scan: ScanResult,
    *,
    setting: LoadFoundVideo,
    any_candidate_loaded: bool,
) -> VideoConcern:
    explicit = tuple(v for v in scan.videos if v.explicitly_provided)
    if explicit:
        return _video_from_explicit(explicit)
    return _video_from_scan(scan.videos, setting=setting, already_loaded=any_candidate_loaded)


def _video_from_explicit(candidates: tuple[VideoSource, ...]) -> VideoConcern:
    if len(candidates) == 1:
        return VideoLoad(path=candidates[0].path)
    return VideoUnresolved(candidates=candidates)


def _video_from_scan(
    candidates: tuple[VideoSource, ...],
    *,
    setting: LoadFoundVideo,
    already_loaded: bool,
) -> VideoConcern:
    if not candidates:
        return VideoSkip()
    if len(candidates) > 1:
        return VideoUnresolved(candidates=candidates)
    if already_loaded:
        return VideoSkip()

    (only,) = candidates
    match setting:
        case LoadFoundVideo.ALWAYS:
            return VideoLoad(path=only.path)
        case LoadFoundVideo.ASK_EVERY_TIME:
            return VideoUnresolved(candidates=candidates)
        case LoadFoundVideo.NEVER:
            return VideoSkip()
        case _:
            assert_never(setting)


def resolve_subtitles(scan: ScanResult, *, video_concern: VideoConcern) -> SubtitlesConcern:
    explicit = tuple(s for s in scan.subtitles if s.explicitly_provided)
    if explicit:
        return _subtitles_from_explicit(explicit)
    return _subtitles_from_scan(scan, video_concern)


def _subtitles_from_explicit(candidates: tuple[SubtitleSource, ...]) -> SubtitlesConcern:
    return SubtitlesLoad(paths=tuple(c.path for c in candidates))


def _subtitles_from_scan(scan: ScanResult, video_concern: VideoConcern) -> SubtitlesConcern:
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
