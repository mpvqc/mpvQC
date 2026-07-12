# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from mpvqc.services.platform.backend import PlatformBackend
from mpvqc.services.platform.content_margins import NoContentMarginsApplier
from mpvqc.services.platform.embedded_player import NoEmbeddedPlayerTracker
from mpvqc.services.platform.fullscreen import QtFullscreenHandler
from mpvqc.services.platform.window_configuration import NoWindowConfigurator
from mpvqc.services.platform.window_reveal import NoWindowRevealer

from .surface import SurfaceController
from .window_button_detector import WindowButtonDetector

_ROOT_QML_URL = "qrc:/qt/qml/MpvqcApplicationLinux.qml"


def create_desktop_backend() -> PlatformBackend:
    surface = SurfaceController()
    return PlatformBackend(
        root_qml_url=_ROOT_QML_URL,
        draws_own_shadow=True,
        owns_window_geometry=False,
        fullscreen=QtFullscreenHandler(),
        window_configuration=surface,
        window_reveal=NoWindowRevealer(),
        embedded_player=NoEmbeddedPlayerTracker(),
        content_margins=surface,
        window_buttons=_create_window_button_detector(),
    )


def create_window_manager_backend() -> PlatformBackend:
    return PlatformBackend(
        root_qml_url=_ROOT_QML_URL,
        draws_own_shadow=False,
        # Ideally this would follow whether the compositor currently tiles the
        # window, but Qt does not expose that state
        owns_window_geometry=True,
        fullscreen=QtFullscreenHandler(),
        # The window manager owns sizing and placement; nothing to set up.
        window_configuration=NoWindowConfigurator(),
        window_reveal=NoWindowRevealer(),
        embedded_player=NoEmbeddedPlayerTracker(),
        content_margins=NoContentMarginsApplier(),
        window_buttons=_create_window_button_detector(),
    )


def _create_window_button_detector() -> WindowButtonDetector:
    detector = WindowButtonDetector()
    detector.detect()
    return detector
