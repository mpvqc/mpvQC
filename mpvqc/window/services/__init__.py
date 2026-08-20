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
from .fullscreen_session import EnterFromMaximized as EnterFromMaximized
from .fullscreen_session import EnterFromNormal as EnterFromNormal
from .fullscreen_session import EnterUnavailable as EnterUnavailable
from .fullscreen_session import FullscreenEntryPlan as FullscreenEntryPlan
from .fullscreen_session import FullscreenExitPlan as FullscreenExitPlan
from .fullscreen_session import FullscreenRect as FullscreenRect
from .fullscreen_session import FullscreenSession as FullscreenSession
from .fullscreen_session import FullscreenSessionAbsent as FullscreenSessionAbsent
from .fullscreen_session import FullscreenSessionEntering as FullscreenSessionEntering
from .fullscreen_session import FullscreenSessionRunning as FullscreenSessionRunning
from .fullscreen_session import KeepSession as KeepSession
from .fullscreen_session import NativeMaximized as NativeMaximized
from .fullscreen_session import NativeMinimized as NativeMinimized
from .fullscreen_session import NativeNormal as NativeNormal
from .fullscreen_session import NativeOverhangsMonitor as NativeOverhangsMonitor
from .fullscreen_session import NativeStateProbe as NativeStateProbe
from .fullscreen_session import NativeWindowState as NativeWindowState
from .fullscreen_session import NothingToLeave as NothingToLeave
from .fullscreen_session import ResizeBorders as ResizeBorders
from .fullscreen_session import RestoreMaximized as RestoreMaximized
from .fullscreen_session import RestorePlacement as RestorePlacement
from .fullscreen_session import RetireAndRepinSession as RetireAndRepinSession
from .fullscreen_session import RetireSession as RetireSession
from .fullscreen_session import SessionVerdict as SessionVerdict
from .fullscreen_session import WindowStateProbe as WindowStateProbe
from .fullscreen_session import classify_native_state as classify_native_state
from .fullscreen_session import decide_session_verdict as decide_session_verdict
from .fullscreen_session import decide_window_state_read as decide_window_state_read
from .fullscreen_session import plan_fullscreen_entry as plan_fullscreen_entry
from .fullscreen_session import plan_fullscreen_exit as plan_fullscreen_exit
from .main_window import MainWindowService as MainWindowService
from .native_frame import AppBarEdge as AppBarEdge
from .native_frame import ClientRect as ClientRect
from .native_frame import MonitorGeometry as MonitorGeometry
from .native_frame import MonitorRect as MonitorRect
from .native_frame import ProposedRect as ProposedRect
from .native_frame import Rect as Rect
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
from .window_placement import WindowPlacement as WindowPlacement
from .window_reveal import NoWindowRevealer as NoWindowRevealer
from .window_state import QtWindowStateHandler as QtWindowStateHandler
from .window_state import WindowStateSnapshot as WindowStateSnapshot
