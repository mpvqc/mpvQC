# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

VIDEO = Path.home() / "video.mp4"
SUBTITLE = Path.home() / "subtitle"
SUBTITLES = (SUBTITLE,)


def _commands(player_handle, name: str) -> list[tuple]:
    return [command for command in player_handle.commands if command[0] == name]


def test_subs_only_with_video_loaded_attach_directly(player_handle, player_service, push_property):
    push_property("path", "video")

    player_service.open_media(video=None, subtitles=SUBTITLES)

    assert len(_commands(player_handle, "sub-add")) == 1


def test_subs_only_with_no_video_do_not_issue_command(player_handle, player_service):
    player_service.open_media(video=None, subtitles=SUBTITLES)

    assert not player_handle.commands


def test_video_with_subs_flushes_after_file_loaded(player_handle, player_service, push_file_loaded):
    player_service.open_media(video=VIDEO, subtitles=SUBTITLES)
    push_file_loaded()

    loadfile_calls = _commands(player_handle, "loadfile")
    sub_add_calls = _commands(player_handle, "sub-add")
    assert len(loadfile_calls) == 1
    assert Path(loadfile_calls[0][1]) == VIDEO
    assert len(sub_add_calls) == 1
    assert Path(sub_add_calls[0][1]) == SUBTITLE


def test_same_video_reloads_and_flushes_subs(player_handle, player_service, push_property, push_file_loaded):
    push_property("path", str(VIDEO))

    player_service.open_media(video=VIDEO, subtitles=SUBTITLES)
    push_file_loaded()

    assert len(_commands(player_handle, "loadfile")) == 1
    assert len(_commands(player_handle, "sub-add")) == 1
