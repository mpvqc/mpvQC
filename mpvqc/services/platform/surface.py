# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from collections.abc import Callable

    from PySide6.QtGui import QWindow


class SurfaceHandler(Protocol):
    """Owns the decorated padding around the window content: the state-aware
    margin read and the edge-triggered push when the margin changes."""

    def drop_shadow_margin(self, window: QWindow) -> int: ...

    def on_drop_shadow_margin_changed(self, callback: Callable[[int], None]) -> None: ...


class NoSurfaceHandler:
    """For platforms without a client-side-decorated surface."""

    def drop_shadow_margin(self, window: QWindow) -> int:  # noqa: ARG002
        return 0

    def on_drop_shadow_margin_changed(self, callback: Callable[[int], None]) -> None:
        """The margin is always zero here, so nothing ever pushes."""
