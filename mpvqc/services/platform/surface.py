# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from collections.abc import Callable

    from PySide6.QtGui import QWindow


class SurfaceHandler(Protocol):
    """Owns the drop shadow margin."""

    def drop_shadow_margin(self, window: QWindow) -> int: ...

    def on_drop_shadow_margin_changed(self, callback: Callable[[int], None]) -> None: ...


class NoSurfaceHandler:
    """For platforms where the app draws no drop shadow."""

    def drop_shadow_margin(self, window: QWindow) -> int:  # noqa: ARG002
        return 0

    def on_drop_shadow_margin_changed(self, callback: Callable[[int], None]) -> None:
        """The margin is always zero here, so it never changes."""
