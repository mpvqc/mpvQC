# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

import pytest

from mpvqc.services.player.state import (
    OBSERVED_PROPERTIES,
    ObservedProperty,
    PlayerState,
    RawPropertyValue,
    make_observer,
    reduce_update,
)


class ReduceCase(NamedTuple):
    name: str
    before: PlayerState
    prop: str
    raw: RawPropertyValue
    after: PlayerState


SCALAR_CASES = [
    ReduceCase("duration", PlayerState(), "duration", 120.5, PlayerState(duration=120.5)),
    ReduceCase("duration zero keeps default", PlayerState(), "duration", 0.0, PlayerState()),
    ReduceCase("percent-pos stores int", PlayerState(), "percent-pos", 51, PlayerState(percent_pos=51)),
    ReduceCase("time-pos stores int", PlayerState(), "time-pos", 66, PlayerState(time_pos=66)),
    ReduceCase("time-remaining stores int", PlayerState(), "time-remaining", 30, PlayerState(time_remaining=30)),
    ReduceCase("filename", PlayerState(), "filename", "video.mp4", PlayerState(filename="video.mp4")),
    ReduceCase("height", PlayerState(), "height", 1080, PlayerState(height=1080)),
    ReduceCase("width", PlayerState(), "width", 1920, PlayerState(width=1920)),
]


@pytest.mark.parametrize("case", SCALAR_CASES, ids=lambda case: case.name)
def test_reduces_scalar_properties(case: ReduceCase):
    assert reduce_update(case.before, case.prop, case.raw) == case.after


PATH_CASES = [
    ReduceCase(
        "load marks video loaded",
        PlayerState(),
        "path",
        "/movies/a.mkv",
        PlayerState(path="/movies/a.mkv", video_loaded=True),
    ),
    ReduceCase(
        "new path resets dimensions",
        PlayerState(path="/movies/a.mkv", video_loaded=True, width=1920, height=1080),
        "path",
        "/movies/b.mkv",
        PlayerState(path="/movies/b.mkv", video_loaded=True),
    ),
    ReduceCase(
        "same path keeps dimensions",
        PlayerState(path="/movies/a.mkv", video_loaded=True, width=1920, height=1080),
        "path",
        "/movies/a.mkv",
        PlayerState(path="/movies/a.mkv", video_loaded=True, width=1920, height=1080),
    ),
    ReduceCase(
        "unload keeps last path",
        PlayerState(path="/movies/a.mkv", video_loaded=True, width=1920, height=1080),
        "path",
        None,
        PlayerState(path="/movies/a.mkv", video_loaded=False, width=1920, height=1080),
    ),
]


@pytest.mark.parametrize("case", PATH_CASES, ids=lambda case: case.name)
def test_reduces_path(case: ReduceCase):
    assert reduce_update(case.before, case.prop, case.raw) == case.after


def _audio(count: int) -> list[dict]:
    return [{"type": "audio", "external": False, "external-filename": ""}] * count


def _internal_subs(count: int) -> list[dict]:
    return [{"type": "sub", "external": False, "external-filename": ""}] * count


def _external_sub(filename: str) -> dict:
    return {"type": "sub", "external": True, "external-filename": filename}


TRACK_LIST_CASES = [
    ReduceCase("empty track list", PlayerState(), "track-list", [], PlayerState()),
    ReduceCase(
        "audio tracks counted",
        PlayerState(),
        "track-list",
        _audio(3),
        PlayerState(audio_track_count=3),
    ),
    ReduceCase(
        "subtitle tracks counted",
        PlayerState(),
        "track-list",
        _internal_subs(2),
        PlayerState(subtitle_track_count=2),
    ),
    ReduceCase(
        "mixed tracks counted separately",
        PlayerState(),
        "track-list",
        [{"type": "video", "external": False, "external-filename": ""}, *_audio(2), *_internal_subs(1)],
        PlayerState(audio_track_count=2, subtitle_track_count=1),
    ),
    ReduceCase(
        "external subtitles collected sorted",
        PlayerState(),
        "track-list",
        [_external_sub("/work/b.srt"), _external_sub("/work/a.ass"), *_internal_subs(1)],
        PlayerState(
            subtitle_track_count=3,
            external_subtitles=(str(Path("/work/a.ass").resolve()), str(Path("/work/b.srt").resolve())),
        ),
    ),
    ReduceCase(
        "track removal shrinks counts",
        PlayerState(audio_track_count=2, subtitle_track_count=1),
        "track-list",
        _audio(1),
        PlayerState(audio_track_count=1),
    ),
]


@pytest.mark.parametrize("case", TRACK_LIST_CASES, ids=lambda case: case.name)
def test_reduces_track_list(case: ReduceCase):
    assert reduce_update(case.before, case.prop, case.raw) == case.after


LOADED = PlayerState(path="/movies/a.mkv", video_loaded=True, duration=120.5, width=1920, height=1080)

IGNORED_CASES = [
    ReduceCase("none duration", LOADED, "duration", None, LOADED),
    ReduceCase("none time-pos", LOADED, "time-pos", None, LOADED),
    ReduceCase("none track-list", LOADED, "track-list", None, LOADED),
]


@pytest.mark.parametrize("case", IGNORED_CASES, ids=lambda case: case.name)
def test_ignores_none_updates(case: ReduceCase):
    assert reduce_update(case.before, case.prop, case.raw) == case.after


@pytest.mark.parametrize(
    ("prop", "raw"),
    [
        ("volume", 50),
        ("duration", "not-a-number"),
        ("duration", 0),
    ],
)
def test_logs_and_ignores_malformed_updates(caplog: pytest.LogCaptureFixture, prop: str, raw: RawPropertyValue):
    state = PlayerState()

    assert reduce_update(state, prop, raw) is state
    assert prop in caplog.text


@pytest.mark.parametrize(
    ("width", "height", "expected"),
    [
        (0, 0, False),
        (1920, 0, False),
        (0, 1080, False),
        (1920, 1080, True),
    ],
)
def test_has_dimensions(width: int, height: int, expected: bool):
    assert PlayerState(width=width, height=height).has_dimensions is expected


def _spec(name: str) -> ObservedProperty:
    return next(spec for spec in OBSERVED_PROPERTIES if spec.name == name)


class ObserverCase(NamedTuple):
    name: str
    prop: str
    raws: list[RawPropertyValue]
    forwarded: list[RawPropertyValue]


OBSERVER_CASES = [
    ObserverCase("rounds and dedups within a second", "time-pos", [0.2, 0.3, 0.7], [0, 1]),
    ObserverCase("rounds and dedups within a percent", "percent-pos", [50.2, 50.7, 51.1], [50, 51]),
    ObserverCase("non-dedup property forwards duplicates", "path", ["/a", "/a", "/b"], ["/a", "/a", "/b"]),
    ObserverCase("forwards none through", "time-pos", [65.0, None], [65, None]),
    ObserverCase("dedups consecutive none", "time-pos", [None, None], [None]),
]


@pytest.mark.parametrize("case", OBSERVER_CASES, ids=lambda case: case.name)
def test_observer_forwards_expected_values(case: ObserverCase):
    forwarded: list[RawPropertyValue] = []
    observe = make_observer(_spec(case.prop), lambda _name, value: forwarded.append(value))

    for raw in case.raws:
        observe(None, raw)

    assert forwarded == case.forwarded


def test_observer_forwards_property_name():
    seen: list[tuple[str, RawPropertyValue]] = []
    observe = make_observer(_spec("time-pos"), lambda name, value: seen.append((name, value)))

    observe(None, 12.4)

    assert seen == [("time-pos", 12)]
