# SPDX-FileCopyrightText: zhiyiYo
# SPDX-FileCopyrightText: Virace
# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from .backend import PlatformBackend as PlatformBackend
from .capabilities import PlatformCapabilities as PlatformCapabilities
from .capabilities import linux_desktop_capabilities as linux_desktop_capabilities
from .capabilities import linux_tiling_capabilities as linux_tiling_capabilities
from .capabilities import windows_capabilities as windows_capabilities
from .embedded_player import NoEmbeddedPlayerTracker as NoEmbeddedPlayerTracker
from .main_window import MainWindowService as MainWindowService
from .native_frame import AppBarEdge as AppBarEdge
from .native_frame import ClientRect as ClientRect
from .native_frame import MonitorGeometry as MonitorGeometry
from .native_frame import MonitorRect as MonitorRect
from .native_frame import ProposedRect as ProposedRect
from .native_frame import WindowRect as WindowRect
from .native_frame import WorkArea as WorkArea
from .native_frame import handle_non_client_calculate_size as handle_non_client_calculate_size
from .native_frame import handle_non_client_hit_test as handle_non_client_hit_test
from .native_frame import overhangs as overhangs
from .native_frame import read_hit_test_point as read_hit_test_point
from .native_frame import reserve_auto_hide_taskbar_strip as reserve_auto_hide_taskbar_strip
from .platform import PlatformService as PlatformService
from .surface import NoSurfaceHandler as NoSurfaceHandler
from .surface import SurfaceHandler as SurfaceHandler
from .window_buttons import StaticWindowButtons as StaticWindowButtons
from .window_buttons import WindowButtonPreference as WindowButtonPreference
from .window_configuration import NoWindowConfigurator as NoWindowConfigurator
from .window_reveal import NoWindowRevealer as NoWindowRevealer
from .window_state import QtWindowStateHandler as QtWindowStateHandler
from .window_state import WindowStateSnapshot as WindowStateSnapshot
