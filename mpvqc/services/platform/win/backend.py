# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from mpvqc.services.platform.backend import PlatformBackend
from mpvqc.services.platform.content_margins import NoContentMarginsApplier
from mpvqc.services.platform.window_buttons import StaticWindowButtons

from .frame_integration import WindowsFrameIntegration
from .fullscreen import WindowsFullscreenHandler


def create_windows_backend() -> PlatformBackend:
    frame = WindowsFrameIntegration()
    return PlatformBackend(
        root_qml_url="qrc:/qt/qml/MpvqcApplicationWindows.qml",
        draws_own_shadow=False,
        owns_window_geometry=False,
        fullscreen=WindowsFullscreenHandler(),
        window_configuration=frame,
        embedded_player=frame,
        content_margins=NoContentMarginsApplier(),
        window_buttons=StaticWindowButtons(),
    )
