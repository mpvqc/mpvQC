# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass

import pytest


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (0, None),
        (0.0, None),
        (120.5, 120.5),
        (None, None),
    ],
)
def test_duration_changed(player_service, make_spy, value, expected):
    spy = make_spy(player_service.duration_changed)

    player_service._duration_prop.on_update(value)

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
def test_path_changed_emits_signal(player_service, make_spy, value, expected):
    spy = make_spy(player_service.path_changed)

    player_service._path_prop.on_update(value)

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
def test_path_changed_emits_video_loaded(player_service, make_spy, value, expected):
    spy = make_spy(player_service.video_loaded_changed)

    player_service._video_loaded_prop.on_update(value)

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
def test_filename_changed_emits_signal(player_service, make_spy, value, expected):
    spy = make_spy(player_service.filename_changed)

    player_service._filename_prop.on_update(value)

    if expected is not None:
        assert spy.count() == 1
        assert spy.at(0, 0) == expected
    else:
        assert spy.count() == 0


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (50.7, 51),
        (None, None),
    ],
)
def test_percent_pos_changed(player_service, make_spy, value, expected):
    spy = make_spy(player_service.percent_pos_changed)

    player_service._percent_pos_prop.on_update(value)

    if expected is not None:
        assert spy.count() == 1
        assert spy.at(0, 0) == expected
    else:
        assert spy.count() == 0


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (65.8, 66),
        (None, None),
    ],
)
def test_time_pos_changed(player_service, make_spy, value, expected):
    spy = make_spy(player_service.time_pos_changed)

    player_service._time_pos_prop.on_update(value)

    if expected is not None:
        assert spy.count() == 1
        assert spy.at(0, 0) == expected
    else:
        assert spy.count() == 0


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (0.499999, 0),
        (0.500000, 1),
        (0.500001, 1),
        (1.499999, 1),
        (1.500001, 2),
        (None, 0),
    ],
)
def test_time_pos(player_service, value, expected):
    player_service._time_pos_prop.on_update(value)

    assert player_service.time_pos == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (30.2, 30),
        (30.7, 31),
        (None, None),
    ],
)
def test_time_remaining_changed(player_service, make_spy, value, expected):
    spy = make_spy(player_service.time_remaining_changed)

    player_service._time_remaining_prop.on_update(value)

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
def test_height_changed(player_service, make_spy, value, expected):
    spy = make_spy(player_service.height_changed)

    player_service._height_prop.on_update(value)

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
def test_width_changed(player_service, make_spy, value, expected):
    spy = make_spy(player_service.width_changed)

    player_service._width_prop.on_update(value)

    if expected is not None:
        assert spy.count() == 1
        assert spy.at(0, 0) == expected
    else:
        assert spy.count() == 0


@dataclass
class TrackCountTestCase:
    description: str
    track_list: list[dict]
    expected_audio_count: int
    expected_subtitle_count: int


def _handle_track_list(player_service, value):
    player_service._audio_track_count_prop.on_update(value)
    player_service._subtitle_track_count_prop.on_update(value)


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
def test_track_list_changed_updates_counts(player_service, test_case):
    _handle_track_list(player_service, test_case.track_list)

    assert player_service.audio_track_count == test_case.expected_audio_count
    assert player_service.subtitle_track_count == test_case.expected_subtitle_count


def test_track_list_changed_emits_audio_signal(player_service, make_spy):
    spy = make_spy(player_service.audio_track_count_changed)
    track_list = [{"type": "audio", "external": False, "external-filename": ""}]

    _handle_track_list(player_service, track_list)

    assert spy.count() == 1
    assert spy.at(0, 0) == 1


def test_track_list_changed_emits_subtitle_signal(player_service, make_spy):
    spy = make_spy(player_service.subtitle_track_count_changed)
    track_list = [{"type": "sub", "external": False, "external-filename": ""}]

    _handle_track_list(player_service, track_list)

    assert spy.count() == 1
    assert spy.at(0, 0) == 1


def test_track_list_changed_does_not_emit_for_none(player_service, make_spy):
    audio_spy = make_spy(player_service.audio_track_count_changed)
    subtitle_spy = make_spy(player_service.subtitle_track_count_changed)

    _handle_track_list(player_service, None)

    assert audio_spy.count() == 0
    assert subtitle_spy.count() == 0


def test_track_list_changed_does_not_emit_when_count_unchanged(player_service, make_spy):
    track_list = [{"type": "audio", "external": False, "external-filename": ""}]
    _handle_track_list(player_service, track_list)

    spy = make_spy(player_service.audio_track_count_changed)
    _handle_track_list(player_service, track_list)

    assert spy.count() == 0


def test_track_list_changed_emits_only_changed_signal(player_service, make_spy):
    initial_list = [
        {"type": "audio", "external": False, "external-filename": ""},
        {"type": "sub", "external": False, "external-filename": ""},
    ]
    _handle_track_list(player_service, initial_list)

    audio_spy = make_spy(player_service.audio_track_count_changed)
    subtitle_spy = make_spy(player_service.subtitle_track_count_changed)

    updated_list = [
        {"type": "audio", "external": False, "external-filename": ""},
        {"type": "sub", "external": False, "external-filename": ""},
        {"type": "sub", "external": True, "external-filename": "/path/sub.srt"},
    ]
    _handle_track_list(player_service, updated_list)

    assert audio_spy.count() == 0
    assert subtitle_spy.count() == 1
    assert subtitle_spy.at(0, 0) == 2
