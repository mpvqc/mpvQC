# mpvQC
#
# Copyright (C) 2022 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import inject
import pytest

from mpvqc.services import TypeMapperService, ApplicationPathsService, OperatingSystemZoomDetectorService, PlayerService

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


def create_mpv_and_player_service(has_video: bool = False) -> Generator[MagicMock, PlayerService]:
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
    mpv_mock, service = next(create_mpv_and_player_service(has_video=False))

    service.open_subtitles(SUBTITLES)

    assert not mpv_mock.command.called
    assert SUBTITLE in service._cached_subtitles


def test_subtitles_open_video_present():
    mpv_mock, service = next(create_mpv_and_player_service(has_video=True))

    service.open_subtitles(SUBTITLES)

    assert mpv_mock.command.called
    assert SUBTITLE not in service._cached_subtitles
    assert not service._cached_subtitles


def test_subtitles_load_subtitles():
    mpv_mock, service = next(create_mpv_and_player_service(has_video=False))

    service.open_subtitles(SUBTITLES)
    service.open_video(VIDEO)

    assert mpv_mock.command.called
    loadfile, video, replace = mpv_mock.command.call_args_list[0][0]
    assert "loadfile" == loadfile
    assert VIDEO == video
    assert "replace" == replace

    sub_add, subtitle, select = mpv_mock.command.call_args_list[1][0]
    assert "sub-add" == sub_add
    assert SUBTITLE == subtitle
    assert "select" == select


def test_subtitles_empties_cache():
    mpv_mock, service = next(create_mpv_and_player_service(has_video=False))

    service.open_subtitles(SUBTITLES)
    service.open_video(VIDEO)

    assert SUBTITLE not in service._cached_subtitles
    assert not service._cached_subtitles
