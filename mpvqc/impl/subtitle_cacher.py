#  mpvQC
#
#  Copyright (C) 2022 mpvQC developers
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


from typing import Callable, Iterable


class SubtitleCacher:

    def __init__(
            self,
            is_video_loaded_func: Callable[[], bool],
            load_subtitles_func: Callable[[Iterable[str]], None]
    ):
        self._is_video_loaded_func = is_video_loaded_func
        self._load_subtitles_func = load_subtitles_func
        self._cache = set()

    def open(self, subtitles: tuple[str]):
        if self._have_video():
            self._load_subtitles(subtitles)
        else:
            self._cache_subtitles(subtitles)

    def _have_video(self):
        return self._is_video_loaded_func()

    def _load_subtitles(self, subtitles: Iterable[str]):
        self._load_subtitles_func(subtitles)

    def _cache_subtitles(self, subtitles):
        self._cache = self._cache | set(subtitles)

    def load_cached_subtitles(self):
        self._load_subtitles(self._cache)
        self._cache.clear()
