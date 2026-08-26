# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

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
