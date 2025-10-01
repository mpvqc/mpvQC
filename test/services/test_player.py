# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import inject
import pytest

from mpvqc.services import ApplicationPathsService, OperatingSystemZoomDetectorService, PlayerService, TypeMapperService

VIDEO = "video"
SUBTITLE = "test"
SUBTITLES = (SUBTITLE,)


@pytest.fixture(autouse=True, scope="module")
def configure_injections(type_mapper):
    def config(binder: inject.Binder):
        binder.bind(TypeMapperService, type_mapper)
        binder.bind(ApplicationPathsService, MagicMock())
        binder.bind(OperatingSystemZoomDetectorService, MagicMock())

    inject.configure(config, clear=True)


def test_log_handler_set_when_mpvqc_debug_is_set(monkeypatch):
    monkeypatch.setenv("MPVQC_DEBUG", "1")

    from mpvqc.services.player import PlayerService

    service = PlayerService()

    assert "log_handler" in service._init_args


def test_log_handler_set_when_mpvqc_player_log_is_set(monkeypatch):
    monkeypatch.setenv("MPVQC_PLAYER_LOG", "1")

    from mpvqc.services.player import PlayerService

    service = PlayerService()

    assert "log_handler" in service._init_args


def test_log_handler_not_set_when_no_env_vars(monkeypatch):
    monkeypatch.delenv("MPVQC_DEBUG", raising=False)
    monkeypatch.delenv("MPVQC_PLAYER_LOG", raising=False)

    from mpvqc.services.player import PlayerService

    service = PlayerService()

    assert "log_handler" not in service._init_args


def _create_mpv_and_player_service(has_video: bool = False) -> Generator[MagicMock, PlayerService]:
    mpv_mock = MagicMock()
    mpv_mock.path = "video" if has_video else None

    def _mocked_command(arg1, _, __):
        if arg1 == "loadfile":
            mpv_mock.path = "video"

    mpv_mock.command = MagicMock(side_effect=_mocked_command)
    service: PlayerService = PlayerService()
    service._mpv = mpv_mock

    with patch("mpvqc.services.player.MPV", return_value=MagicMock()):
        yield mpv_mock, service


def test_subtitles_open_video_not_present():
    mpv_mock, service = next(_create_mpv_and_player_service(has_video=False))

    service.open_subtitles(SUBTITLES)

    assert not mpv_mock.command.called
    assert SUBTITLE in service._cached_subtitles


def test_subtitles_open_video_present():
    mpv_mock, service = next(_create_mpv_and_player_service(has_video=True))

    service.open_subtitles(SUBTITLES)

    assert mpv_mock.command.called
    assert SUBTITLE not in service._cached_subtitles
    assert not service._cached_subtitles


def test_subtitles_load_subtitles():
    mpv_mock, service = next(_create_mpv_and_player_service(has_video=False))

    service.open_subtitles(SUBTITLES)
    service.open_video(VIDEO)

    assert mpv_mock.command.called
    loadfile, video, replace = mpv_mock.command.call_args_list[0][0]
    assert loadfile == "loadfile"
    assert video == VIDEO
    assert replace == "replace"

    sub_add, subtitle, select = mpv_mock.command.call_args_list[1][0]
    assert sub_add == "sub-add"
    assert subtitle == SUBTITLE
    assert select == "select"


def test_subtitles_empties_cache():
    mpv_mock, service = next(_create_mpv_and_player_service(has_video=False))

    service.open_subtitles(SUBTITLES)
    service.open_video(VIDEO)

    assert SUBTITLE not in service._cached_subtitles
    assert not service._cached_subtitles
