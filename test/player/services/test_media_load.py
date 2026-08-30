# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import NamedTuple

import pytest

from mpvqc.player.services import (
    IDLE,
    AttachSubtitles,
    DoNothing,
    LoadInFlight,
    LoadVideo,
    MediaCommand,
    MediaEvent,
    MediaLoadState,
    MediaRequested,
    VideoLoadFailed,
    VideoLoadSucceeded,
    reduce_media_load,
)

VIDEO_A = Path.home() / "a.mkv"
VIDEO_B = Path.home() / "b.mkv"
S1 = Path.home() / "one.srt"
S2 = Path.home() / "two.srt"
S3 = Path.home() / "three.srt"


def subtitles_alone(*subtitles: Path, video_loaded: bool) -> MediaRequested:
    return MediaRequested(video=None, subtitles=subtitles, video_loaded=video_loaded)


def video_with(video: Path, *subtitles: Path, video_loaded: bool = False) -> MediaRequested:
    return MediaRequested(video=video, subtitles=subtitles, video_loaded=video_loaded)


class FoldCase(NamedTuple):
    name: str
    before: MediaLoadState
    event: MediaEvent
    after: MediaLoadState
    command: MediaCommand


SUBTITLES_ALONE_CASES = [
    FoldCase(
        name="video on screen, nothing in flight: attach at once",
        before=IDLE,
        event=subtitles_alone(S1, S2, video_loaded=True),
        after=IDLE,
        command=AttachSubtitles((S1, S2)),
    ),
    FoldCase(
        name="no video, nothing in flight: wait for the next load",
        before=IDLE,
        event=subtitles_alone(S1, video_loaded=False),
        after=replace(IDLE, for_next_load=(S1,)),
        command=DoNothing(),
    ),
    FoldCase(
        name="waiting subtitles accumulate in order",
        before=replace(IDLE, for_next_load=(S1,)),
        event=subtitles_alone(S2, S3, video_loaded=False),
        after=replace(IDLE, for_next_load=(S1, S2, S3)),
        command=DoNothing(),
    ),
    FoldCase(
        name="load in flight, old video on screen: wait for the video that lands",
        before=replace(IDLE, in_flight=LoadInFlight((S1,))),
        event=subtitles_alone(S2, video_loaded=True),
        after=replace(IDLE, for_next_load=(S2,), in_flight=LoadInFlight((S1,))),
        command=DoNothing(),
    ),
    FoldCase(
        name="load in flight, no video on screen: wait for the video that lands",
        before=replace(IDLE, in_flight=LoadInFlight(())),
        event=subtitles_alone(S2, video_loaded=False),
        after=replace(IDLE, for_next_load=(S2,), in_flight=LoadInFlight(())),
        command=DoNothing(),
    ),
    FoldCase(
        name="nothing to attach: nothing happens",
        before=IDLE,
        event=subtitles_alone(video_loaded=True),
        after=IDLE,
        command=DoNothing(),
    ),
    FoldCase(
        name="nothing to wait for: nothing happens",
        before=IDLE,
        event=subtitles_alone(video_loaded=False),
        after=IDLE,
        command=DoNothing(),
    ),
]


@pytest.mark.parametrize("case", SUBTITLES_ALONE_CASES, ids=lambda case: case.name)
def test_subtitles_opened_alone(case: FoldCase):
    assert reduce_media_load(case.before, case.event) == (case.after, case.command)


VIDEO_REQUESTED_CASES = [
    FoldCase(
        name="video alone: load it, nothing in flight to carry",
        before=IDLE,
        event=video_with(VIDEO_A),
        after=replace(IDLE, in_flight=LoadInFlight(())),
        command=LoadVideo(VIDEO_A),
    ),
    FoldCase(
        name="video with subtitles: load it, the subtitles ride with the load",
        before=IDLE,
        event=video_with(VIDEO_A, S1, S2),
        after=replace(IDLE, in_flight=LoadInFlight((S1, S2))),
        command=LoadVideo(VIDEO_A),
    ),
    FoldCase(
        name="video on screen: the load replaces it, same as when none is",
        before=IDLE,
        event=video_with(VIDEO_A, S1, video_loaded=True),
        after=replace(IDLE, in_flight=LoadInFlight((S1,))),
        command=LoadVideo(VIDEO_A),
    ),
    FoldCase(
        name="second request while the first is in flight: the first's subtitles die with it",
        before=replace(IDLE, in_flight=LoadInFlight((S1,))),
        event=video_with(VIDEO_B, S2),
        after=replace(IDLE, in_flight=LoadInFlight((S2,))),
        command=LoadVideo(VIDEO_B),
    ),
    FoldCase(
        name="subtitles waiting for the next load keep waiting",
        before=replace(IDLE, for_next_load=(S1,)),
        event=video_with(VIDEO_A, S2),
        after=replace(IDLE, for_next_load=(S1,), in_flight=LoadInFlight((S2,))),
        command=LoadVideo(VIDEO_A),
    ),
]


@pytest.mark.parametrize("case", VIDEO_REQUESTED_CASES, ids=lambda case: case.name)
def test_video_requested(case: FoldCase):
    assert reduce_media_load(case.before, case.event) == (case.after, case.command)


LOAD_SUCCEEDED_CASES = [
    FoldCase(
        name="the load's own subtitles attach",
        before=replace(IDLE, in_flight=LoadInFlight((S1, S2))),
        event=VideoLoadSucceeded(),
        after=IDLE,
        command=AttachSubtitles((S1, S2)),
    ),
    FoldCase(
        name="subtitles waiting for the next load attach first, the load's own after",
        before=replace(IDLE, for_next_load=(S1,), in_flight=LoadInFlight((S2,))),
        event=VideoLoadSucceeded(),
        after=IDLE,
        command=AttachSubtitles((S1, S2)),
    ),
    FoldCase(
        name="a subtitle named twice attaches once",
        before=replace(IDLE, for_next_load=(S1, S2, S1), in_flight=LoadInFlight((S2, S3))),
        event=VideoLoadSucceeded(),
        after=IDLE,
        command=AttachSubtitles((S1, S2, S3)),
    ),
    FoldCase(
        name="a load the app did not ask for still takes the waiting subtitles",
        before=replace(IDLE, for_next_load=(S1,)),
        event=VideoLoadSucceeded(),
        after=IDLE,
        command=AttachSubtitles((S1,)),
    ),
    FoldCase(
        name="nothing waiting: nothing happens",
        before=replace(IDLE, in_flight=LoadInFlight(())),
        event=VideoLoadSucceeded(),
        after=IDLE,
        command=DoNothing(),
    ),
    FoldCase(
        name="idle: nothing happens",
        before=IDLE,
        event=VideoLoadSucceeded(),
        after=IDLE,
        command=DoNothing(),
    ),
]


@pytest.mark.parametrize("case", LOAD_SUCCEEDED_CASES, ids=lambda case: case.name)
def test_video_load_succeeded(case: FoldCase):
    assert reduce_media_load(case.before, case.event) == (case.after, case.command)


LOAD_FAILED_CASES = [
    FoldCase(
        name="the load's own subtitles die with it",
        before=replace(IDLE, in_flight=LoadInFlight((S1, S2))),
        event=VideoLoadFailed(),
        after=IDLE,
        command=DoNothing(),
    ),
    FoldCase(
        name="subtitles waiting for the next load survive it",
        before=replace(IDLE, for_next_load=(S1,), in_flight=LoadInFlight((S2,))),
        event=VideoLoadFailed(),
        after=replace(IDLE, for_next_load=(S1,)),
        command=DoNothing(),
    ),
    FoldCase(
        name="nothing in flight, as after a mid-playback error: nothing happens",
        before=replace(IDLE, for_next_load=(S1,)),
        event=VideoLoadFailed(),
        after=replace(IDLE, for_next_load=(S1,)),
        command=DoNothing(),
    ),
    FoldCase(
        name="idle: nothing happens",
        before=IDLE,
        event=VideoLoadFailed(),
        after=IDLE,
        command=DoNothing(),
    ),
]


@pytest.mark.parametrize("case", LOAD_FAILED_CASES, ids=lambda case: case.name)
def test_video_load_failed(case: FoldCase):
    assert reduce_media_load(case.before, case.event) == (case.after, case.command)


def test_a_failure_after_a_success_changes_nothing():
    landed, _ = reduce_media_load(replace(IDLE, in_flight=LoadInFlight((S1,))), VideoLoadSucceeded())

    assert reduce_media_load(landed, VideoLoadFailed()) == (IDLE, DoNothing())
