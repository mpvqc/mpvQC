# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from .backend import PlatformBackend as PlatformBackend
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
from .window_configuration import NoWindowConfigurator as NoWindowConfigurator
from .window_reveal import NoWindowRevealer as NoWindowRevealer
from .window_state import QtWindowStateHandler as QtWindowStateHandler
from .window_state import WindowStateSnapshot as WindowStateSnapshot
