# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from collections.abc import Callable

    from mpv import MPV, MpvEvent

    from .state import RawPropertyValue


class RenderContext(Protocol):
    def render(self, *, flip_y: bool, opengl_fbo: dict[str, int]) -> None: ...

    def free(self) -> None: ...


class PlayerHandle(Protocol):
    """The port for mpv using mpv naming convention."""

    def open(self, args: dict) -> None: ...

    def close(self) -> None: ...

    def command(self, name: str, *args: object) -> None: ...

    def command_async(self, name: str, *args: object) -> None: ...

    def get_property(self, name: str) -> RawPropertyValue: ...

    def set_property(self, name: str, value: RawPropertyValue) -> None: ...

    def observe_property(self, name: str, observer: Callable[[str, RawPropertyValue], None]) -> None: ...

    def on_file_loaded(self, callback: Callable[[], None]) -> None: ...

    def on_file_load_failed(self, callback: Callable[[], None]) -> None: ...

    def create_render_context(
        self,
        get_proc_address: Callable,
        display_params: dict[str, int],
        on_update: Callable[[], None],
    ) -> RenderContext: ...


class MpvPlayerHandle:
    """Speaks to mpv, the one module that names the library."""

    def __init__(self) -> None:
        self._mpv: MPV | None = None
        self._observers: list[tuple[str, Callable[[str, RawPropertyValue], None]]] = []
        self._file_loaded: Callable[[], None] | None = None
        self._file_load_failed: Callable[[], None] | None = None

    def open(self, args: dict) -> None:
        from mpv import MPV

        mpv = MPV(**args)

        for name, observer in self._observers:
            mpv.observe_property(name, observer)

        if (on_loaded := self._file_loaded) is not None:
            mpv.event_callback("file-loaded")(lambda _event: on_loaded())

        if (on_failed := self._file_load_failed) is not None:
            mpv.event_callback("end-file")(_only_on_error(on_failed))

        self._mpv = mpv

    def close(self) -> None:
        self._player.terminate()

    def command(self, name: str, *args: object) -> None:
        self._player.command(name, *args)

    def command_async(self, name: str, *args: object) -> None:
        self._player.command_async(name, *args)

    def get_property(self, name: str) -> RawPropertyValue:
        if (mpv := self._mpv) is None:
            return None
        return getattr(mpv, _as_attribute(name))

    def set_property(self, name: str, value: RawPropertyValue) -> None:
        setattr(self._player, _as_attribute(name), value)

    def observe_property(self, name: str, observer: Callable[[str, RawPropertyValue], None]) -> None:
        self._observers.append((name, observer))

    def on_file_loaded(self, callback: Callable[[], None]) -> None:
        self._file_loaded = callback

    def on_file_load_failed(self, callback: Callable[[], None]) -> None:
        self._file_load_failed = callback

    def create_render_context(
        self,
        get_proc_address: Callable,
        display_params: dict[str, int],
        on_update: Callable[[], None],
    ) -> RenderContext:
        from mpv import MpvGlGetProcAddressFn, MpvRenderContext

        context = MpvRenderContext(
            mpv=self._player,
            api_type="opengl",
            opengl_init_params={"get_proc_address": MpvGlGetProcAddressFn(get_proc_address)},
            **display_params,
        )
        context.update_cb = on_update
        return context

    @property
    def _player(self) -> MPV:
        if (mpv := self._mpv) is None:
            msg = "The player handle has not been opened"
            raise RuntimeError(msg)
        return mpv


def _only_on_error(callback: Callable[[], None]) -> Callable[[MpvEvent], None]:
    from mpv import MpvEventEndFile

    def on_end_file(event: MpvEvent) -> None:
        if event.data.reason == MpvEventEndFile.ERROR:
            callback()

    return on_end_file


def _as_attribute(name: str) -> str:
    """python-mpv serves every mpv property as an attribute, with the dashes turned into underscores."""
    return name.replace("-", "_")
