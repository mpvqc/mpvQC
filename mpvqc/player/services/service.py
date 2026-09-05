# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from functools import cached_property
from typing import TYPE_CHECKING

import inject
from PySide6.QtCore import QObject, Qt, Signal

from mpvqc.build import get_build_info
from mpvqc.services import ApplicationPathsService
from mpvqc.shared import map_path_to_str

from .event_marshal import EventMarshal
from .init_args import make_embedded_init_args, make_in_scene_init_args
from .key_command import key_command
from .media_load import (
    IDLE,
    AttachSubtitles,
    DoNothing,
    LoadVideo,
    MediaRequested,
    VideoLoadFailed,
    VideoLoadSucceeded,
    reduce_media_load,
)
from .state import OBSERVED_PROPERTIES, PlayerState, make_observer, reduce_update
from .versions import PlayerVersions, clean_versions

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from PySide6.QtCore import SignalInstance

    from .handle import PlayerHandle, RenderContext
    from .media_load import MediaEvent
    from .state import RawPropertyValue

logger = logging.getLogger(__name__)


class PlayerService(QObject):
    _paths = inject.attr(ApplicationPathsService)

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

    def __init__(self, handle: PlayerHandle) -> None:
        super().__init__()

        self._handle = handle
        self._opened = False
        self._shutdown_hook: Callable[[], None] | None = None

        self._state = PlayerState()
        self._media = IDLE

        self._marshal = EventMarshal()
        self._post_property_update = self._marshal.channel(self._apply_property_update)
        self._post_file_loaded = self._marshal.channel(self._on_file_loaded)
        self._post_file_load_failed = self._marshal.channel(self._on_file_load_failed)

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

        for spec in OBSERVED_PROPERTIES:
            handle.observe_property(spec.name, make_observer(spec, self._post_property_update))

        handle.on_file_loaded(self._post_file_loaded)
        handle.on_file_load_failed(self._post_file_load_failed)

    def open_embedded(self, win_id: int) -> None:
        mpv_init_args = make_embedded_init_args(
            win_id=win_id,
            config_dir=self._paths.dir_config,
            screenshot_directory=self._paths.dir_screenshots,
            audio_client_name=get_build_info().name,
        )
        self._handle.open(mpv_init_args)
        self._opened = True

    def open_in_scene(self) -> None:
        mpv_init_args = make_in_scene_init_args(
            config_dir=self._paths.dir_config,
            screenshot_directory=self._paths.dir_screenshots,
            audio_client_name=get_build_info().name,
        )
        self._handle.open(mpv_init_args)
        self._opened = True

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

    def create_render_context(
        self,
        get_proc_address: Callable,
        display_params: dict[str, int],
        on_update: Callable[[], None],
    ) -> RenderContext:
        return self._handle.create_render_context(get_proc_address, display_params, on_update)

    @cached_property
    def versions(self) -> PlayerVersions:
        return clean_versions(
            mpv=self._handle.get_property("mpv-version"),
            ffmpeg=self._handle.get_property("ffmpeg-version"),
        )

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
        match self._handle.get_property("time-pos"):
            case float() | int() as raw:
                return float(raw)
            case _:
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

    @property
    def audio_track_count(self) -> int:
        return self._state.audio_track_count

    @property
    def subtitle_track_count(self) -> int:
        return self._state.subtitle_track_count

    def move_mouse(self, x: int, y: int) -> None:
        if not self._opened:
            logger.debug("Ignoring mouse move; player not yet initialized")
            return
        self._handle.command_async("mouse", x, y)

    def open_media(self, *, video: Path | None, subtitles: tuple[Path, ...]) -> None:
        self._apply_media_event(MediaRequested(video=video, subtitles=subtitles, video_loaded=self.video_loaded))

    def _on_file_loaded(self) -> None:
        self._apply_media_event(VideoLoadSucceeded())

    def _on_file_load_failed(self) -> None:
        self._apply_media_event(VideoLoadFailed())

    def _apply_media_event(self, event: MediaEvent) -> None:
        self._media, command = reduce_media_load(self._media, event)
        match command:
            case DoNothing():
                pass
            case LoadVideo(path=video):
                self._handle.command("loadfile", map_path_to_str(video), "replace")
                self.play()
            case AttachSubtitles(subtitles=subtitles):
                for subtitle in subtitles:
                    self._handle.command("sub-add", map_path_to_str(subtitle), "select")

    def play(self) -> None:
        self._handle.set_property("pause", False)

    def pause(self) -> None:
        self._handle.set_property("pause", True)

    def forward_key(self, key: Qt.Key, modifiers: Qt.KeyboardModifier) -> None:
        if command := key_command(key, modifiers):
            self._handle.command_async("keypress", command)

    def jump_to(self, seconds: float) -> None:
        self._handle.command_async("seek", seconds, "absolute+exact")

    def press_mouse_left(self) -> None:
        self._handle.command_async("keydown", "MOUSE_BTN0")

    def release_mouse_left(self) -> None:
        self._handle.command_async("keyup", "MOUSE_BTN0")

    def press_mouse_middle(self) -> None:
        self._handle.command_async("keypress", "MOUSE_BTN1")

    def press_mouse_back(self) -> None:
        self._handle.command_async("keypress", "MOUSE_BTN5")

    def press_mouse_forward(self) -> None:
        self._handle.command_async("keypress", "MOUSE_BTN6")

    def scroll_up(self) -> None:
        self._handle.command_async("keypress", "MOUSE_BTN3")

    def scroll_down(self) -> None:
        self._handle.command_async("keypress", "MOUSE_BTN4")

    def frame_step_forward(self) -> None:
        self._handle.command_async("frame-step")

    def frame_step_backward(self) -> None:
        self._handle.command_async("frame-back-step")

    def cycle_subtitle_track(self) -> None:
        self._handle.command_async("osd-msg", "cycle", "sub")

    def cycle_audio_track(self) -> None:
        self._handle.command_async("osd-msg", "cycle", "audio")

    def set_shutdown_hook(self, hook: Callable[[], None] | None) -> None:
        self._shutdown_hook = hook

    def terminate(self) -> None:
        if not self._opened:
            return
        if self._shutdown_hook is not None:
            self._shutdown_hook()
        self._handle.close()
