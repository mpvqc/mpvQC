# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from PySide6.QtGui import QGuiApplication, QWindow


class WindowRevealer(Protocol):
    def install(self, app: QGuiApplication, main_window: QWindow) -> None: ...


class NoWindowRevealer:
    """For platforms whose windows never reach the screen without content."""

    def install(self, app: QGuiApplication, main_window: QWindow) -> None:
        pass
