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

from typing import Iterable, Callable

import inject
from mpv import MPV

from .application_paths import ApplicationPathsService
from .operating_system_zoom_detector import OperatingSystemZoomDetectorService


class PlayerService:
    _paths = inject.attr(ApplicationPathsService)
    _zoom_detector_service = inject.attr(OperatingSystemZoomDetectorService)

    def __init__(self, **properties):
        super().__init__(**properties)
        self._mpv = MPV(
            vo="libmpv",
            keep_open="yes",
            idle="yes",
            osc="yes",
            cursor_autohide="no",
            input_cursor="no",
            input_default_bindings="no",
            config="yes",
            config_dir=str(self._paths.dir_config),
            screenshot_directory=str(self._paths.dir_screenshots),
            ytdl="yes",
            # log_handler=logging.mpv_log_handler,
        )
        self._subtitle_cacher = SubtitleCacher(
            is_video_loaded_func=self._is_video_loaded,
            load_subtitles_func=self._load_subtitles
        )

    def _is_video_loaded(self) -> bool:
        return bool(self._mpv.path)

    def _load_subtitles(self, subtitles) -> None:
        for subtitle in subtitles:
            self._mpv.command("sub-add", subtitle, "select")

    @property
    def mpv(self) -> MPV:
        return self._mpv

    @property
    def path(self) -> str:
        return self._mpv.path

    @property
    def current_time(self) -> int:
        return self._mpv.time_pos or 0

    def move_mouse(self, x: int, y: int) -> None:
        zoom_factor = self._zoom_detector_service.zoom_factor
        x = int(x * zoom_factor)
        y = int(y * zoom_factor)
        self._mpv.command_async("mouse", x, y)

    def open_video(self, video: str) -> None:
        self._mpv.command("loadfile", video, "replace")
        self._subtitle_cacher.load_cached_subtitles()
        self.play()

    def open_subtitles(self, subtitles: tuple[str]) -> None:
        self._subtitle_cacher.open(subtitles)

    def play(self) -> None:
        self._mpv.pause = False

    def pause(self) -> None:
        self._mpv.pause = True

    def execute(self, command) -> None:
        self._mpv.command_async("keypress", command)

    def jump_to(self, seconds: int) -> None:
        self._mpv.command_async("seek", seconds, "absolute+exact")

    def press_mouse_left(self) -> None:
        self._mpv.command_async("keydown", "MOUSE_BTN0")

    def press_mouse_middle(self) -> None:
        self._mpv.command_async("keypress", "MOUSE_BTN1")

    def release_mouse_left(self) -> None:
        self._mpv.command_async("keyup", "MOUSE_BTN0")

    def scroll_up(self) -> None:
        self._mpv.command_async("keypress", f"MOUSE_BTN3")

    def scroll_down(self) -> None:
        self._mpv.command_async("keypress", f"MOUSE_BTN4")


class SubtitleCacher:

    def __init__(
            self,
            is_video_loaded_func: Callable[[], bool],
            load_subtitles_func: Callable[[Iterable[str]], None]
    ):
        self._is_video_loaded_func = is_video_loaded_func
        self._load_subtitles_func = load_subtitles_func
        self._cache = set()

    def open(self, subtitles: tuple[str]) -> None:
        if self._have_video():
            self._load_subtitles(subtitles)
        else:
            self._cache_subtitles(subtitles)

    def _have_video(self) -> bool:
        return self._is_video_loaded_func()

    def _load_subtitles(self, subtitles: Iterable[str]) -> None:
        self._load_subtitles_func(subtitles)

    def _cache_subtitles(self, subtitles) -> None:
        self._cache = self._cache | set(subtitles)

    def load_cached_subtitles(self) -> None:
        self._load_subtitles(self._cache)
        self._cache.clear()
