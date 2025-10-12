# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
from collections.abc import Iterable
from pathlib import Path

import inject
from loguru import logger
from mpv import MPV
from PySide6.QtCore import QObject, Signal

from .application_paths import ApplicationPathsService
from .key_command import KeyCommandGeneratorService
from .operating_system_zoom_detector import OperatingSystemZoomDetectorService
from .type_mapper import TypeMapperService


class PlayerService(QObject):
    _command_generator: KeyCommandGeneratorService = inject.attr(KeyCommandGeneratorService)
    _paths = inject.attr(ApplicationPathsService)
    _type_mapper: TypeMapperService = inject.attr(TypeMapperService)
    _zoom_detector_service = inject.attr(OperatingSystemZoomDetectorService)

    video_loaded_changed = Signal(bool)
    path_changed = Signal(str)
    filename_changed = Signal(str)
    duration_changed = Signal(float)
    percent_pos_changed = Signal(int)
    time_pos_changed = Signal(int)
    time_remaining_changed = Signal(int)
    height_changed = Signal(int)
    width_changed = Signal(int)

    video_dimensions_changed = Signal(int, int)

    def __init__(self, **properties):
        super().__init__(**properties)
        self._cached_subtitles = set()
        self._loading_video = False

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

        if os.getenv("MPVQC_DEBUG") or os.getenv("MPVQC_PLAYER_LOG"):

            def player_logger(*args):
                level, context, message = args
                logger.log("MPV", message.strip(), mpv_level=level, mpv_context=context)

            self._init_args["log_handler"] = player_logger

        self._mpv: MPV | None = None

        self._dimensions_coordinator = DualSignalCoordinator(
            signal_a=self.width_changed,
            signal_b=self.height_changed,
            reset_signal=self.path_changed,
        )
        self._dimensions_coordinator.both_ready.connect(self.video_dimensions_changed.emit)

    def init(self, win_id: int | None = None):
        if win_id is None:  # noqa: SIM108
            args = {"vo": "libmpv"}
        else:
            args = {"wid": win_id}

        self._mpv = MPV(**dict(self._init_args, **args))

        self.observe("duration", self._on_duration_changed)
        self.observe("path", self._on_player_path_changed)
        self.observe("filename", self._on_player_filename_changed)
        self.observe("percent-pos", self._on_player_percent_pos_changed)
        self.observe("time-pos", self._on_player_time_pos_changed)
        self.observe("time-remaining", self._on_player_time_remaining_changed)
        self.observe("height", self._on_player_height_changed)
        self.observe("width", self._on_player_width_changed)

    @property
    def mpv(self) -> MPV:
        return self._mpv

    @property
    def mpv_version(self) -> str:
        return self._mpv.mpv_version if self._mpv else ""

    @property
    def ffmpeg_version(self) -> str:
        return self._mpv.ffmpeg_version if self._mpv else ""

    @property
    def path(self) -> str | None:
        return self._mpv.path if self._mpv else None

    @property
    def filename(self) -> str | None:
        return self._mpv.filename if self._mpv else None

    @property
    def percent_pos(self) -> int | None:
        if not self._mpv or self._mpv.percent_pos is None:
            return None
        return int(self._mpv.percent_pos + 0.5)

    @property
    def time_pos(self) -> int | None:
        if not self._mpv or self._mpv.time_pos is None:
            return None
        return int(self._mpv.time_pos)

    @property
    def time_remaining(self) -> int | None:
        if not self._mpv or self._mpv.time_remaining is None:
            return None
        return int(self._mpv.time_remaining)

    @property
    def height(self) -> int | None:
        return self._mpv.height if self._mpv else None

    @property
    def width(self) -> int | None:
        return self._mpv.width if self._mpv else None

    @property
    def video_loaded(self) -> bool:
        return self.path is not None

    @property
    def has_video(self) -> bool:
        return self.path is not None

    @property
    def current_time(self) -> int:
        return self.time_pos or 0

    @property
    def duration(self) -> float:
        return self._mpv.duration if self._mpv and self._mpv.duration else 0.0

    def is_video_loaded(self, video: Path) -> bool:
        if (path := self.path) is not None:
            current = self._type_mapper.map_path_to_str(Path(path))
            to_check = self._type_mapper.map_path_to_str(video)
            return current == to_check
        return False

    def _on_duration_changed(self, _, value: float) -> None:
        if value:
            self.duration_changed.emit(value)

    def _on_player_path_changed(self, _, value: str) -> None:
        self.path_changed.emit(value or "")
        self.video_loaded_changed.emit(value is not None)

        if value is not None and self._loading_video:
            self._loading_video = False
            self._open_cached_subtitles()

    def _open_cached_subtitles(self):
        if self._cached_subtitles:
            self.open_subtitles(self._cached_subtitles)
            self._cached_subtitles.clear()

    def _on_player_filename_changed(self, _, value: str) -> None:
        self.filename_changed.emit(value or "")

    def _on_player_percent_pos_changed(self, _, value: float) -> None:
        if value is not None:
            self.percent_pos_changed.emit(int(value))

    def _on_player_time_pos_changed(self, _, value: float) -> None:
        if value is not None:
            self.time_pos_changed.emit(int(value))

    def _on_player_time_remaining_changed(self, _, value: float) -> None:
        if value is not None:
            self.time_remaining_changed.emit(int(value))

    def _on_player_height_changed(self, _, value: int) -> None:
        if value is not None:
            self.height_changed.emit(value)

    def _on_player_width_changed(self, _, value: int) -> None:
        if value is not None:
            self.width_changed.emit(value)

    def move_mouse(self, x: int, y: int) -> None:
        zoom_factor = self._zoom_detector_service.zoom_factor
        x = int(x * zoom_factor)
        y = int(y * zoom_factor)
        self._mpv.command_async("mouse", x, y)

    def open_video(self, video: str) -> None:
        self._loading_video = True
        self._mpv.command("loadfile", video, "replace")
        self.play()

    def open_subtitles(self, subtitles: Iterable[str]) -> None:
        def _load():
            for subtitle in subtitles:
                self._mpv.command("sub-add", subtitle, "select")

        def _cache():
            self._cached_subtitles |= set(subtitles)

        if self.has_video and not self._loading_video:
            _load()
        else:
            _cache()

    def play(self) -> None:
        self._mpv.pause = False

    def pause(self) -> None:
        self._mpv.pause = True

    def handle_key_event(self, key: int, modifiers: int) -> None:
        if command := self._command_generator.generate_command(key, modifiers):
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


class DualSignalCoordinator(QObject):
    both_ready = Signal(object, object)

    def __init__(self, signal_a, signal_b, reset_signal=None):
        super().__init__()
        self._value_a = None
        self._value_b = None
        self._ready_a = False
        self._ready_b = False

        signal_a.connect(self._on_signal_a)
        signal_b.connect(self._on_signal_b)

        if reset_signal:
            reset_signal.connect(self._reset)

    def _on_signal_a(self, value):
        self._value_a = value
        self._ready_a = True
        self._check_and_emit()

    def _on_signal_b(self, value):
        self._value_b = value
        self._ready_b = True
        self._check_and_emit()

    def _check_and_emit(self):
        if self._ready_a and self._ready_b and self._value_a and self._value_b:
            self.both_ready.emit(self._value_a, self._value_b)
            self._reset()

    def _reset(self):
        self._ready_a = False
        self._ready_b = False
