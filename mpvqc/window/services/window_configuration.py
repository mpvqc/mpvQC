# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from PySide6.QtGui import QGuiApplication, QWindow


class WindowConfigurator(Protocol):
    def configure_window(self, app: QGuiApplication, window: QWindow) -> None: ...


class NoWindowConfigurator:
    """For platforms where the stock Qt window needs no extra configuration."""

    def configure_window(self, app: QGuiApplication, window: QWindow) -> None:
        pass
