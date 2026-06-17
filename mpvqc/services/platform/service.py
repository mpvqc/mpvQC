# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
import sys
from functools import cached_property
from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal

from .desktop_environment import is_tiling_window_manager
from .window_buttons import DEFAULT_WINDOW_BUTTON_PREFERENCE, WindowButtonPreference, read_window_button_preference
from .window_integration import select_window_integration

if TYPE_CHECKING:
    from PySide6.QtGui import QGuiApplication, QWindow

logger = logging.getLogger(__name__)


class PlatformService(QObject):
    """Single entry point for OS- and desktop-specific window behavior.

    Hides the platform hacks (native window configuration, desktop-environment
    queries) behind one interface. Delegates to focused collaborators so each
    hack stays in its own module and can be removed cleanly once Qt grows a
    native equivalent.
    """

    window_button_preference_changed = Signal(object)

    def __init__(self) -> None:
        super().__init__()
        self._window = select_window_integration()
        self._window_button_preference = DEFAULT_WINDOW_BUTTON_PREFERENCE
        self._detect_window_button_preference_async()

    def _detect_window_button_preference_async(self) -> None:
        def job() -> None:
            preference = read_window_button_preference()
            if preference != self._window_button_preference:
                self._window_button_preference = preference
                self.window_button_preference_changed.emit(preference)

        QThreadPool.globalInstance().start(QRunnable.create(job))

    @property
    def window_button_preference(self) -> WindowButtonPreference:
        return self._window_button_preference

    @cached_property
    def is_tiling_window_manager(self) -> bool:
        if sys.platform != "linux":
            return False
        return is_tiling_window_manager()

    def configure_window(self, app: QGuiApplication, window: QWindow) -> None:
        self._window.configure_for(app, window)

    def set_embedded_player_hwnd(self, win_id: int) -> None:
        self._window.set_embedded_player_hwnd(win_id)
