# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING

from PySide6.QtCore import Qt

from mpvqc.window.services.fullscreen_session import (
    EnterFromMaximized,
    EnterFromNormal,
    EnterUnavailable,
    FullscreenSessionAbsent,
    FullscreenSessionEntering,
    FullscreenSessionRunning,
    KeepSession,
    NothingToLeave,
    RestoreMaximized,
    RestorePlacement,
    RetireAndRepinSession,
    RetireSession,
    decide_session_verdict,
    decide_window_state_read,
    plan_fullscreen_entry,
    plan_fullscreen_exit,
)

from .native import (
    get_window_placement,
    mark_fullscreen_window,
    maximize_window,
    minimize_window,
    refresh_window_frame,
    set_outer_window_rect,
    set_window_border_visible,
    set_window_corners_rounded,
    set_window_placement,
    set_window_transitions_enabled,
    strip_maximize_style,
)
from .probes import WindowsWindowStateProbe

if TYPE_CHECKING:
    from collections.abc import Generator

    from PySide6.QtGui import QWindow

    from mpvqc.window.services.fullscreen_session import (
        FullscreenRect,
        FullscreenSession,
        SessionVerdict,
    )
    from mpvqc.window.services.native_frame import Rect
    from mpvqc.window.services.window_placement import WindowPlacement
    from mpvqc.window.services.window_state import WindowStateSnapshot


class WindowsWindowStateHandler:
    """Assumes a single top-level window: one fullscreen session at a time,
    always for the same window."""

    def __init__(self) -> None:
        self._session: FullscreenSession = FullscreenSessionAbsent()

    def minimize(self, window: QWindow) -> None:
        # Qt does not keep WPF_RESTORETOMAXIMIZED (flag to restore a minimized window to maximized)
        # We need it, so we go native here.
        minimize_window(window.winId())

    def maximize(self, window: QWindow) -> None:
        window.setWindowStates(Qt.WindowState.WindowMaximized)

    def show_normal(self, window: QWindow) -> None:
        window.setWindowStates(Qt.WindowState.WindowNoState)

    def enter_fullscreen(self, window: QWindow) -> None:
        hwnd = window.winId()
        probe = WindowsWindowStateProbe(window)

        self._retire_if_abandoned(window, decide_session_verdict(self._session, probe))

        match plan_fullscreen_entry(self._session, probe):
            case EnterUnavailable():
                return
            case EnterFromNormal(placement=placement, rect=rect):
                self._enter_from_normal(hwnd, placement, rect)
            case EnterFromMaximized(placement=placement, rect=rect):
                self._enter_from_maximized(hwnd, placement, rect)

    def exit_fullscreen(self, window: QWindow) -> None:
        match plan_fullscreen_exit(self._session):
            case NothingToLeave():
                return
            case RestoreMaximized(placement=placement):
                self._leave_to_maximized(window.winId(), placement)
            case RestorePlacement(placement=placement):
                self._leave_to_placement(window.winId(), placement)

    def read_state(self, window: QWindow) -> WindowStateSnapshot:
        snapshot, verdict = decide_window_state_read(
            self._session,
            window.windowStates(),
            WindowsWindowStateProbe(window),
        )
        self._retire_if_abandoned(window, verdict)
        return snapshot

    def _retire_if_abandoned(self, window: QWindow, verdict: SessionVerdict) -> None:
        match verdict:
            case KeepSession():
                pass
            case RetireSession():
                self._retire(window.winId())
            case RetireAndRepinSession(normal_rect=normal_rect):
                hwnd = window.winId()
                self._retire(hwnd)
                _repin_normal_geometry(hwnd, normal_rect)

    def _retire(self, hwnd: int) -> None:
        self._session = FullscreenSessionAbsent()
        _restore_frame_chrome(hwnd)

    def _enter_from_normal(self, hwnd: int, placement: WindowPlacement, rect: FullscreenRect) -> None:
        with self._session_entering(placement):
            _strip_frame_chrome(hwnd)
            set_outer_window_rect(hwnd, rect)
            mark_fullscreen_window(hwnd, fullscreen=True)

    def _enter_from_maximized(self, hwnd: int, placement: WindowPlacement, rect: FullscreenRect) -> None:
        with self._session_entering(placement):
            _strip_frame_chrome(hwnd)
            with _transitions_suspended(hwnd):
                strip_maximize_style(hwnd)
                set_outer_window_rect(hwnd, rect)
            mark_fullscreen_window(hwnd, fullscreen=True)

    def _leave_to_maximized(self, hwnd: int, placement: WindowPlacement) -> None:
        self._session = FullscreenSessionAbsent()
        _restore_frame_chrome(hwnd)
        with _transitions_suspended(hwnd):
            maximize_window(hwnd)
        _repin_normal_geometry(hwnd, placement.normal_rect)
        refresh_window_frame(hwnd)

    def _leave_to_placement(self, hwnd: int, placement: WindowPlacement) -> None:
        self._session = FullscreenSessionAbsent()
        _restore_frame_chrome(hwnd)
        set_window_placement(hwnd, placement)
        refresh_window_frame(hwnd)

    @contextmanager
    def _session_entering(self, placement: WindowPlacement) -> Generator[None]:
        self._session = FullscreenSessionEntering(placement=placement)
        try:
            yield
        finally:
            self._session = FullscreenSessionRunning(placement=placement)


def _strip_frame_chrome(hwnd: int) -> None:
    set_window_corners_rounded(hwnd, rounded=False)
    set_window_border_visible(hwnd, visible=False)


def _restore_frame_chrome(hwnd: int) -> None:
    mark_fullscreen_window(hwnd, fullscreen=False)
    set_window_corners_rounded(hwnd, rounded=True)
    set_window_border_visible(hwnd, visible=True)


def _repin_normal_geometry(hwnd: int, normal_rect: Rect) -> None:
    placement = get_window_placement(hwnd)
    if placement is not None:
        set_window_placement(hwnd, placement._replace(normal_rect=normal_rect))


@contextmanager
def _transitions_suspended(hwnd: int) -> Generator[None]:
    set_window_transitions_enabled(hwnd, enabled=False)
    try:
        yield
    finally:
        set_window_transitions_enabled(hwnd, enabled=True)
