# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from PySide6.QtCore import QCoreApplication

if TYPE_CHECKING:
    from collections.abc import Callable

    from mpvqc.player.services import RawPropertyValue, RenderContext


class RecordingPlayerHandle:
    """Stands in for mpv: records what the service asked of it, and pushes raw property values
    and the file-loaded event back through the observers the service registered.

    The two property paths stay apart, so a test can drive either alone: `properties` is what
    `get_property` answers, and a push reaches the observers without writing it.
    """

    def __init__(self) -> None:
        self.opened_with: dict = {}
        self.closed = False
        self.commands: list[tuple] = []
        self.async_commands: list[tuple] = []
        self.properties: dict[str, RawPropertyValue] = {}
        self._observers: dict[str, Callable[[str, RawPropertyValue], None]] = {}
        self._file_loaded: Callable[[], None] | None = None

    def open(self, args: dict) -> None:
        self.opened_with = args

    def close(self) -> None:
        self.closed = True

    def command(self, name: str, *args: object) -> None:
        self.commands.append((name, *args))

    def command_async(self, name: str, *args: object) -> None:
        self.async_commands.append((name, *args))

    def get_property(self, name: str) -> RawPropertyValue:
        return self.properties.get(name)

    def set_property(self, name: str, value: RawPropertyValue) -> None:
        self.properties[name] = value

    def observe_property(self, name: str, observer: Callable[[str, RawPropertyValue], None]) -> None:
        self._observers[name] = observer

    def on_file_loaded(self, callback: Callable[[], None]) -> None:
        self._file_loaded = callback

    def create_render_context(
        self,
        get_proc_address: Callable,
        display_params: dict[str, int],
        on_update: Callable[[], None],
    ) -> RenderContext:
        msg = "The recording handle draws nothing; only mpv can render"
        raise NotImplementedError(msg)

    def push_property(self, name: str, raw: RawPropertyValue) -> None:
        self._observers[name](name, raw)

    def push_file_loaded(self) -> None:
        if self._file_loaded is None:
            msg = "Nothing observes the file-loaded event"
            raise RuntimeError(msg)
        self._file_loaded()

    def load_video(self, path: str) -> None:
        self._push_and_pump("path", path)
        self._push_and_pump("filename", Path(path).name)

    def unload_video(self) -> None:
        self.properties.pop("time-pos", None)
        self._push_and_pump("path", None)

    def update(
        self,
        *,
        duration: float | None = None,
        percent_pos: float | None = None,
        time_pos: float | None = None,
        time_remaining: float | None = None,
        height: int | None = None,
        width: int | None = None,
        track_list: list[dict] | None = None,
    ) -> None:
        if duration is not None:
            # the reducer matches float instances, an int literal would be dropped
            self._push_and_pump("duration", duration + 0.0)
        if percent_pos is not None:
            self._push_and_pump("percent-pos", percent_pos)
        if time_pos is not None:
            self.properties["time-pos"] = time_pos
            self._push_and_pump("time-pos", time_pos)
        if time_remaining is not None:
            self._push_and_pump("time-remaining", time_remaining)
        if height is not None:
            self._push_and_pump("height", height)
        if width is not None:
            self._push_and_pump("width", width)
        if track_list is not None:
            self._push_and_pump("track-list", track_list)

    def _push_and_pump(self, name: str, raw: RawPropertyValue) -> None:
        self.push_property(name, raw)
        # the marshal hands updates to the event loop, and a test asserts right after the call
        QCoreApplication.processEvents()
