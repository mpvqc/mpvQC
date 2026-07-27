# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from mpvqc.services.platform.backend import PlatformBackend
from mpvqc.services.platform.embedded_player import NoEmbeddedPlayerTracker
from mpvqc.services.platform.surface import NoSurfaceHandler
from mpvqc.services.platform.window_configuration import NoWindowConfigurator
from mpvqc.services.platform.window_reveal import NoWindowRevealer
from mpvqc.services.platform.window_state import QtWindowStateHandler

from .surface import SurfaceController
from .window_button_detector import WindowButtonDetector

_ROOT_QML_URL = "qrc:/qt/qml/MpvqcApplication.qml"


def create_desktop_backend() -> PlatformBackend:
    # Transparent padding around the content that the QML drop shadow is
    # painted into. Must exceed the widest shadow blur plus offset, otherwise
    # the soft edge clips at the surface boundary.
    surface = SurfaceController(shadow_margin=88)

    return PlatformBackend(
        root_qml_url=_ROOT_QML_URL,
        desktop_sizes_window=False,
        window_state=QtWindowStateHandler(),
        surface=surface,
        window_configuration=surface,
        window_reveal=NoWindowRevealer(),
        embedded_player=NoEmbeddedPlayerTracker(),
        window_buttons=_create_window_button_detector(),
    )


def create_tiling_backend() -> PlatformBackend:
    return PlatformBackend(
        root_qml_url=_ROOT_QML_URL,
        desktop_sizes_window=True,
        window_state=QtWindowStateHandler(),
        surface=NoSurfaceHandler(),
        window_configuration=NoWindowConfigurator(),
        window_reveal=NoWindowRevealer(),
        embedded_player=NoEmbeddedPlayerTracker(),
        window_buttons=_create_window_button_detector(),
    )


def _create_window_button_detector() -> WindowButtonDetector:
    detector = WindowButtonDetector()
    detector.detect()
    return detector
