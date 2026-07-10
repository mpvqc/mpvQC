# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .content_margins import ContentMarginsApplier
    from .embedded_player import EmbeddedPlayerTracker
    from .fullscreen import FullscreenHandler
    from .window_buttons import WindowButtonSource
    from .window_configuration import WindowConfigurator

logger = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class PlatformBackend:
    root_qml_url: str
    draws_own_shadow: bool
    owns_window_geometry: bool

    fullscreen: FullscreenHandler
    window_configuration: WindowConfigurator
    embedded_player: EmbeddedPlayerTracker
    content_margins: ContentMarginsApplier
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
    from .linux.backend import create_desktop_backend, create_window_manager_backend
    from .linux.tiling import is_tiling_window_manager

    if is_tiling_window_manager():
        backend = create_window_manager_backend()
        logger.info("Using Linux window manager platform backend")
        return backend

    backend = create_desktop_backend()
    logger.info("Using Linux desktop platform backend")
    return backend
