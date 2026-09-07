# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

import pytest

from mpvqc.player.services import (
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
    ReduceCase(
        name="duration",
        before=PlayerState(),
        prop="duration",
        raw=120.5,
        after=PlayerState(duration=120.5),
    ),
    ReduceCase(
        name="duration zero keeps default",
        before=PlayerState(),
        prop="duration",
        raw=0.0,
        after=PlayerState(),
    ),
    ReduceCase(
        name="percent-pos stores int",
        before=PlayerState(),
        prop="percent-pos",
        raw=51,
        after=PlayerState(percent_pos=51),
    ),
    ReduceCase(
        name="time-pos stores int",
        before=PlayerState(),
        prop="time-pos",
        raw=66,
        after=PlayerState(time_pos=66),
    ),
    ReduceCase(
        name="time-remaining stores int",
        before=PlayerState(),
        prop="time-remaining",
        raw=30,
        after=PlayerState(time_remaining=30),
    ),
    ReduceCase(
        name="filename",
        before=PlayerState(),
        prop="filename",
        raw="video.mp4",
        after=PlayerState(filename="video.mp4"),
    ),
    ReduceCase(
        name="height",
        before=PlayerState(),
        prop="height",
        raw=1080,
        after=PlayerState(height=1080),
    ),
    ReduceCase(
        name="width",
        before=PlayerState(),
        prop="width",
        raw=1920,
        after=PlayerState(width=1920),
    ),
]


@pytest.mark.parametrize("case", SCALAR_CASES, ids=lambda case: case.name)
def test_reduces_scalar_properties(case: ReduceCase):
    assert reduce_update(case.before, case.prop, case.raw) == case.after


PATH_CASES = [
    ReduceCase(
        name="load marks video loaded",
        before=PlayerState(),
        prop="path",
        raw="/movies/a.mkv",
        after=PlayerState(path="/movies/a.mkv", video_loaded=True),
    ),
    ReduceCase(
        name="new path resets dimensions",
        before=PlayerState(path="/movies/a.mkv", video_loaded=True, width=1920, height=1080),
        prop="path",
        raw="/movies/b.mkv",
        after=PlayerState(path="/movies/b.mkv", video_loaded=True),
    ),
    ReduceCase(
        name="same path keeps dimensions",
        before=PlayerState(path="/movies/a.mkv", video_loaded=True, width=1920, height=1080),
        prop="path",
        raw="/movies/a.mkv",
        after=PlayerState(path="/movies/a.mkv", video_loaded=True, width=1920, height=1080),
    ),
    ReduceCase(
        name="unload keeps last path",
        before=PlayerState(path="/movies/a.mkv", video_loaded=True, width=1920, height=1080),
        prop="path",
        raw=None,
        after=PlayerState(path="/movies/a.mkv", video_loaded=False, width=1920, height=1080),
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
    ReduceCase(
        name="empty track list",
        before=PlayerState(),
        prop="track-list",
        raw=[],
        after=PlayerState(),
    ),
    ReduceCase(
        name="audio tracks counted",
        before=PlayerState(),
        prop="track-list",
        raw=_audio(3),
        after=PlayerState(audio_track_count=3),
    ),
    ReduceCase(
        name="subtitle tracks counted",
        before=PlayerState(),
        prop="track-list",
        raw=_internal_subs(2),
        after=PlayerState(subtitle_track_count=2),
    ),
    ReduceCase(
        name="mixed tracks counted separately",
        before=PlayerState(),
        prop="track-list",
        raw=[{"type": "video", "external": False, "external-filename": ""}, *_audio(2), *_internal_subs(1)],
        after=PlayerState(audio_track_count=2, subtitle_track_count=1),
    ),
    ReduceCase(
        name="external subtitles collected sorted",
        before=PlayerState(),
        prop="track-list",
        raw=[_external_sub("/work/b.srt"), _external_sub("/work/a.ass"), *_internal_subs(1)],
        after=PlayerState(
            subtitle_track_count=3,
            external_subtitles=(str(Path("/work/a.ass").resolve()), str(Path("/work/b.srt").resolve())),
        ),
    ),
    ReduceCase(
        name="track removal shrinks counts",
        before=PlayerState(audio_track_count=2, subtitle_track_count=1),
        prop="track-list",
        raw=_audio(1),
        after=PlayerState(audio_track_count=1),
    ),
]


@pytest.mark.parametrize("case", TRACK_LIST_CASES, ids=lambda case: case.name)
def test_reduces_track_list(case: ReduceCase):
    assert reduce_update(case.before, case.prop, case.raw) == case.after


LOADED = PlayerState(path="/movies/a.mkv", video_loaded=True, duration=120.5, width=1920, height=1080)

IGNORED_CASES = [
    ReduceCase(name="none duration", before=LOADED, prop="duration", raw=None, after=LOADED),
    ReduceCase(name="none time-pos", before=LOADED, prop="time-pos", raw=None, after=LOADED),
    ReduceCase(name="none track-list", before=LOADED, prop="track-list", raw=None, after=LOADED),
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


class DimensionsCase(NamedTuple):
    width: int
    height: int
    expected: bool


@pytest.mark.parametrize(
    ("width", "height", "expected"),
    [
        DimensionsCase(width=0, height=0, expected=False),
        DimensionsCase(width=1920, height=0, expected=False),
        DimensionsCase(width=0, height=1080, expected=False),
        DimensionsCase(width=1920, height=1080, expected=True),
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
    ObserverCase(
        name="rounds and dedups within a second",
        prop="time-pos",
        raws=[0.2, 0.3, 0.7],
        forwarded=[0, 1],
    ),
    ObserverCase(
        name="rounds and dedups within a percent",
        prop="percent-pos",
        raws=[50.2, 50.7, 51.1],
        forwarded=[50, 51],
    ),
    ObserverCase(
        name="non-dedup property forwards duplicates",
        prop="path",
        raws=["/a", "/a", "/b"],
        forwarded=["/a", "/a", "/b"],
    ),
    ObserverCase(
        name="forwards none through",
        prop="time-pos",
        raws=[65.0, None],
        forwarded=[65, None],
    ),
    ObserverCase(
        name="dedups consecutive none",
        prop="time-pos",
        raws=[None, None],
        forwarded=[None],
    ),
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
