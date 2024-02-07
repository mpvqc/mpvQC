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
from unittest.mock import Mock

from mpvqc.services import SubtitleCacher


class TestSubtitleCacher(unittest.TestCase):
    subtitle = 'test'
    subtitles = (subtitle,)

    def test_open_video_not_present(self):
        cacher = SubtitleCacher(
            is_video_loaded_func=lambda: False,
            load_subtitles_func=lambda: None
        )
        cacher.open(self.subtitles)
        self.assertIn(self.subtitle, cacher._cache)

    def test_open_video_present(self):
        mock = Mock()
        cacher = SubtitleCacher(
            is_video_loaded_func=lambda: True,
            load_subtitles_func=mock()
        )
        cacher.open(self.subtitles)
        mock.assert_called()

    def test_load_subtitles(self):
        mock = Mock()
        cacher = SubtitleCacher(
            is_video_loaded_func=lambda: True,
            load_subtitles_func=mock()
        )
        cacher.load_cached_subtitles()
        mock.assert_called()

    def test_load_subtitles_empties_cache(self):
        mock = Mock()
        cacher = SubtitleCacher(
            is_video_loaded_func=lambda: True,
            load_subtitles_func=mock()
        )
        cacher._cache.update(self.subtitle)
        cacher.load_cached_subtitles()
        self.assertFalse(cacher._cache)
