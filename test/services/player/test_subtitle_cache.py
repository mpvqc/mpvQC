# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from unittest.mock import MagicMock

from mpvqc.services import PlayerService

VIDEO = Path.home() / "video.mp4"
SUBTITLE = Path.home() / "subtitle"
SUBTITLES = (SUBTITLE,)


def test_subtitles_open_video_not_present(mpv_mock, player_service):
    mpv_mock.path = None

    player_service.open_subtitles(SUBTITLES)

    assert not mpv_mock.command.called
    assert SUBTITLE in player_service._subtitle_coordinator.cached


def test_subtitles_open_video_present(mpv_mock, player_service):
    player_service._path_prop.on_update("video")
    player_service._video_loaded_prop.on_update("video")

    player_service.open_subtitles(SUBTITLES)

    assert mpv_mock.command.called
    assert SUBTITLE not in player_service._subtitle_coordinator.cached
    assert not player_service._subtitle_coordinator.cached


def test_subtitles_load_subtitles(mpv_mock, player_service):
    mpv_mock.path = None

    def _mocked_command(arg1, _, __):
        if arg1 == "loadfile":
            mpv_mock.path = "video"

    mpv_mock.command = MagicMock(side_effect=_mocked_command)

    player_service.open_subtitles(SUBTITLES)
    player_service.open_video(VIDEO)

    _simulate_path_changed_event(player_service)

    assert mpv_mock.command.called
    loadfile, video, replace = mpv_mock.command.call_args_list[0][0]
    assert loadfile == "loadfile"
    assert video == str(VIDEO)
    assert replace == "replace"

    sub_add, subtitle, select = mpv_mock.command.call_args_list[1][0]
    assert sub_add == "sub-add"
    assert Path(subtitle) == SUBTITLE
    assert select == "select"


def test_subtitles_empties_cache(mpv_mock, player_service):
    mpv_mock.path = None

    def _mocked_command(arg1, _, __):
        if arg1 == "loadfile":
            mpv_mock.path = "video"

    mpv_mock.command = MagicMock(side_effect=_mocked_command)

    player_service.open_subtitles(SUBTITLES)
    player_service.open_video(VIDEO)

    _simulate_path_changed_event(player_service)

    assert SUBTITLE not in player_service._subtitle_coordinator.cached
    assert not player_service._subtitle_coordinator.cached


def test_subtitles_cached_during_video_load(mpv_mock, player_service):
    mpv_mock.path = "video"

    def _mocked_command(arg1, _, __):
        if arg1 == "loadfile":
            mpv_mock.path = "video"

    mpv_mock.command = MagicMock(side_effect=_mocked_command)

    player_service.open_video(VIDEO)
    player_service.open_subtitles(SUBTITLES)

    assert mpv_mock.command.called
    loadfile, video, replace = mpv_mock.command.call_args_list[0][0]
    assert loadfile == "loadfile"
    assert video == str(VIDEO)
    assert replace == "replace"
    assert SUBTITLE in player_service._subtitle_coordinator.cached

    _simulate_path_changed_event(player_service)

    sub_add, subtitle, select = mpv_mock.command.call_args_list[1][0]
    assert sub_add == "sub-add"
    assert Path(subtitle) == SUBTITLE
    assert select == "select"
    assert SUBTITLE not in player_service._subtitle_coordinator.cached


# noinspection PyProtectedMember
def _simulate_path_changed_event(player_service: PlayerService):
    player_service._path_prop.on_update(str(VIDEO))
    player_service._video_loaded_prop.on_update(str(VIDEO))
