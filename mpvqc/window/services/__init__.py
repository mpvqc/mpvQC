# SPDX-FileCopyrightText: zhiyiYo
# SPDX-FileCopyrightText: Virace
# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from .backend import PlatformBackend as PlatformBackend
from .backend import select_platform_backend as select_platform_backend
from .capabilities import PlatformCapabilities as PlatformCapabilities
from .capabilities import linux_desktop_capabilities as linux_desktop_capabilities
from .capabilities import linux_tiling_capabilities as linux_tiling_capabilities
from .capabilities import windows_capabilities as windows_capabilities
from .embedded_player import NoEmbeddedPlayerTracker as NoEmbeddedPlayerTracker
from .main_window import MainWindowService as MainWindowService
from .platform import PlatformService as PlatformService
from .surface import NoSurfaceHandler as NoSurfaceHandler
from .surface import SurfaceHandler as SurfaceHandler
from .window_buttons import StaticWindowButtons as StaticWindowButtons
from .window_buttons import WindowButtonPreference as WindowButtonPreference
from .window_configuration import NoWindowConfigurator as NoWindowConfigurator
from .window_reveal import NoWindowRevealer as NoWindowRevealer
from .window_state import QtWindowStateHandler as QtWindowStateHandler
from .window_state import WindowStateSnapshot as WindowStateSnapshot
from .windows_decisions import AppBarEdge as AppBarEdge
from .windows_decisions import ClientRect as ClientRect
from .windows_decisions import EnterFromMaximized as EnterFromMaximized
from .windows_decisions import EnterFromNormal as EnterFromNormal
from .windows_decisions import EnterUnavailable as EnterUnavailable
from .windows_decisions import FullscreenEntryPlan as FullscreenEntryPlan
from .windows_decisions import FullscreenExitPlan as FullscreenExitPlan
from .windows_decisions import FullscreenRect as FullscreenRect
from .windows_decisions import FullscreenSession as FullscreenSession
from .windows_decisions import FullscreenSessionAbsent as FullscreenSessionAbsent
from .windows_decisions import FullscreenSessionEntering as FullscreenSessionEntering
from .windows_decisions import FullscreenSessionRunning as FullscreenSessionRunning
from .windows_decisions import KeepSession as KeepSession
from .windows_decisions import MonitorGeometry as MonitorGeometry
from .windows_decisions import MonitorRect as MonitorRect
from .windows_decisions import NativeMaximized as NativeMaximized
from .windows_decisions import NativeMinimized as NativeMinimized
from .windows_decisions import NativeNormal as NativeNormal
from .windows_decisions import NativeOverhangsMonitor as NativeOverhangsMonitor
from .windows_decisions import NativeStateProbe as NativeStateProbe
from .windows_decisions import NativeWindowState as NativeWindowState
from .windows_decisions import NothingToLeave as NothingToLeave
from .windows_decisions import ProposedRect as ProposedRect
from .windows_decisions import Rect as Rect
from .windows_decisions import ResizeBorders as ResizeBorders
from .windows_decisions import RestoreMaximized as RestoreMaximized
from .windows_decisions import RestorePlacement as RestorePlacement
from .windows_decisions import RetireAndRepinSession as RetireAndRepinSession
from .windows_decisions import RetireSession as RetireSession
from .windows_decisions import SessionVerdict as SessionVerdict
from .windows_decisions import WindowPlacement as WindowPlacement
from .windows_decisions import WindowRect as WindowRect
from .windows_decisions import WindowStateProbe as WindowStateProbe
from .windows_decisions import WorkArea as WorkArea
from .windows_decisions import classify_native_state as classify_native_state
from .windows_decisions import decide_session_verdict as decide_session_verdict
from .windows_decisions import decide_window_state_read as decide_window_state_read
from .windows_decisions import handle_non_client_calculate_size as handle_non_client_calculate_size
from .windows_decisions import handle_non_client_hit_test as handle_non_client_hit_test
from .windows_decisions import overhangs as overhangs
from .windows_decisions import plan_fullscreen_entry as plan_fullscreen_entry
from .windows_decisions import plan_fullscreen_exit as plan_fullscreen_exit
from .windows_decisions import read_hit_test_point as read_hit_test_point
from .windows_decisions import reserve_auto_hide_taskbar_strip as reserve_auto_hide_taskbar_strip
