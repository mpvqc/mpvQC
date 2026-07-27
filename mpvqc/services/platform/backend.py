# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .embedded_player import EmbeddedPlayerTracker
    from .surface import SurfaceHandler
    from .window_buttons import WindowButtonSource
    from .window_configuration import WindowConfigurator
    from .window_reveal import WindowRevealer
    from .window_state import WindowStateHandler

logger = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class PlatformBackend:
    keeps_native_frame: bool
    """If True, the app keeps the native frame: the OS draws the border, drop shadow and rounded corners."""

    draws_drop_shadow: bool
    """If True, the app paints its own drop shadow into the surface beyond the window geometry."""

    window_state: WindowStateHandler
    surface: SurfaceHandler
    window_configuration: WindowConfigurator
    window_reveal: WindowRevealer
    embedded_player: EmbeddedPlayerTracker
    window_buttons: WindowButtonSource


def select_platform_backend() -> PlatformBackend:
    match sys.platform:
        case "win32":
            from .win.backend import create_windows_backend

            backend = create_windows_backend()
            logger.info("Using Windows platform backend")
            return backend
        case "linux":
            return _select_linux_backend()
        case _:
            msg = f"Unsupported platform for window integration: {sys.platform}"
            raise NotImplementedError(msg)


def _select_linux_backend() -> PlatformBackend:
    from .linux.backend import create_desktop_backend, create_tiling_backend
    from .linux.tiling import is_tiling_desktop

    if is_tiling_desktop():
        backend = create_tiling_backend()
        logger.info("Using Linux tiling desktop platform backend")
        return backend

    backend = create_desktop_backend()
    logger.info("Using Linux desktop platform backend")
    return backend
