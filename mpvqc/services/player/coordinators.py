# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable
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
    def __init__(self, on_add: Callable[[tuple[Path, ...]], None]) -> None:
        self._on_add = on_add
        self._pending: tuple[Path, ...] | None = None

    def attach_or_queue(self, subtitles: tuple[Path, ...], *, video_loaded: bool) -> None:
        if not subtitles:
            return
        if video_loaded:
            self._on_add(subtitles)
        else:
            self._queue(subtitles)

    def queue_for_next_load(self, subtitles: tuple[Path, ...]) -> None:
        self._queue(subtitles)

    def flush(self) -> None:
        pending, self._pending = self._pending, None
        if pending:
            self._on_add(pending)

    def _queue(self, subtitles: tuple[Path, ...]) -> None:
        existing = self._pending or ()
        self._pending = tuple(dict.fromkeys((*existing, *subtitles)))
