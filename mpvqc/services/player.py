# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import TYPE_CHECKING, cast, override

import inject
from PySide6.QtCore import Property, QObject, Signal, SignalInstance

from .application_paths import ApplicationPathsService
from .host_integration import HostIntegrationService
from .type_mapper import TypeMapperService

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable
    from typing import Any, ClassVar

    from mpv import MPV, MpvRenderContext

logger = logging.getLogger(__name__)


class MpvProperty[TRaw, T]:
    name: ClassVar[str]
    initial: ClassVar[Any]

    def __init__(self, signal: SignalInstance) -> None:
        self._signal = signal
        self._cached: T = self.initial
        self._listeners: list[Callable[[T], object]] = []

    def transform(self, raw: TRaw) -> T:
        return cast("T", raw)

    def on_change(self, listener: Callable[[T], object]) -> None:
        self._listeners.append(listener)

    def on_update(self, raw: TRaw | None) -> None:
        if raw is None:
            return
        new_value = self.transform(raw)
        self.set(new_value)

    def set(self, new_value: T) -> None:
        if self._cached == new_value:
            return
        self._cached = new_value
        self._signal.emit(new_value)
        for listener in self._listeners:
            listener(new_value)

    @property
    def cached(self) -> T:
        return self._cached


class DurationProperty(MpvProperty[float, float]):
    name: ClassVar[str] = "duration"
    initial: ClassVar[float] = 0.0


class PercentPosProperty(MpvProperty[float, int]):
    name: ClassVar[str] = "percent-pos"
    initial: ClassVar[int] = 0

    @override
    def transform(self, raw: float) -> int:
        return int(raw + 0.5)


class TimePosProperty(MpvProperty[float, int]):
    name: ClassVar[str] = "time-pos"
    initial: ClassVar[int] = 0

    @override
    def transform(self, raw: float) -> int:
        return int(raw + 0.5)


class TimeRemainingProperty(MpvProperty[float, int]):
    name: ClassVar[str] = "time-remaining"
    initial: ClassVar[int] = 0

    @override
    def transform(self, raw: float) -> int:
        return int(raw + 0.5)


class PathProperty(MpvProperty[str, str]):
    name: ClassVar[str] = "path"
    initial: ClassVar[str] = ""


class VideoLoadedProperty(MpvProperty[str, bool]):
    name: ClassVar[str] = "path"
    initial: ClassVar[bool] = False

    @override
    def on_update(self, raw: str | None) -> None:
        self.set(raw is not None)


class FilenameProperty(MpvProperty[str, str]):
    name: ClassVar[str] = "filename"
    initial: ClassVar[str] = ""


class HeightProperty(MpvProperty[int, int]):
    name: ClassVar[str] = "height"
    initial: ClassVar[int] = 0


class WidthProperty(MpvProperty[int, int]):
    name: ClassVar[str] = "width"
    initial: ClassVar[int] = 0


class AudioTrackCountProperty(MpvProperty[list[dict], int]):
    name: ClassVar[str] = "track-list"
    initial: ClassVar[int] = 0

    @override
    def transform(self, raw: list[dict]) -> int:
        return sum(1 for entry in raw if entry.get("type") == "audio")


class SubtitleTrackCountProperty(MpvProperty[list[dict], int]):
    name: ClassVar[str] = "track-list"
    initial: ClassVar[int] = 0

    @override
    def transform(self, raw: list[dict]) -> int:
        return sum(1 for entry in raw if entry.get("type") == "sub")


class ExternalSubtitlesProperty(MpvProperty[list[dict], tuple[str, ...]]):
    name: ClassVar[str] = "track-list"
    initial: ClassVar[tuple[str, ...]] = ()

    @override
    def transform(self, raw: list[dict]) -> tuple[str, ...]:
        external = {
            str(Path(entry.get("external-filename", "")).resolve())
            for entry in raw
            if entry.get("external") and entry.get("type") == "sub"
        }
        return tuple(sorted(external))


class DimensionsCoordinator:
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


class SubtitleLoadCoordinator:
    def __init__(self, on_flush: Callable[[Iterable[Path]], None]) -> None:
        self._on_flush = on_flush
        self._cache: set[Path] = set()
        self._loading = False

    @property
    def is_loading(self) -> bool:
        return self._loading

    @property
    def cached(self) -> set[Path]:
        return self._cache

    def begin_loading(self) -> None:
        self._loading = True

    def queue(self, subtitles: Iterable[Path]) -> None:
        self._cache |= set(subtitles)

    def on_video_loaded(self, loaded: bool) -> None:
        if loaded and self._loading:
            self._loading = False
            if self._cache:
                self._on_flush(self._cache)
                self._cache.clear()


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
        self._observed: list[MpvProperty[Any, Any]] = []
        self._dimensions_coordinator = DimensionsCoordinator(on_both_ready=self.video_dimensions_changed.emit)
        self._subtitle_coordinator = SubtitleLoadCoordinator(on_flush=self._load_subtitles_now)

        def register[P: MpvProperty[Any, Any]](prop: P) -> P:
            self._observed.append(prop)
            return prop

        self._duration_prop = register(DurationProperty(self.duration_changed))
        self._percent_pos_prop = register(PercentPosProperty(self.percent_pos_changed))
        self._time_pos_prop = register(TimePosProperty(self.time_pos_changed))
        self._time_remaining_prop = register(TimeRemainingProperty(self.time_remaining_changed))
        self._path_prop = register(PathProperty(self.path_changed))
        self._video_loaded_prop = register(VideoLoadedProperty(self.video_loaded_changed))
        self._filename_prop = register(FilenameProperty(self.filename_changed))
        self._height_prop = register(HeightProperty(self.height_changed))
        self._width_prop = register(WidthProperty(self.width_changed))
        self._audio_track_count_prop = register(AudioTrackCountProperty(self.audio_track_count_changed))
        self._subtitle_track_count_prop = register(SubtitleTrackCountProperty(self.subtitle_track_count_changed))
        self._external_subtitles_prop = register(ExternalSubtitlesProperty(self.external_subtitles_changed))

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
