# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path


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
