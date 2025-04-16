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

from collections.abc import Iterable

import inject
from mpv import MPV

from .application_paths import ApplicationPathsService
from .operating_system_zoom_detector import OperatingSystemZoomDetectorService
from .type_mapper import TypeMapperService


class PlayerService:
    _paths = inject.attr(ApplicationPathsService)
    _zoom_detector_service = inject.attr(OperatingSystemZoomDetectorService)
    _type_mapper: TypeMapperService = inject.attr(TypeMapperService)

    def __init__(self, **properties):
        super().__init__(**properties)
        self._cached_subtitles = set()

        self._init_args = {
            "keep_open": "yes",
            "idle": "yes",
            "osc": "yes",
            "cursor_autohide": "no",
            "input_cursor": "no",
            "input_default_bindings": "no",
            "config": "yes",
            "config_dir": self._type_mapper.map_path_to_str(self._paths.dir_config),
            "screenshot_directory": self._type_mapper.map_path_to_str(self._paths.dir_screenshots),
            "ytdl": "yes",
        }

        self._mpv: MPV | None = None

    def init(self, win_id: int or None = None):
        if win_id is None:  # noqa: SIM108
            args = {"vo": "libmpv"}
        else:
            args = {"wid": win_id}

        self._mpv = MPV(**dict(self._init_args, **args))

    @property
    def mpv(self) -> MPV:
        return self._mpv

    @property
    def mpv_version(self) -> str:
        return self._mpv.mpv_version

    @property
    def ffmpeg_version(self) -> str:
        return self._mpv.ffmpeg_version

    @property
    def path(self) -> str or None:
        return self._mpv.path

    @property
    def has_video(self) -> bool:
        return self.path is not None

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
        self._open_cached_subtitles()
        self.play()

    def _open_cached_subtitles(self):
        if self._cached_subtitles:
            self.open_subtitles(self._cached_subtitles)
            self._cached_subtitles.clear()

    def open_subtitles(self, subtitles: Iterable[str]) -> None:
        def _load():
            for subtitle in subtitles:
                self._mpv.command("sub-add", subtitle, "select")

        def _cache():
            self._cached_subtitles |= set(subtitles)

        if self.has_video:
            _load()
        else:
            _cache()

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
        self._mpv.command_async("keypress", "MOUSE_BTN3")

    def scroll_down(self) -> None:
        self._mpv.command_async("keypress", "MOUSE_BTN4")

    def terminate(self) -> None:
        self._mpv.terminate()

    def observe(self, property_name, handler):
        self._mpv.observe_property(property_name, handler)
