# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


@dataclass(frozen=True)
class MediaRequested:
    video: Path | None
    subtitles: tuple[Path, ...]
    video_loaded: bool


@dataclass(frozen=True)
class VideoLoadSucceeded:
    pass


@dataclass(frozen=True)
class VideoLoadFailed:
    pass


type MediaEvent = MediaRequested | VideoLoadSucceeded | VideoLoadFailed


@dataclass(frozen=True)
class NoLoadInFlight:
    pass


@dataclass(frozen=True)
class LoadInFlight:
    subtitles: tuple[Path, ...]


type InFlight = NoLoadInFlight | LoadInFlight


@dataclass(frozen=True)
class DoNothing:
    pass


@dataclass(frozen=True)
class LoadVideo:
    path: Path


@dataclass(frozen=True)
class AttachSubtitles:
    subtitles: tuple[Path, ...]


type MediaCommand = DoNothing | LoadVideo | AttachSubtitles


@dataclass(frozen=True)
class MediaLoadState:
    for_next_load: tuple[Path, ...]
    in_flight: InFlight


IDLE = MediaLoadState(for_next_load=(), in_flight=NoLoadInFlight())


def reduce_media_load(state: MediaLoadState, event: MediaEvent) -> tuple[MediaLoadState, MediaCommand]:
    match event:
        case MediaRequested():
            return _reduce_request(state, event)
        case VideoLoadSucceeded():
            return IDLE, _attach((*state.for_next_load, *_subtitles_in_flight(state.in_flight)))
        case VideoLoadFailed():
            return replace(state, in_flight=NoLoadInFlight()), DoNothing()


def _reduce_request(state: MediaLoadState, request: MediaRequested) -> tuple[MediaLoadState, MediaCommand]:
    if request.video is not None:
        return replace(state, in_flight=LoadInFlight(request.subtitles)), LoadVideo(request.video)
    match state.in_flight:
        case NoLoadInFlight() if request.video_loaded:
            return state, _attach(request.subtitles)
        case NoLoadInFlight() | LoadInFlight():
            return _wait_for_next_load(state, request.subtitles), DoNothing()


def _wait_for_next_load(state: MediaLoadState, subtitles: tuple[Path, ...]) -> MediaLoadState:
    return replace(state, for_next_load=(*state.for_next_load, *subtitles))


def _subtitles_in_flight(in_flight: InFlight) -> tuple[Path, ...]:
    match in_flight:
        case LoadInFlight(subtitles=subtitles):
            return subtitles
        case NoLoadInFlight():
            return ()


def _attach(subtitles: tuple[Path, ...]) -> MediaCommand:
    distinct = tuple(dict.fromkeys(subtitles))
    return AttachSubtitles(distinct) if distinct else DoNothing()
