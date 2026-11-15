# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Protocol


class EmbeddedPlayerTracker(Protocol):
    def track(self, win_id: int) -> None: ...


class NoEmbeddedPlayerTracker:
    """For platforms without an embedded player."""

    def track(self, win_id: int) -> None:
        pass
