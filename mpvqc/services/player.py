#  mpvQC
#
#  Copyright (C) 2022 mpvQC developers
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


import inject

from mpvqc.impl import MPV
from mpvqc.services.file import FileService
from mpvqc.services.time_formatter import TimeFormatterService


class PlayerService:
    _files = inject.attr(FileService)
    _formatter = inject.attr(TimeFormatterService)

    def __init__(self, **properties):
        super().__init__(**properties)
        self.__subtitles = []
        self._mpv = MPV(
            vo="libmpv",
            keep_open="yes",
            idle="yes",
            osc="yes",
            cursor_autohide="no",
            input_cursor="no",
            input_default_bindings="no",
            config="yes",
            config_dir=str(self._files.dir_config),
            screenshot_directory=str(self._files.dir_screenshots),
            ytdl="yes",
            # log_handler=logging.mpv_log_handler,
        )

    @property
    def mpv(self):
        return self._mpv

    @property
    def current_time(self) -> tuple[int, str]:
        return self._formatter.format(self._mpv.time_pos)

    def move_mouse(self, x: int, y: int):
        self._mpv.command_async("mouse", x, y)

    def open(self, url: str):
        self._mpv.command_async("loadfile", url, "replace")
        self.play()

    def pause(self):
        self._mpv.pause = True

    def play(self):
        self._mpv.pause = False

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

    def version_mpv(self):
        return self._mpv.mpv_version

    def version_ffmpeg(self):
        return self._mpv.ffmpeg_version
