# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from mpvqc.services.platform.backend import PlatformBackend
from mpvqc.services.platform.surface import NoSurfaceHandler
from mpvqc.services.platform.window_buttons import StaticWindowButtons

from .frame_integration import WindowsFrameIntegration
from .reveal_filter import WindowRevealFilter
from .window_state import WindowsWindowStateHandler


def create_windows_backend() -> PlatformBackend:
    frame = WindowsFrameIntegration()
    return PlatformBackend(
        keeps_native_frame=True,
        draws_drop_shadow=False,
        embeds_native_player=True,
        window_state=WindowsWindowStateHandler(),
        surface=NoSurfaceHandler(),
        window_configuration=frame,
        window_reveal=WindowRevealFilter(),
        embedded_player=frame,
        window_buttons=StaticWindowButtons(),
    )
