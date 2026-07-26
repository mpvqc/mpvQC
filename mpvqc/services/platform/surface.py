# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Protocol

from PySide6.QtCore import QObject, Signal

if TYPE_CHECKING:
    from PySide6.QtGui import QWindow


class SurfaceHandler(Protocol):
    """Owns the decorated padding around the window content: the state-aware
    margin read and the edge-triggered push when the margin changes."""

    shadow_margin_changed: ClassVar[Signal]

    def shadow_margin(self, window: QWindow) -> int: ...


class NoSurfaceHandler(QObject):
    """For platforms without a client-side-decorated surface."""

    shadow_margin_changed = Signal(int)

    def shadow_margin(self, window: QWindow) -> int:  # noqa: ARG002
        return 0
