# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import TYPE_CHECKING

import inject
from PySide6.QtCore import Property, QObject, Signal

import mpvqc.services.player.properties as props
from mpvqc.services.application_paths import ApplicationPathsService
from mpvqc.services.host_integration import HostIntegrationService
from mpvqc.services.player.coordinators import DimensionsCoordinator, SubtitleLoadCoordinator
from mpvqc.services.type_mapper import TypeMapperService

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable
    from typing import Any

    from mpv import MPV, MpvRenderContext

logger = logging.getLogger(__name__)


class PlayerService(QObject):
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
    external_subtitles_changed = Signal(list)

    def __init__(self) -> None:
        super().__init__()

        self._mpv: MPV | None = None
        self._observed: list[props.MpvProperty[Any, Any]] = []
        self._dimensions_coordinator = DimensionsCoordinator(on_both_ready=self.video_dimensions_changed.emit)
        self._subtitle_coordinator = SubtitleLoadCoordinator(on_flush=self._load_subtitles_now)

        def register[P: props.MpvProperty[Any, Any]](prop: P) -> P:
            self._observed.append(prop)
            return prop

        self._duration_prop = register(props.Duration(self.duration_changed))
        self._percent_pos_prop = register(props.PercentPos(self.percent_pos_changed))
        self._time_pos_prop = register(props.TimePos(self.time_pos_changed))
        self._time_remaining_prop = register(props.TimeRemaining(self.time_remaining_changed))
        self._path_prop = register(props.Path(self.path_changed))
        self._video_loaded_prop = register(props.VideoLoaded(self.video_loaded_changed))
        self._filename_prop = register(props.Filename(self.filename_changed))
        self._height_prop = register(props.Height(self.height_changed))
        self._width_prop = register(props.Width(self.width_changed))
        self._audio_track_count_prop = register(props.AudioTrackCount(self.audio_track_count_changed))
        self._subtitle_track_count_prop = register(props.SubtitleTrackCount(self.subtitle_track_count_changed))
        self._external_subtitles_prop = register(props.ExternalSubtitles(self.external_subtitles_changed))

        self._path_prop.on_change(lambda _: self._dimensions_coordinator.reset())
        self._video_loaded_prop.on_change(self._subtitle_coordinator.on_video_loaded)
        self._height_prop.on_change(self._dimensions_coordinator.on_height)
        self._width_prop.on_change(self._dimensions_coordinator.on_width)

    def init(self, win_id: int | None = None) -> None:
        args = {"vo": "libmpv"} if win_id is None else {"wid": win_id}
        merged_args = self._build_init_args() | args

        from mpv import MPV

        mpv = MPV(**merged_args)

        for prop in self._observed:
            mpv.observe_property(prop.name, lambda _, v, p=prop: p.on_update(v))

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
            "ytdl": "yes",
        }

        if os.getenv("MPVQC_DEBUG") or os.getenv("MPVQC_PLAYER_LOG"):
            mpv_log_level = 25

            def player_logger(level: str, context: str, message: str) -> None:
                logger.log(mpv_log_level, message.rstrip(), extra={"mpv_level": level, "mpv_context": context})

            args["log_handler"] = player_logger

        return args

    @property
    def _mpv_player(self) -> MPV:
        if self._mpv is None:
            msg = "MPV player has not been initialized"
            raise RuntimeError(msg)
        return self._mpv

    def create_render_context(self, get_proc_address: Callable) -> MpvRenderContext:
        from mpv import MpvGlGetProcAddressFn, MpvRenderContext

        return MpvRenderContext(
            mpv=self._mpv_player,
            api_type="opengl",
            opengl_init_params={"get_proc_address": MpvGlGetProcAddressFn(get_proc_address)},
        )

    @property
    def mpv_version(self) -> str:
        return str(self._mpv.mpv_version or "") if self._mpv is not None else ""

    @property
    def ffmpeg_version(self) -> str:
        return str(self._mpv.ffmpeg_version or "") if self._mpv is not None else ""

    @property
    def path(self) -> str:
        return self._path_prop.cached

    @property
    def filename(self) -> str:
        return self._filename_prop.cached

    @property
    def percent_pos(self) -> int:
        return self._percent_pos_prop.cached

    @property
    def time_pos(self) -> int:
        return self._time_pos_prop.cached

    @property
    def time_remaining(self) -> int:
        return self._time_remaining_prop.cached

    @property
    def height(self) -> int:
        return self._height_prop.cached

    @property
    def width(self) -> int:
        return self._width_prop.cached

    @property
    def video_loaded(self) -> bool:
        return self._video_loaded_prop.cached

    @property
    def duration(self) -> float:
        return self._duration_prop.cached

    @property
    def external_subtitles(self) -> tuple[str, ...]:
        return self._external_subtitles_prop.cached

    @Property(int, notify=audio_track_count_changed)
    def audio_track_count(self) -> int:
        return self._audio_track_count_prop.cached

    @Property(int, notify=subtitle_track_count_changed)
    def subtitle_track_count(self) -> int:
        return self._subtitle_track_count_prop.cached

    def move_mouse(self, x: int, y: int) -> None:
        if self._mpv is None:
            logger.debug("Ignoring mouse move; player not yet initialized")
            return
        zoom_factor = self._host_integration.display_zoom_factor
        x = int(x * zoom_factor)
        y = int(y * zoom_factor)
        self._mpv_player.command_async("mouse", x, y)

    def open_video(self, video: Path) -> None:
        self._subtitle_coordinator.begin_loading()
        path = self._type_mapper.map_path_to_str(video)
        self._mpv_player.command("loadfile", path, "replace")
        self.play()

    def is_video_loaded(self, video: Path) -> bool:
        if path := self.path:
            return Path(path).resolve() == video.resolve()
        return False

    def open_subtitles(self, subtitles: Iterable[Path]) -> None:
        if self.video_loaded and not self._subtitle_coordinator.is_loading:
            self._load_subtitles_now(subtitles)
        else:
            self._subtitle_coordinator.queue(subtitles)

    def _load_subtitles_now(self, subtitles: Iterable[Path]) -> None:
        for subtitle in subtitles:
            path = self._type_mapper.map_path_to_str(subtitle)
            self._mpv_player.command("sub-add", path, "select")

    def play(self) -> None:
        self._mpv_player.pause = False

    def pause(self) -> None:
        self._mpv_player.pause = True

    def press_key(self, command: str) -> None:
        self._mpv_player.command_async("keypress", command)

    def jump_to(self, seconds: int) -> None:
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

    def terminate(self) -> None:
        self._mpv_player.terminate()
