# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .capabilities import linux_desktop_capabilities, linux_tiling_capabilities, windows_capabilities
from .embedded_player import NoEmbeddedPlayerTracker
from .surface import NoSurfaceHandler
from .window_buttons import StaticWindowButtons
from .window_configuration import NoWindowConfigurator
from .window_reveal import NoWindowRevealer
from .window_state import QtWindowStateHandler

if TYPE_CHECKING:
    from .capabilities import PlatformCapabilities
    from .embedded_player import EmbeddedPlayerTracker
    from .linux import WindowButtonDetector
    from .surface import SurfaceHandler
    from .window_buttons import WindowButtonSource
    from .window_configuration import WindowConfigurator
    from .window_reveal import WindowRevealer
    from .window_state import WindowStateHandler

logger = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class PlatformBackend:
    capabilities: PlatformCapabilities
    window_state: WindowStateHandler
    surface: SurfaceHandler
    window_configuration: WindowConfigurator
    window_reveal: WindowRevealer
    embedded_player: EmbeddedPlayerTracker
    window_buttons: WindowButtonSource


def select_platform_backend() -> PlatformBackend:
    match sys.platform:
        case "win32":
            backend = _create_windows_backend()
            logger.info("Using Windows platform backend")
            return backend
        case "linux":
            from .linux import is_tiling_desktop

            if is_tiling_desktop():
                backend = _create_linux_tiling_backend()
                logger.info("Using Linux tiling desktop platform backend")
                return backend

            backend = _create_linux_desktop_backend()
            logger.info("Using Linux desktop platform backend")
            return backend
        case _:
            msg = f"Unsupported platform for window integration: {sys.platform}"
            raise NotImplementedError(msg)


def _create_windows_backend() -> PlatformBackend:
    from .windows import WindowRevealFilter, WindowsFrameIntegration, WindowsWindowStateHandler

    frame = WindowsFrameIntegration()

    return PlatformBackend(
        capabilities=windows_capabilities(),
        window_state=WindowsWindowStateHandler(),
        surface=NoSurfaceHandler(),
        window_configuration=frame,
        window_reveal=WindowRevealFilter(),
        embedded_player=frame,
        window_buttons=StaticWindowButtons(),
    )


def _create_linux_desktop_backend() -> PlatformBackend:
    from .linux import SurfaceController

    # The margin must exceed the widest shadow blur plus spread, otherwise the
    # soft edge clips at the surface boundary.
    surface = SurfaceController(drop_shadow_margin=25)

    return PlatformBackend(
        capabilities=linux_desktop_capabilities(),
        window_state=QtWindowStateHandler(),
        surface=surface,
        window_configuration=surface,
        window_reveal=NoWindowRevealer(),
        embedded_player=NoEmbeddedPlayerTracker(),
        window_buttons=_create_linux_window_button_detector(),
    )


def _create_linux_tiling_backend() -> PlatformBackend:
    return PlatformBackend(
        capabilities=linux_tiling_capabilities(),
        window_state=QtWindowStateHandler(),
        surface=NoSurfaceHandler(),
        window_configuration=NoWindowConfigurator(),
        window_reveal=NoWindowRevealer(),
        embedded_player=NoEmbeddedPlayerTracker(),
        window_buttons=_create_linux_window_button_detector(),
    )


def _create_linux_window_button_detector() -> WindowButtonDetector:
    from .linux import WindowButtonDetector

    detector = WindowButtonDetector()
    detector.detect()
    return detector
