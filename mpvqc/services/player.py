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


import inject
from mpv import MPV

from mpvqc.impl import SubtitleCacher
from mpvqc.services.file_paths import FilePathService


class PlayerService:
    _paths = inject.attr(FilePathService)

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

    def _is_video_loaded(self):
        return bool(self._mpv.path)

    def _load_subtitles(self, subtitles):
        for subtitle in subtitles:
            self._mpv.command("sub-add", subtitle, "select")

    @property
    def mpv(self):
        return self._mpv

    @property
    def current_time(self) -> int:
        return self._mpv.time_pos or 0

    def move_mouse(self, x: int, y: int):
        self._mpv.command_async("mouse", x, y)

    def open_video(self, video: str):
        self._mpv.command("loadfile", video, "replace")
        self._subtitle_cacher.load_cached_subtitles()
        self.play()

    def open_subtitles(self, subtitles: tuple[str]):
        self._subtitle_cacher.open(subtitles)

    def play(self):
        self._mpv.pause = False

    def pause(self):
        self._mpv.pause = True

    def execute(self, command):
        self._mpv.command_async("keypress", command)

    def jump_to(self, seconds: int):
        self._mpv.command_async("seek", seconds, "absolute+exact")

    def press_mouse_left(self):
        self._mpv.command_async("keydown", "MOUSE_BTN0")

    def press_mouse_middle(self):
        self._mpv.command_async("keypress", "MOUSE_BTN1")

    def release_mouse_left(self):
        self._mpv.command_async("keyup", "MOUSE_BTN0")

    def scroll_up(self):
        self._mpv.command_async("keypress", f"MOUSE_BTN3")

    def scroll_down(self):
        self._mpv.command_async("keypress", f"MOUSE_BTN4")
