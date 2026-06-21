# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import TYPE_CHECKING

import inject
from PySide6.QtCore import Property, QObject, Qt, Signal, Slot

from mpvqc.services.application_paths import ApplicationPathsService
from mpvqc.services.build_info import BuildInfoService
from mpvqc.services.main_window import MainWindowService
from mpvqc.services.type_mapper import TypeMapperService

from .coordinators import SubtitleLoadCoordinator
from .state import OBSERVED_PROPERTIES, PlayerState, make_observer, reduce_update

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

    from mpv import MPV, MpvRenderContext
    from PySide6.QtCore import SignalInstance

    from .state import RawPropertyValue

logger = logging.getLogger(__name__)


class PlayerService(QObject):
    _build_info = inject.attr(BuildInfoService)
    _main_window = inject.attr(MainWindowService)
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
    external_subtitles_changed = Signal(list)

    file_loaded = Signal()

    _property_updated = Signal(str, object)

    def __init__(self) -> None:
        super().__init__()

        self._mpv: MPV | None = None
        self._shutdown_hook: Callable[[], None] | None = None
        self._state = PlayerState()
        self._subtitle_coordinator = SubtitleLoadCoordinator(on_add=self._load_subtitles_now)
        self._notifiers: dict[str, SignalInstance] = {
            "duration": self.duration_changed,
            "percent_pos": self.percent_pos_changed,
            "time_pos": self.time_pos_changed,
            "time_remaining": self.time_remaining_changed,
            "path": self.path_changed,
            "video_loaded": self.video_loaded_changed,
            "filename": self.filename_changed,
            "height": self.height_changed,
            "width": self.width_changed,
            "audio_track_count": self.audio_track_count_changed,
            "subtitle_track_count": self.subtitle_track_count_changed,
            "external_subtitles": self.external_subtitles_changed,
        }

        self._property_updated.connect(self._apply_property_update, Qt.ConnectionType.QueuedConnection)
        self.file_loaded.connect(self._on_file_loaded, Qt.ConnectionType.QueuedConnection)

    def init(self, win_id: int | None = None) -> None:
        args = {"vo": "libmpv"} if win_id is None else {"wid": win_id}
        merged_args = self._build_init_args() | args

        from mpv import MPV

        mpv = MPV(**merged_args)

        for spec in OBSERVED_PROPERTIES:
            mpv.observe_property(spec.name, make_observer(spec, self._property_updated.emit))

        mpv.event_callback("file-loaded")(lambda _event: self.file_loaded.emit())

        self._mpv = mpv

    def _build_init_args(self) -> dict:
        args: dict = {
            "keep_open": "yes",
            "idle": "yes",
            "osc": "yes",
            "cursor_autohide": "no",
            "input_cursor": "no",
            "input_default_bindings": "no",
            "config": "yes",
            "config_dir": self._type_mapper.map_path_to_str(self._paths.dir_config),
            "screenshot_directory": self._type_mapper.map_path_to_str(self._paths.dir_screenshots),
            "audio_client_name": self._build_info.name,
            "ytdl": "yes",
        }

        if os.getenv("MPVQC_DEBUG") or os.getenv("MPVQC_PLAYER_LOG"):
            mpv_log_level = 25

            def player_logger(level: str, context: str, message: str) -> None:
                logger.log(mpv_log_level, message.rstrip(), extra={"mpv_level": level, "mpv_context": context})

            args["log_handler"] = player_logger

        return args

    @Slot(str, object)
    def _apply_property_update(self, name: str, raw: RawPropertyValue) -> None:
        old = self._state
        new = reduce_update(old, name, raw)
        if new is old or new == old:
            return
        self._state = new
        self._emit_field_changes(old, new)
        self._emit_transitions(old, new)

    def _emit_field_changes(self, old: PlayerState, new: PlayerState) -> None:
        for field_name, signal in self._notifiers.items():
            if (value := getattr(new, field_name)) != getattr(old, field_name):
                signal.emit(value)

    def _emit_transitions(self, old: PlayerState, new: PlayerState) -> None:
        if new.has_dimensions and not old.has_dimensions:
            self.video_dimensions_changed.emit(new.width, new.height)

    @property
    def _mpv_player(self) -> MPV:
        if self._mpv is None:
            msg = "MPV player has not been initialized"
            raise RuntimeError(msg)
        return self._mpv

    def create_render_context(self, get_proc_address: Callable, display_params: dict[str, int]) -> MpvRenderContext:
        from mpv import MpvGlGetProcAddressFn, MpvRenderContext

        return MpvRenderContext(
            mpv=self._mpv_player,
            api_type="opengl",
            opengl_init_params={"get_proc_address": MpvGlGetProcAddressFn(get_proc_address)},
            **display_params,
        )

    @property
    def mpv_version(self) -> str:
        return str(self._mpv.mpv_version or "") if self._mpv is not None else ""

    @property
    def ffmpeg_version(self) -> str:
        return str(self._mpv.ffmpeg_version or "") if self._mpv is not None else ""

    @property
    def path(self) -> str:
        return self._state.path

    @property
    def filename(self) -> str:
        return self._state.filename

    @property
    def percent_pos(self) -> int:
        return self._state.percent_pos

    @property
    def time_pos(self) -> int:
        return self._state.time_pos

    @property
    def exact_time_pos(self) -> float:
        if self._mpv is not None and (raw := self._mpv.time_pos) is not None:
            return raw
        return float(self._state.time_pos)

    @property
    def time_remaining(self) -> int:
        return self._state.time_remaining

    @property
    def height(self) -> int:
        return self._state.height

    @property
    def width(self) -> int:
        return self._state.width

    @property
    def video_loaded(self) -> bool:
        return self._state.video_loaded

    @property
    def duration(self) -> float:
        return self._state.duration

    @property
    def external_subtitles(self) -> tuple[str, ...]:
        return self._state.external_subtitles

    @Property(int, notify=audio_track_count_changed)
    def audio_track_count(self) -> int:
        return self._state.audio_track_count

    @Property(int, notify=subtitle_track_count_changed)
    def subtitle_track_count(self) -> int:
        return self._state.subtitle_track_count

    def move_mouse(self, x: int, y: int) -> None:
        if self._mpv is None:
            logger.debug("Ignoring mouse move; player not yet initialized")
            return
        zoom_factor = self._main_window.display_zoom_factor
        x = int(x * zoom_factor)
        y = int(y * zoom_factor)
        self._mpv_player.command_async("mouse", x, y)

    @staticmethod
    def is_video_path_loaded(loaded_path: str, videos: Iterable[Path]) -> bool:
        if not loaded_path:
            return False
        current = Path(loaded_path).resolve()
        return any(current == video.resolve() for video in videos)

    def is_any_video_loaded(self, videos: Iterable[Path]) -> bool:
        return self.is_video_path_loaded(self.path, videos)

    def open_media(self, *, video: Path | None, subtitles: tuple[Path, ...]) -> None:
        if video is None:
            self._subtitle_coordinator.attach_or_queue(subtitles, video_loaded=self.video_loaded)
            return

        self._subtitle_coordinator.queue_for_next_load(subtitles)
        path = self._type_mapper.map_path_to_str(video)
        self._mpv_player.command("loadfile", path, "replace")
        self.play()

    @Slot()
    def _on_file_loaded(self) -> None:
        self._subtitle_coordinator.flush()

    def _load_subtitles_now(self, subtitles: tuple[Path, ...]) -> None:
        for subtitle in dict.fromkeys(subtitles):
            path = self._type_mapper.map_path_to_str(subtitle)
            self._mpv_player.command("sub-add", path, "select")

    def play(self) -> None:
        self._mpv_player.pause = False

    def pause(self) -> None:
        self._mpv_player.pause = True

    def press_key(self, command: str) -> None:
        self._mpv_player.command_async("keypress", command)

    def jump_to(self, seconds: float) -> None:
        self._mpv_player.command_async("seek", seconds, "absolute+exact")

    def press_mouse_left(self) -> None:
        self._mpv_player.command_async("keydown", "MOUSE_BTN0")

    def release_mouse_left(self) -> None:
        self._mpv_player.command_async("keyup", "MOUSE_BTN0")

    def press_mouse_middle(self) -> None:
        self._mpv_player.command_async("keypress", "MOUSE_BTN1")

    def press_mouse_back(self) -> None:
        self._mpv_player.command_async("keypress", "MOUSE_BTN5")

    def press_mouse_forward(self) -> None:
        self._mpv_player.command_async("keypress", "MOUSE_BTN6")

    def scroll_up(self) -> None:
        self._mpv_player.command_async("keypress", "MOUSE_BTN3")

    def scroll_down(self) -> None:
        self._mpv_player.command_async("keypress", "MOUSE_BTN4")

    def frame_step_forward(self) -> None:
        self._mpv_player.command_async("frame-step")

    def frame_step_backward(self) -> None:
        self._mpv_player.command_async("frame-back-step")

    def cycle_subtitle_track(self) -> None:
        self._mpv_player.command_async("osd-msg", "cycle", "sub")

    def cycle_audio_track(self) -> None:
        self._mpv_player.command_async("osd-msg", "cycle", "audio")

    def set_shutdown_hook(self, hook: Callable[[], None] | None) -> None:
        self._shutdown_hook = hook

    def terminate(self) -> None:
        if self._mpv is None:
            return
        if self._shutdown_hook is not None:
            self._shutdown_hook()
        self._mpv_player.terminate()
