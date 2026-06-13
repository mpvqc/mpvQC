# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
import pathlib
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

logger = logging.getLogger(__name__)

type RawPropertyValue = float | int | str | list[dict] | None


def float_to_int(value: float) -> int:
    return int(value + 0.5)


@dataclass(frozen=True)
class ObservedProperty:
    name: str
    dedup: bool = False
    transform: Callable[..., RawPropertyValue] | None = None


def make_observer(spec: ObservedProperty, emit: Callable[[str, RawPropertyValue], None]) -> Callable[..., None]:
    last: object = object()

    def observe(_: str, raw: RawPropertyValue) -> None:
        nonlocal last
        value = raw if raw is None or spec.transform is None else spec.transform(raw)
        if spec.dedup:
            if value == last:
                return
            last = value
        emit(spec.name, value)

    return observe


OBSERVED_PROPERTIES = (
    ObservedProperty("duration"),
    ObservedProperty("percent-pos", dedup=True, transform=float_to_int),
    ObservedProperty("time-pos", dedup=True, transform=float_to_int),
    ObservedProperty("time-remaining", dedup=True, transform=float_to_int),
    ObservedProperty("path"),
    ObservedProperty("filename"),
    ObservedProperty("height"),
    ObservedProperty("width"),
    ObservedProperty("track-list"),
)


@dataclass(frozen=True)
class PlayerState:
    duration: float = 0.0
    percent_pos: int = 0
    time_pos: int = 0
    time_remaining: int = 0
    path: str = ""
    video_loaded: bool = False
    filename: str = ""
    height: int = 0
    width: int = 0
    audio_track_count: int = 0
    subtitle_track_count: int = 0
    external_subtitles: tuple[str, ...] = ()

    @property
    def has_dimensions(self) -> bool:
        return self.width > 0 and self.height > 0


def reduce_update(state: PlayerState, name: str, raw: RawPropertyValue) -> PlayerState:
    match name, raw:
        case "path", (str() | None) as path_raw:
            return _reduce_path(state, path_raw)
        case _, None:
            return state
        case "track-list", list(tracks):
            return _reduce_track_list(state, tracks)
        case _:
            return _reduce_scalar(state, name, raw)


def _reduce_scalar(state: PlayerState, name: str, raw: RawPropertyValue) -> PlayerState:
    match name, raw:
        case "duration", float(value):
            return replace(state, duration=value)
        case "percent-pos", int(value):
            return replace(state, percent_pos=value)
        case "time-pos", int(value):
            return replace(state, time_pos=value)
        case "time-remaining", int(value):
            return replace(state, time_remaining=value)
        case "filename", str(value):
            return replace(state, filename=value)
        case "height", int(value):
            return replace(state, height=value)
        case "width", int(value):
            return replace(state, width=value)
        case _:
            logger.warning("Ignoring unexpected player property update: %s=%r", name, raw)
            return state


def _reduce_track_list(state: PlayerState, tracks: list[dict]) -> PlayerState:
    return replace(
        state,
        audio_track_count=_count_tracks(tracks, "audio"),
        subtitle_track_count=_count_tracks(tracks, "sub"),
        external_subtitles=_external_subtitles(tracks),
    )


def _reduce_path(state: PlayerState, raw: str | None) -> PlayerState:
    if raw is None:
        return replace(state, video_loaded=False)
    if raw == state.path:
        return replace(state, video_loaded=True)
    return replace(state, path=raw, video_loaded=True, width=0, height=0)


def _count_tracks(tracks: list[dict], track_type: str) -> int:
    return sum(1 for entry in tracks if entry.get("type") == track_type)


def _external_subtitles(tracks: list[dict]) -> tuple[str, ...]:
    external = {
        str(pathlib.Path(entry.get("external-filename", "")).resolve())
        for entry in tracks
        if entry.get("external") and entry.get("type") == "sub"
    }
    return tuple(sorted(external))
