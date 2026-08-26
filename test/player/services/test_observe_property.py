# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass, fields
from typing import NamedTuple

import pytest

from mpvqc.player.services import PlayerState, RawPropertyValue

AUDIO_TRACKS = [{"type": "audio", "external": False, "external-filename": ""}]
SUBTITLE_TRACKS = [{"type": "sub", "external": False, "external-filename": ""}]
EXTERNAL_SUBTITLE_TRACKS = [{"type": "sub", "external": True, "external-filename": "/subtitles/a.srt"}]


class NotifierCase(NamedTuple):
    field: str
    property_name: str
    raw: RawPropertyValue


NOTIFIER_CASES = (
    NotifierCase(field="duration", property_name="duration", raw=120.5),
    NotifierCase(field="percent_pos", property_name="percent-pos", raw=51.0),
    NotifierCase(field="time_pos", property_name="time-pos", raw=66.0),
    NotifierCase(field="time_remaining", property_name="time-remaining", raw=30.0),
    NotifierCase(field="path", property_name="path", raw="/movies/a.mkv"),
    NotifierCase(field="video_loaded", property_name="path", raw="/movies/a.mkv"),
    NotifierCase(field="filename", property_name="filename", raw="a.mkv"),
    NotifierCase(field="height", property_name="height", raw=1080),
    NotifierCase(field="width", property_name="width", raw=1920),
    NotifierCase(field="audio_track_count", property_name="track-list", raw=AUDIO_TRACKS),
    NotifierCase(field="subtitle_track_count", property_name="track-list", raw=SUBTITLE_TRACKS),
    NotifierCase(field="external_subtitles", property_name="track-list", raw=EXTERNAL_SUBTITLE_TRACKS),
)


def test_the_notifier_cases_cover_every_state_field():
    assert {case.field for case in NOTIFIER_CASES} == {field.name for field in fields(PlayerState)}


@pytest.mark.parametrize("case", NOTIFIER_CASES, ids=lambda case: case.field)
def test_every_state_field_has_a_notifier(player_service, push_property, make_spy, case):
    spy = make_spy(getattr(player_service, f"{case.field}_changed"))

    push_property(case.property_name, case.raw)

    assert spy.count() == 1


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (0, None),
        (0.0, None),
        (120.5, 120.5),
        (None, None),
    ],
)
def test_duration_changed(player_service, push_property, make_spy, value, expected):
    spy = make_spy(player_service.duration_changed)

    push_property("duration", value)

    if expected is not None:
        assert spy.count() == 1
        assert spy.at(0, 0) == expected
    else:
        assert spy.count() == 0


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("/path/to/video.mp4", "/path/to/video.mp4"),
        (None, None),
    ],
)
def test_path_changed_emits_signal(player_service, push_property, make_spy, value, expected):
    spy = make_spy(player_service.path_changed)

    push_property("path", value)

    if expected is not None:
        assert spy.count() == 1
        assert spy.at(0, 0) == expected
    else:
        assert spy.count() == 0


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("/path/to/video.mp4", True),
        (None, None),
    ],
)
def test_path_changed_emits_video_loaded(player_service, push_property, make_spy, value, expected):
    spy = make_spy(player_service.video_loaded_changed)

    push_property("path", value)

    if expected is not None:
        assert spy.count() == 1
        assert spy.at(0, 0) == expected
    else:
        assert spy.count() == 0


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("video.mp4", "video.mp4"),
        (None, None),
    ],
)
def test_filename_changed_emits_signal(player_service, push_property, make_spy, value, expected):
    spy = make_spy(player_service.filename_changed)

    push_property("filename", value)

    if expected is not None:
        assert spy.count() == 1
        assert spy.at(0, 0) == expected
    else:
        assert spy.count() == 0


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (51, 51),
        (None, None),
    ],
)
def test_percent_pos_changed(player_service, push_property, make_spy, value, expected):
    spy = make_spy(player_service.percent_pos_changed)

    push_property("percent-pos", value)

    if expected is not None:
        assert spy.count() == 1
        assert spy.at(0, 0) == expected
    else:
        assert spy.count() == 0


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (66, 66),
        (None, None),
    ],
)
def test_time_pos_changed(player_service, push_property, make_spy, value, expected):
    spy = make_spy(player_service.time_pos_changed)

    push_property("time-pos", value)

    if expected is not None:
        assert spy.count() == 1
        assert spy.at(0, 0) == expected
    else:
        assert spy.count() == 0


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (30, 30),
        (None, None),
    ],
)
def test_time_remaining_changed(player_service, push_property, make_spy, value, expected):
    spy = make_spy(player_service.time_remaining_changed)

    push_property("time-remaining", value)

    if expected is not None:
        assert spy.count() == 1
        assert spy.at(0, 0) == expected
    else:
        assert spy.count() == 0


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (1080, 1080),
        (None, None),
    ],
)
def test_height_changed(player_service, push_property, make_spy, value, expected):
    spy = make_spy(player_service.height_changed)

    push_property("height", value)

    if expected is not None:
        assert spy.count() == 1
        assert spy.at(0, 0) == expected
    else:
        assert spy.count() == 0


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (1920, 1920),
        (None, None),
    ],
)
def test_width_changed(player_service, push_property, make_spy, value, expected):
    spy = make_spy(player_service.width_changed)

    push_property("width", value)

    if expected is not None:
        assert spy.count() == 1
        assert spy.at(0, 0) == expected
    else:
        assert spy.count() == 0


def test_video_dimensions_emitted_once_both_arrive(player_service, push_property, make_spy):
    spy = make_spy(player_service.video_dimensions_changed)

    push_property("path", "/movies/a.mkv")
    push_property("width", 1920)
    assert spy.count() == 0

    push_property("height", 1080)
    assert spy.count() == 1
    assert spy.at(0, 0) == 1920
    assert spy.at(0, 1) == 1080


class NewVideoCase(NamedTuple):
    name: str
    width: int
    height: int


@pytest.mark.parametrize(
    "case",
    [
        NewVideoCase("different resolution", 1280, 720),
        NewVideoCase("same resolution", 1920, 1080),
    ],
    ids=lambda case: case.name,
)
def test_video_dimensions_emitted_again_after_new_video(player_service, push_property, make_spy, case):
    push_property("path", "/movies/a.mkv")
    push_property("width", 1920)
    push_property("height", 1080)

    spy = make_spy(player_service.video_dimensions_changed)
    push_property("path", "/movies/b.mkv")
    push_property("width", case.width)
    push_property("height", case.height)

    assert spy.count() == 1
    assert spy.at(0, 0) == case.width
    assert spy.at(0, 1) == case.height


def test_property_updates_hop_through_the_marshal(qt_app, player_service, player_handle):
    player_handle.push_property("path", "/movies/a.mkv")

    assert not player_service.path
    qt_app.processEvents()
    assert player_service.path == "/movies/a.mkv"


@dataclass
class TrackCountTestCase:
    description: str
    track_list: list[dict]
    expected_audio_count: int
    expected_subtitle_count: int


@pytest.mark.parametrize(
    "test_case",
    [
        TrackCountTestCase(
            description="empty_track_list",
            track_list=[],
            expected_audio_count=0,
            expected_subtitle_count=0,
        ),
        TrackCountTestCase(
            description="single_audio_track",
            track_list=[
                {"type": "audio", "external": False, "external-filename": ""},
            ],
            expected_audio_count=1,
            expected_subtitle_count=0,
        ),
        TrackCountTestCase(
            description="single_subtitle_track",
            track_list=[
                {"type": "sub", "external": False, "external-filename": ""},
            ],
            expected_audio_count=0,
            expected_subtitle_count=1,
        ),
        TrackCountTestCase(
            description="multiple_audio_tracks",
            track_list=[
                {"type": "audio", "external": False, "external-filename": ""},
                {"type": "audio", "external": False, "external-filename": ""},
                {"type": "audio", "external": True, "external-filename": "/path/audio.mp3"},
            ],
            expected_audio_count=3,
            expected_subtitle_count=0,
        ),
        TrackCountTestCase(
            description="multiple_subtitle_tracks",
            track_list=[
                {"type": "sub", "external": False, "external-filename": ""},
                {"type": "sub", "external": True, "external-filename": "/path/sub.srt"},
            ],
            expected_audio_count=0,
            expected_subtitle_count=2,
        ),
        TrackCountTestCase(
            description="mixed_tracks",
            track_list=[
                {"type": "video", "external": False, "external-filename": ""},
                {"type": "audio", "external": False, "external-filename": ""},
                {"type": "audio", "external": False, "external-filename": ""},
                {"type": "sub", "external": False, "external-filename": ""},
                {"type": "sub", "external": True, "external-filename": "/path/sub.srt"},
                {"type": "sub", "external": True, "external-filename": "/path/sub2.ass"},
            ],
            expected_audio_count=2,
            expected_subtitle_count=3,
        ),
    ],
    ids=lambda tc: tc.description,
)
def test_track_list_changed_updates_counts(player_service, push_property, test_case):
    push_property("track-list", test_case.track_list)

    assert player_service.audio_track_count == test_case.expected_audio_count
    assert player_service.subtitle_track_count == test_case.expected_subtitle_count


def test_track_list_changed_emits_audio_signal(player_service, push_property, make_spy):
    spy = make_spy(player_service.audio_track_count_changed)
    track_list = [{"type": "audio", "external": False, "external-filename": ""}]

    push_property("track-list", track_list)

    assert spy.count() == 1
    assert spy.at(0, 0) == 1


def test_track_list_changed_emits_subtitle_signal(player_service, push_property, make_spy):
    spy = make_spy(player_service.subtitle_track_count_changed)
    track_list = [{"type": "sub", "external": False, "external-filename": ""}]

    push_property("track-list", track_list)

    assert spy.count() == 1
    assert spy.at(0, 0) == 1


def test_track_list_changed_does_not_emit_for_none(player_service, push_property, make_spy):
    audio_spy = make_spy(player_service.audio_track_count_changed)
    subtitle_spy = make_spy(player_service.subtitle_track_count_changed)

    push_property("track-list", None)

    assert audio_spy.count() == 0
    assert subtitle_spy.count() == 0


def test_track_list_changed_does_not_emit_when_count_unchanged(player_service, push_property, make_spy):
    track_list = [{"type": "audio", "external": False, "external-filename": ""}]
    push_property("track-list", track_list)

    spy = make_spy(player_service.audio_track_count_changed)
    push_property("track-list", track_list)

    assert spy.count() == 0


def test_track_list_changed_emits_only_changed_signal(player_service, push_property, make_spy):
    initial_list = [
        {"type": "audio", "external": False, "external-filename": ""},
        {"type": "sub", "external": False, "external-filename": ""},
    ]
    push_property("track-list", initial_list)

    audio_spy = make_spy(player_service.audio_track_count_changed)
    subtitle_spy = make_spy(player_service.subtitle_track_count_changed)

    updated_list = [
        {"type": "audio", "external": False, "external-filename": ""},
        {"type": "sub", "external": False, "external-filename": ""},
        {"type": "sub", "external": True, "external-filename": "/path/sub.srt"},
    ]
    push_property("track-list", updated_list)

    assert audio_spy.count() == 0
    assert subtitle_spy.count() == 1
    assert subtitle_spy.at(0, 0) == 2
