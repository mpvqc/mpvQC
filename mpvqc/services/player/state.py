# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
import pathlib
from dataclasses import dataclass, replace

logger = logging.getLogger(__name__)

type RawPropertyValue = float | int | str | list[dict] | None

OBSERVED_PROPERTIES = (
    "duration",
    "percent-pos",
    "time-pos",
    "time-remaining",
    "path",
    "filename",
    "height",
    "width",
    "track-list",
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
        case "percent-pos", float(value):
            percent_pos = int(value + 0.5)
            return state if percent_pos == state.percent_pos else replace(state, percent_pos=percent_pos)
        case "time-pos", float(value):
            time_pos = int(value + 0.5)
            return state if time_pos == state.time_pos else replace(state, time_pos=time_pos)
        case "time-remaining", float(value):
            time_remaining = int(value + 0.5)
            return state if time_remaining == state.time_remaining else replace(state, time_remaining=time_remaining)
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
