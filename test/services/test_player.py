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

import unittest
from unittest.mock import MagicMock, patch

import inject

from mpvqc.services import PlayerService, TypeMapperService, OperatingSystemZoomDetectorService, ApplicationPathsService


class PlayerServiceTest(unittest.TestCase):
    video = "video"
    subtitle = "test"
    subtitles = (subtitle,)

    def setUp(self):
        # fmt: off
        inject.clear_and_configure(lambda binder: binder
                                   .bind(TypeMapperService, TypeMapperService())
                                   .bind(ApplicationPathsService, MagicMock())
                                   .bind(OperatingSystemZoomDetectorService, MagicMock()))
        # fmt: on

    def tearDown(self):
        inject.clear()

    def _mock(self, has_video: bool = False):
        self._mpv_mock = MagicMock()
        self._mpv_mock.path = "video" if has_video else None

        def _mocked_command(arg1, arg2, arg3):
            if arg1 == "loadfile":
                self._mpv_mock.path = "video"

        self._mpv_mock.command = MagicMock(side_effect=_mocked_command)
        self._service: PlayerService = PlayerService()
        self._service._mpv = self._mpv_mock

    @patch("mpvqc.services.player.MPV", return_value=MagicMock())
    def test_open_video_not_present(self, *_):
        self._mock(has_video=False)
        self._service.open_subtitles(self.subtitles)
        self.assertFalse(self._mpv_mock.command.called)
        self.assertIn(self.subtitle, self._service._cached_subtitles)

    @patch("mpvqc.services.player.MPV", return_value=MagicMock())
    def test_open_video_present(self, *_):
        self._mock(has_video=True)
        self._service.open_subtitles(self.subtitles)
        self._mpv_mock.command.assert_called()
        self.assertNotIn(self.subtitle, self._service._cached_subtitles)
        self.assertFalse(self._service._cached_subtitles)

    @patch("mpvqc.services.player.MPV", return_value=MagicMock())
    def test_load_subtitles(self, *_):
        self._mock(has_video=False)
        self._service.open_subtitles(self.subtitles)
        self._service.open_video(self.video)

        self._mpv_mock.command.assert_called()
        loadfile, video, replace = self._mpv_mock.command.call_args_list[0][0]
        self.assertEqual("loadfile", loadfile)
        self.assertEqual(self.video, video)
        self.assertEqual("replace", replace)

        sub_add, subtitle, select = self._mpv_mock.command.call_args_list[1][0]
        self.assertEqual("sub-add", sub_add)
        self.assertEqual(self.subtitle, subtitle)
        self.assertEqual("select", select)

    @patch("mpvqc.services.player.MPV", return_value=MagicMock())
    def test_load_subtitles_empties_cache(self, *_):
        self._mock(has_video=False)
        self._service.open_subtitles(self.subtitles)
        self._service.open_video(self.video)

        self.assertNotIn(self.subtitle, self._service._cached_subtitles)
        self.assertFalse(self._service._cached_subtitles)
