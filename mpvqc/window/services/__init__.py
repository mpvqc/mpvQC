# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from .backend import PlatformBackend as PlatformBackend
from .backend import select_platform_backend as select_platform_backend
from .capabilities import PlatformCapabilities as PlatformCapabilities
from .capabilities import linux_desktop_capabilities as linux_desktop_capabilities
from .capabilities import linux_tiling_capabilities as linux_tiling_capabilities
from .capabilities import windows_capabilities as windows_capabilities
from .embedded_player import EmbeddedPlayerTracker as EmbeddedPlayerTracker
from .embedded_player import NoEmbeddedPlayerTracker as NoEmbeddedPlayerTracker
from .main_window import MainWindowInputs as MainWindowInputs
from .main_window import MainWindowProps as MainWindowProps
from .main_window import MainWindowService as MainWindowService
from .main_window import derive_main_window_props as derive_main_window_props
from .platform import PlatformService as PlatformService
from .surface import NoSurfaceHandler as NoSurfaceHandler
from .surface import SurfaceHandler as SurfaceHandler
from .window_buttons import StaticWindowButtons as StaticWindowButtons
from .window_buttons import WindowButtonPreference as WindowButtonPreference
from .window_buttons import WindowButtonSource as WindowButtonSource
from .window_configuration import NoWindowConfigurator as NoWindowConfigurator
from .window_configuration import WindowConfigurator as WindowConfigurator
from .window_reveal import NoWindowRevealer as NoWindowRevealer
from .window_reveal import WindowRevealer as WindowRevealer
from .window_state import QtWindowStateHandler as QtWindowStateHandler
from .window_state import WindowStateHandler as WindowStateHandler
from .window_state import WindowStateSnapshot as WindowStateSnapshot
