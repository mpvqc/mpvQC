# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import inject
from PySide6.QtCore import Property, QObject, Qt, Signal

from .application_paths import ApplicationPathsService
from .host_integration import HostIntegrationService
from .key_command import KeyCommandGeneratorService
from .type_mapper import TypeMapperService

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable
    from typing import Any

    from mpv import MPV

logger = logging.getLogger(__name__)


class PlayerService(QObject):
    _command_generator = inject.attr(KeyCommandGeneratorService)
    _host_integration = inject.attr(HostIntegrationService)
    _paths = inject.attr(ApplicationPathsService)
    _type_mapper = inject.attr(TypeMapperService)

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

    audio_track_count_changed = Signal(int)
    subtitle_track_count_changed = Signal(int)

    def __init__(self, **properties) -> None:
        super().__init__(**properties)

        # Cache subtitles for two reasons:
        # - User can open a subtitle before a video
        # - We need to wait until mpv internally updated the video before adding subtitles to it
        self._cached_subtitles: set[Path] = set()

        # Flag indicating a video is loading.
        # This is set to True for the time we start loading a video until mpv internally updates it's 'path' property
        self._loading_video = False

        self._init_args: dict[str, Any] = {
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
            mpv_log_level = 25

            def player_logger(*args) -> None:
                level, context, message = args
                logger.log(mpv_log_level, message.strip(), extra={"mpv_level": level, "mpv_context": context})

            self._init_args["log_handler"] = player_logger

        self._mpv: MPV | None = None

        self._dimensions_coordinator = _DimensionsCoordinator(on_both_ready=self.video_dimensions_changed.emit)

        self._cached_audio_track_count = 0
        self._cached_subtitle_track_count = 0

    def init(self, win_id: int | None = None) -> None:
        args = {"vo": "libmpv"} if win_id is None else {"wid": win_id}
        merged_args = self._init_args | args

        from mpv import MPV

        mpv = MPV(**merged_args)
        mpv.observe_property("duration", self._on_duration_changed)
        mpv.observe_property("path", self._on_player_path_changed)
        mpv.observe_property("filename", self._on_player_filename_changed)
        mpv.observe_property("percent-pos", self._on_player_percent_pos_changed)
        mpv.observe_property("time-pos", self._on_player_time_pos_changed)
        mpv.observe_property("time-remaining", self._on_player_time_remaining_changed)
        mpv.observe_property("height", self._on_player_height_changed)
        mpv.observe_property("width", self._on_player_width_changed)
        mpv.observe_property("track-list", self._on_track_list_changed)
        self._mpv = mpv

    @property
    def mpv(self) -> MPV:
        if self._mpv is None:
            msg = "MPV player has not been initialized"
            raise RuntimeError(msg)
        return self._mpv

    def _get_mpv_attr(self, attr: str) -> Any | None:
        if self._mpv is None:
            return None
        return getattr(self._mpv, attr, None)

    @property
    def mpv_version(self) -> str:
        return self._get_mpv_attr("mpv_version") or ""

    @property
    def ffmpeg_version(self) -> str:
        return self._get_mpv_attr("ffmpeg_version") or ""

    @property
    def path(self) -> str | None:
        return self._get_mpv_attr("path")

    @property
    def filename(self) -> str | None:
        return self._get_mpv_attr("filename")

    @property
    def percent_pos(self) -> int | None:
        percent: float | None = self._get_mpv_attr("percent_pos")
        if percent is None:
            return None
        return int(percent + 0.5)

    @property
    def time_pos(self) -> int | None:
        time: float | None = self._get_mpv_attr("time_pos")
        if time is None:
            return None
        return int(time + 0.5)

    @property
    def time_remaining(self) -> int | None:
        time: float | None = self._get_mpv_attr("time_remaining")
        if time is None:
            return None
        return int(time + 0.5)

    @property
    def height(self) -> int | None:
        return self._get_mpv_attr("height")

    @property
    def width(self) -> int | None:
        return self._get_mpv_attr("width")

    @property
    def video_loaded(self) -> bool:
        return self.path is not None

    @property
    def current_time(self) -> int:
        return self.time_pos or 0

    @property
    def duration(self) -> float:
        return self._get_mpv_attr("duration") or 0.0

    @property
    def is_paused(self) -> bool:
        return not self.is_playing

    @property
    def is_playing(self) -> bool:
        if mpv := self._mpv:
            return not mpv.pause and not mpv.idle_active
        return False

    @property
    def _track_list(self) -> list[TrackListEntry]:
        if self._mpv is None:
            return []
        track_list = self._get_mpv_attr("track_list") or []
        return [TrackListEntry.from_dict(e) for e in track_list]

    @property
    def external_subtitles(self) -> list[Path]:
        external = {
            Path(entry.external_filename).resolve()
            for entry in self._track_list
            if entry.external and entry.type == "sub"
        }
        return sorted(external)

    @Property(int, notify=audio_track_count_changed)
    def audio_track_count(self) -> int:
        return self._cached_audio_track_count

    @Property(int, notify=subtitle_track_count_changed)
    def subtitle_track_count(self) -> int:
        return self._cached_subtitle_track_count

    def _on_duration_changed(self, _, value: float | None) -> None:
        if value is not None:
            self.duration_changed.emit(value)

    def _on_player_path_changed(self, _, value: str | None) -> None:
        self._dimensions_coordinator.reset()
        self.path_changed.emit(value or "")
        self.video_loaded_changed.emit(value is not None)

        if value is not None and self._loading_video:
            self._loading_video = False
            self._open_cached_subtitles()

    def _open_cached_subtitles(self) -> None:
        if self._cached_subtitles:
            self.open_subtitles(self._cached_subtitles)
            self._cached_subtitles.clear()

    def _on_player_filename_changed(self, _, value: str | None) -> None:
        self.filename_changed.emit(value or "")

    def _on_player_percent_pos_changed(self, _, value: float | None) -> None:
        if value is not None:
            self.percent_pos_changed.emit(int(value + 0.5))

    def _on_player_time_pos_changed(self, _, value: float | None) -> None:
        if value is not None:
            self.time_pos_changed.emit(int(value + 0.5))

    def _on_player_time_remaining_changed(self, _, value: float | None) -> None:
        if value is not None:
            self.time_remaining_changed.emit(int(value + 0.5))

    def _on_player_height_changed(self, _, value: int | None) -> None:
        if value is not None:
            self.height_changed.emit(value)
            self._dimensions_coordinator.on_height(value)

    def _on_player_width_changed(self, _, value: int | None) -> None:
        if value is not None:
            self.width_changed.emit(value)
            self._dimensions_coordinator.on_width(value)

    def _on_track_list_changed(self, _, value: Any | None) -> None:
        if value is None:
            return

        audio_count = sum(1 for entry in self._track_list if entry.type == "audio")
        if audio_count != self._cached_audio_track_count:
            self._cached_audio_track_count = audio_count
            self.audio_track_count_changed.emit(audio_count)

        subtitle_count = sum(1 for entry in self._track_list if entry.type == "sub")
        if subtitle_count != self._cached_subtitle_track_count:
            self._cached_subtitle_track_count = subtitle_count
            self.subtitle_track_count_changed.emit(subtitle_count)

    def move_mouse(self, x: int, y: int) -> None:
        zoom_factor = self._host_integration.display_zoom_factor
        x = int(x * zoom_factor)
        y = int(y * zoom_factor)
        self.mpv.command_async("mouse", x, y)

    def open_video(self, video: Path) -> None:
        self._loading_video = True
        path = self._type_mapper.map_path_to_str(video)
        self.mpv.command("loadfile", path, "replace")
        self.play()

    def is_video_loaded(self, video: Path) -> bool:
        if (path := self.path) is not None:
            current = self._type_mapper.map_path_to_str(Path(path))
            to_check = self._type_mapper.map_path_to_str(video)
            return current == to_check
        return False

    def open_subtitles(self, subtitles: Iterable[Path]) -> None:
        def _load() -> None:
            for subtitle in subtitles:
                path = self._type_mapper.map_path_to_str(subtitle)
                self.mpv.command("sub-add", path, "select")

        def _cache() -> None:
            self._cached_subtitles |= set(subtitles)

        if self.video_loaded and not self._loading_video:
            _load()
        else:
            _cache()

    def play(self) -> None:
        self.mpv.pause = False

    def pause(self) -> None:
        self.mpv.pause = True

    def handle_key_event(self, key: Qt.Key, modifiers: Qt.KeyboardModifier) -> None:
        if command := self._command_generator.generate_command(key, modifiers):
            self.mpv.command_async("keypress", command)

    def jump_to(self, seconds: int) -> None:
        self.mpv.command_async("seek", seconds, "absolute+exact")

    def press_mouse_left(self) -> None:
        self.mpv.command_async("keydown", "MOUSE_BTN0")

    def press_mouse_middle(self) -> None:
        self.mpv.command_async("keypress", "MOUSE_BTN1")

    def release_mouse_left(self) -> None:
        self.mpv.command_async("keyup", "MOUSE_BTN0")

    def press_mouse_back(self) -> None:
        self.mpv.command_async("keypress", "MOUSE_BTN5")

    def press_mouse_forward(self) -> None:
        self.mpv.command_async("keypress", "MOUSE_BTN6")

    def scroll_up(self) -> None:
        self.mpv.command_async("keypress", "MOUSE_BTN3")

    def scroll_down(self) -> None:
        self.mpv.command_async("keypress", "MOUSE_BTN4")

    def frame_step_forward(self) -> None:
        self.mpv.command_async("frame-step")

    def frame_step_backward(self) -> None:
        self.mpv.command_async("frame-back-step")

    def cycle_subtitle_track(self) -> None:
        self.mpv.command_async("osd-msg", "cycle", "sub")

    def cycle_audio_track(self) -> None:
        self.mpv.command_async("osd-msg", "cycle", "audio")

    def terminate(self) -> None:
        self.mpv.terminate()


class _DimensionsCoordinator:
    def __init__(self, on_both_ready: Callable[[int, int], None]) -> None:
        self._on_both_ready = on_both_ready
        self._pending_width: int | None = None
        self._pending_height: int | None = None

    def on_width(self, value: int) -> None:
        self._pending_width = value
        self._check()

    def on_height(self, value: int) -> None:
        self._pending_height = value
        self._check()

    def reset(self) -> None:
        self._pending_width = None
        self._pending_height = None

    def _check(self) -> None:
        if self._pending_width and self._pending_height:
            self._on_both_ready(self._pending_width, self._pending_height)
            self.reset()


@dataclass(frozen=True)
class TrackListEntry:
    type: str
    external: bool
    external_filename: str

    @classmethod
    def from_dict(cls, data: dict) -> TrackListEntry:
        return cls(
            type=data.get("type", ""),
            external=data.get("external", False),
            external_filename=data.get("external-filename", ""),
        )
