# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

from mpvqc.services import PlayerService

VIDEO = Path.home() / "video.mp4"
SUBTITLE = Path.home() / "subtitle"
SUBTITLES = (SUBTITLE,)


def test_subs_only_with_video_loaded_attach_directly(mpv_mock, player_service):
    player_service._apply_property_update("path", "video")

    player_service.open_media(video=None, subtitles=SUBTITLES)

    sub_add_calls = [c for c in mpv_mock.command.call_args_list if c[0][0] == "sub-add"]
    assert len(sub_add_calls) == 1


def test_subs_only_with_no_video_do_not_issue_command(mpv_mock, player_service):
    mpv_mock.path = None

    player_service.open_media(video=None, subtitles=SUBTITLES)

    assert not mpv_mock.command.called


def test_video_with_subs_flushes_after_file_loaded(mpv_mock, player_service):
    mpv_mock.path = None

    player_service.open_media(video=VIDEO, subtitles=SUBTITLES)
    _simulate_file_loaded(player_service)

    loadfile_calls = [c for c in mpv_mock.command.call_args_list if c[0][0] == "loadfile"]
    sub_add_calls = [c for c in mpv_mock.command.call_args_list if c[0][0] == "sub-add"]
    assert len(loadfile_calls) == 1
    assert Path(loadfile_calls[0][0][1]) == VIDEO
    assert len(sub_add_calls) == 1
    assert Path(sub_add_calls[0][0][1]) == SUBTITLE


def test_same_video_reloads_and_flushes_subs(mpv_mock, player_service):
    player_service._apply_property_update("path", str(VIDEO))

    player_service.open_media(video=VIDEO, subtitles=SUBTITLES)
    _simulate_file_loaded(player_service)

    loadfile_calls = [c for c in mpv_mock.command.call_args_list if c[0][0] == "loadfile"]
    sub_add_calls = [c for c in mpv_mock.command.call_args_list if c[0][0] == "sub-add"]
    assert len(loadfile_calls) == 1
    assert len(sub_add_calls) == 1


# noinspection PyProtectedMember
def _simulate_file_loaded(player_service: PlayerService) -> None:
    player_service._on_file_loaded()
