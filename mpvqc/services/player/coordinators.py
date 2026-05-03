# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable
    from pathlib import Path


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
