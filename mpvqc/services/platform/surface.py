# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from PySide6.QtGui import QWindow


class SurfaceHandler(Protocol):
    """Owns the decorated padding around the window content: the state-aware
    margin read and the content-margin write."""

    def shadow_margin(self, window: QWindow) -> int: ...

    def apply_content_margins(self, margin: int) -> None: ...


class NoSurfaceHandler:
    """For platforms without a client-side-decorated surface."""

    def shadow_margin(self, window: QWindow) -> int:  # noqa: ARG002
        return 0

    def apply_content_margins(self, margin: int) -> None:
        pass
