# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Final

    from PySide6.QtGui import QWindow


@dataclass(frozen=True)
class SurfaceSnapshot:
    draws_own_frame: bool
    drop_shadow_margin: int


NO_OWN_FRAME: Final = SurfaceSnapshot(draws_own_frame=False, drop_shadow_margin=0)


class SurfaceHandler(Protocol):
    def read_surface(self, window: QWindow) -> SurfaceSnapshot: ...

    def on_surface_changed(self, callback: Callable[[SurfaceSnapshot], None]) -> None: ...


class NoSurfaceHandler:
    """For platforms where the app draws no frame of its own."""

    def read_surface(self, window: QWindow) -> SurfaceSnapshot:  # ruff: ignore[unused-method-argument]
        return NO_OWN_FRAME

    def on_surface_changed(self, callback: Callable[[SurfaceSnapshot], None]) -> None:
        """The surface never changes here."""
