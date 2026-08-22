# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, NamedTuple, NewType, Protocol

from PySide6.QtCore import Qt

from mpvqc.window.services.window_state import WindowStateSnapshot

from .frame_geometry import Rect

if TYPE_CHECKING:
    from .frame_geometry import MonitorRect
    from .window_placement import WindowPlacement

FullscreenRect = NewType("FullscreenRect", Rect)


class ResizeBorders(NamedTuple):
    horizontal: int
    vertical: int


@dataclass(frozen=True)
class NativeMinimized:
    pass


@dataclass(frozen=True)
class NativeMaximized:
    pass


@dataclass(frozen=True)
class NativeOverhangsMonitor:
    pass


@dataclass(frozen=True)
class NativeNormal:
    pass


type NativeWindowState = NativeMinimized | NativeMaximized | NativeOverhangsMonitor | NativeNormal


class NativeStateProbe(Protocol):
    def minimized(self) -> bool: ...

    def maximized(self) -> bool: ...

    def overhangs_monitor(self) -> bool: ...


def classify_native_state(probe: NativeStateProbe) -> NativeWindowState:
    if probe.minimized():
        return NativeMinimized()
    if probe.maximized():
        return NativeMaximized()
    if probe.overhangs_monitor():
        return NativeOverhangsMonitor()
    return NativeNormal()


@dataclass(frozen=True)
class FullscreenSessionAbsent:
    pass


@dataclass(frozen=True)
class FullscreenSessionEntering:
    placement: WindowPlacement


@dataclass(frozen=True)
class FullscreenSessionRunning:
    placement: WindowPlacement


type FullscreenSession = FullscreenSessionAbsent | FullscreenSessionEntering | FullscreenSessionRunning


@dataclass(frozen=True)
class KeepSession:
    pass


@dataclass(frozen=True)
class RetireSession:
    pass


@dataclass(frozen=True)
class RetireAndRepinSession:
    normal_rect: Rect


type SessionVerdict = KeepSession | RetireSession | RetireAndRepinSession


@dataclass(frozen=True)
class EnterUnavailable:
    pass


@dataclass(frozen=True)
class EnterFromNormal:
    placement: WindowPlacement
    rect: FullscreenRect


@dataclass(frozen=True)
class EnterFromMaximized:
    placement: WindowPlacement
    rect: FullscreenRect


type FullscreenEntryPlan = EnterUnavailable | EnterFromNormal | EnterFromMaximized


@dataclass(frozen=True)
class NothingToLeave:
    pass


@dataclass(frozen=True)
class RestoreMaximized:
    placement: WindowPlacement


@dataclass(frozen=True)
class RestorePlacement:
    placement: WindowPlacement


type FullscreenExitPlan = NothingToLeave | RestoreMaximized | RestorePlacement


class WindowStateProbe(Protocol):
    def native_state(self) -> NativeWindowState: ...

    def placement(self) -> WindowPlacement | None: ...

    def restores_to_maximized(self) -> bool: ...

    def monitor_rect(self) -> MonitorRect | None: ...

    def resize_borders(self) -> ResizeBorders: ...


def decide_session_verdict(session: FullscreenSession, probe: WindowStateProbe) -> SessionVerdict:
    match session:
        case FullscreenSessionAbsent() | FullscreenSessionEntering():
            return KeepSession()
        case FullscreenSessionRunning(placement=placement):
            return _verdict_for(probe.native_state(), placement)


def _verdict_for(state: NativeWindowState, placement: WindowPlacement) -> SessionVerdict:
    match state:
        case NativeMinimized() | NativeOverhangsMonitor():
            return KeepSession()
        case NativeMaximized():
            return RetireAndRepinSession(normal_rect=placement.normal_rect)
        case NativeNormal():
            return RetireSession()


def decide_window_state_read(
    session: FullscreenSession,
    qt_states: Qt.WindowState,
    probe: WindowStateProbe,
) -> tuple[WindowStateSnapshot, SessionVerdict]:
    match session:
        case FullscreenSessionAbsent():
            return WindowStateSnapshot(False, _maximized_without_session(qt_states, probe)), KeepSession()
        # A fullscreen window carries no WS_MAXIMIZE, so nothing native still
        # records how the window stood before; the session's placement is that
        # record.
        case FullscreenSessionEntering(placement=placement):
            return WindowStateSnapshot(True, placement.shows_maximized), KeepSession()
        case FullscreenSessionRunning(placement=placement):
            verdict = decide_session_verdict(session, probe)
            match verdict:
                case KeepSession():
                    return WindowStateSnapshot(True, placement.shows_maximized), verdict
                case RetireSession():
                    return WindowStateSnapshot(False, False), verdict
                case RetireAndRepinSession():
                    return WindowStateSnapshot(False, True), verdict


def plan_fullscreen_entry(session: FullscreenSession, probe: WindowStateProbe) -> FullscreenEntryPlan:
    monitor_rect = probe.monitor_rect()
    if monitor_rect is None:
        return EnterUnavailable()

    placement = _placement_to_return_to(session, probe)
    if placement is None:
        return EnterUnavailable()

    match probe.native_state():
        case NativeMinimized():
            return EnterUnavailable()
        case NativeMaximized():
            return EnterFromMaximized(placement=placement, rect=_entry_rect(monitor_rect, probe))
        case _:
            return EnterFromNormal(placement=placement, rect=_entry_rect(monitor_rect, probe))


def plan_fullscreen_exit(session: FullscreenSession) -> FullscreenExitPlan:
    match session:
        case FullscreenSessionAbsent() | FullscreenSessionEntering():
            return NothingToLeave()
        case FullscreenSessionRunning(placement=placement) if placement.shows_maximized:
            return RestoreMaximized(placement=placement)
        case FullscreenSessionRunning(placement=placement):
            return RestorePlacement(placement=placement)


def _placement_to_return_to(session: FullscreenSession, probe: WindowStateProbe) -> WindowPlacement | None:
    match session:
        case FullscreenSessionRunning(placement=placement):
            return placement
        case _:
            return probe.placement()


def _entry_rect(monitor_rect: MonitorRect, probe: WindowStateProbe) -> FullscreenRect:
    return _fullscreen_rect(monitor_rect, probe.resize_borders())


def _fullscreen_rect(monitor_rect: MonitorRect, borders: ResizeBorders) -> FullscreenRect:
    # Qt subtracts the frame border again, so an overhang this size yields a
    # scene of exactly the monitor rect. ADR 0004 has why the overhang is kept.
    left, top, right, bottom = monitor_rect
    return FullscreenRect((left - borders.horizontal, top, right + borders.horizontal, bottom + borders.vertical))


def _maximized_without_session(qt_states: Qt.WindowState, probe: WindowStateProbe) -> bool:
    # While minimized, Qt's bookkeeping can lose the Maximized bit; the native
    # restore flag remembers the restore target.
    if qt_states & Qt.WindowState.WindowMinimized:
        return probe.restores_to_maximized()
    # Qt's states answer without reaching the probe, so this read cannot create
    # the native window; WindowsWindowStateProbe says what that would cost.
    return bool(qt_states & Qt.WindowState.WindowMaximized)
