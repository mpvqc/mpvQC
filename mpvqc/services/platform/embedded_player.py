# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import Protocol


class EmbeddedPlayerTracker(Protocol):
    def track(self, win_id: int) -> None: ...


class NoEmbeddedPlayerTracker:
    """For platforms that do not track the embedded player's native window."""

    def track(self, win_id: int) -> None:
        pass
