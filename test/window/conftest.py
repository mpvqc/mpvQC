# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QObject, Signal

from mpvqc.window.services import WindowStateSnapshot


class PlatformServiceStub(QObject):
    """Carries a real drop_shadow_margin_changed signal so tests can drive pushes."""

    drop_shadow_margin_changed = Signal(int)

    def __init__(self) -> None:
        super().__init__()
        self.keeps_native_frame = False
        self.draws_drop_shadow = True
        self.read_state = MagicMock(return_value=WindowStateSnapshot(is_fullscreen=False, is_maximized=False))
        self.drop_shadow_margin = MagicMock(return_value=0)
        self.configure_window = MagicMock()
        self.minimize = MagicMock()
        self.maximize = MagicMock()
        self.show_normal = MagicMock()
        self.enter_fullscreen = MagicMock()
        self.exit_fullscreen = MagicMock()


@pytest.fixture
def platform_service_stub() -> PlatformServiceStub:
    return PlatformServiceStub()
