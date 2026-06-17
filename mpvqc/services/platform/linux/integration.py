# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, override

from mpvqc.services.platform.linux import LinuxEventFilter
from mpvqc.services.platform.window_integration import WindowIntegration

if TYPE_CHECKING:
    from PySide6.QtGui import QGuiApplication, QWindow


class LinuxWindowIntegration(WindowIntegration):
    @override
    def configure_for(self, app: QGuiApplication, window: QWindow) -> None:
        self._event_filter = LinuxEventFilter(window, app)
        app.installEventFilter(self._event_filter)

    @override
    def set_embedded_player_hwnd(self, win_id: int) -> None:
        pass
