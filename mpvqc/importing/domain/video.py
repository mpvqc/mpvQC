# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import TYPE_CHECKING, assert_never

if TYPE_CHECKING:
    from pathlib import Path

    from .scan import ScanResult, VideoSource


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


def resolve_video(
    scan: ScanResult,
    *,
    setting: LoadFoundVideo,
    any_candidate_loaded: bool,
) -> VideoConcern:
    explicit = tuple(v for v in scan.videos if v.explicitly_provided)
    if explicit:
        return _from_explicit(explicit)
    return _from_scan(scan.videos, setting=setting, already_loaded=any_candidate_loaded)


def _from_explicit(candidates: tuple[VideoSource, ...]) -> VideoConcern:
    if len(candidates) == 1:
        return VideoLoad(path=candidates[0].path)
    return VideoUnresolved(candidates=candidates)


def _from_scan(
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
