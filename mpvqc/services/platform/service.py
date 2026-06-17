# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from functools import cached_property
from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal

from .window_buttons import WindowButtonDetector, WindowButtonPreference
from .window_environment import (
    is_tiling_window_manager as detect_tiling_window_manager,
)
from .window_environment import (
    should_draw_own_shadow,
    should_draw_window_border,
    window_root_qml_url,
)
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
        self._integration = select_window_integration()
        self._window_buttons = WindowButtonDetector()
        self._window_buttons.preference_changed.connect(self.window_button_preference_changed)
        self._detect_window_button_preference()

    def _detect_window_button_preference(self) -> None:
        self._window_buttons.detect()

    @property
    def window_button_preference(self) -> WindowButtonPreference:
        return self._window_buttons.preference

    @cached_property
    def is_tiling_window_manager(self) -> bool:
        return detect_tiling_window_manager()

    @property
    def root_qml_url(self) -> str:
        return window_root_qml_url()

    @cached_property
    def draws_own_shadow(self) -> bool:
        return should_draw_own_shadow(is_tiling_wm=self.is_tiling_window_manager)

    @cached_property
    def draws_window_border(self) -> bool:
        return should_draw_window_border()

    def configure_window(self, app: QGuiApplication, window: QWindow) -> None:
        self._integration.configure_for(app, window)

    def set_embedded_player_hwnd(self, win_id: int) -> None:
        self._integration.set_embedded_player_hwnd(win_id)

    def apply_content_margins(self, margin: int) -> None:
        self._integration.apply_content_margins(margin)
