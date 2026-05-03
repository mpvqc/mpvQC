# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING, cast, override

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any, ClassVar

    from PySide6.QtCore import SignalInstance


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


class Duration(MpvProperty[float, float]):
    name: ClassVar[str] = "duration"
    initial: ClassVar[float] = 0.0


class PercentPos(MpvProperty[float, int]):
    name: ClassVar[str] = "percent-pos"
    initial: ClassVar[int] = 0

    @override
    def transform(self, raw: float) -> int:
        return int(raw + 0.5)


class TimePos(MpvProperty[float, int]):
    name: ClassVar[str] = "time-pos"
    initial: ClassVar[int] = 0

    @override
    def transform(self, raw: float) -> int:
        return int(raw + 0.5)


class TimeRemaining(MpvProperty[float, int]):
    name: ClassVar[str] = "time-remaining"
    initial: ClassVar[int] = 0

    @override
    def transform(self, raw: float) -> int:
        return int(raw + 0.5)


class Path(MpvProperty[str, str]):
    name: ClassVar[str] = "path"
    initial: ClassVar[str] = ""


class VideoLoaded(MpvProperty[str, bool]):
    name: ClassVar[str] = "path"
    initial: ClassVar[bool] = False

    @override
    def on_update(self, raw: str | None) -> None:
        self.set(raw is not None)


class Filename(MpvProperty[str, str]):
    name: ClassVar[str] = "filename"
    initial: ClassVar[str] = ""


class Height(MpvProperty[int, int]):
    name: ClassVar[str] = "height"
    initial: ClassVar[int] = 0


class Width(MpvProperty[int, int]):
    name: ClassVar[str] = "width"
    initial: ClassVar[int] = 0


class AudioTrackCount(MpvProperty[list[dict], int]):
    name: ClassVar[str] = "track-list"
    initial: ClassVar[int] = 0

    @override
    def transform(self, raw: list[dict]) -> int:
        return sum(1 for entry in raw if entry.get("type") == "audio")


class SubtitleTrackCount(MpvProperty[list[dict], int]):
    name: ClassVar[str] = "track-list"
    initial: ClassVar[int] = 0

    @override
    def transform(self, raw: list[dict]) -> int:
        return sum(1 for entry in raw if entry.get("type") == "sub")


class ExternalSubtitles(MpvProperty[list[dict], tuple[str, ...]]):
    name: ClassVar[str] = "track-list"
    initial: ClassVar[tuple[str, ...]] = ()

    @override
    def transform(self, raw: list[dict]) -> tuple[str, ...]:
        external = {
            str(pathlib.Path(entry.get("external-filename", "")).resolve())
            for entry in raw
            if entry.get("external") and entry.get("type") == "sub"
        }
        return tuple(sorted(external))
