# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import ast
from dataclasses import dataclass, field
from pathlib import Path
from typing import NamedTuple

import pytest
from PySide6.QtCore import Qt

from mpvqc.window.services import (
    EnterFromMaximized,
    EnterFromNormal,
    EnterUnavailable,
    FullscreenEntryPlan,
    FullscreenExitPlan,
    FullscreenRect,
    FullscreenSession,
    FullscreenSessionAbsent,
    FullscreenSessionEntering,
    FullscreenSessionRunning,
    KeepSession,
    MonitorRect,
    NativeMaximized,
    NativeMinimized,
    NativeNormal,
    NativeOverhangsMonitor,
    NativeWindowState,
    NothingToLeave,
    Rect,
    ResizeBorders,
    RestoreMaximized,
    RestorePlacement,
    RetireAndRepinSession,
    RetireSession,
    SessionVerdict,
    WindowPlacement,
    WindowStateSnapshot,
    classify_native_state,
    decide_session_verdict,
    decide_window_state_read,
    plan_fullscreen_entry,
    plan_fullscreen_exit,
)

DECISIONS = Path(__file__).resolve().parents[3] / "mpvqc" / "window" / "services" / "fullscreen_session.py"

SW_SHOWNORMAL = 1
SW_SHOWMAXIMIZED = 3

NORMAL_RECT: Rect = (100, 100, 900, 700)
OTHER_RECT: Rect = (200, 200, 800, 600)
MONITOR = MonitorRect((0, 0, 1920, 1080))
BORDERS = ResizeBorders(horizontal=8, vertical=4)
OVERHANG_RECT = FullscreenRect((-8, 0, 1928, 1084))


def placement(*, maximized: bool = False, normal_rect: Rect = NORMAL_RECT) -> WindowPlacement:
    return WindowPlacement(
        flags=0,
        show_cmd=SW_SHOWMAXIMIZED if maximized else SW_SHOWNORMAL,
        min_position=(-1, -1),
        max_position=(-1, -1),
        normal_rect=normal_rect,
    )


@dataclass
class RecordingWindowStateProbe:
    state: NativeWindowState = field(default_factory=NativeNormal)
    fresh_placement: WindowPlacement | None = field(default_factory=placement)
    restore_flag: bool = False
    monitor: MonitorRect | None = MONITOR
    asked: list[str] = field(default_factory=list)

    def native_state(self) -> NativeWindowState:
        self.asked.append("native_state")
        return self.state

    def placement(self) -> WindowPlacement | None:
        self.asked.append("placement")
        return self.fresh_placement

    def restores_to_maximized(self) -> bool:
        self.asked.append("restores_to_maximized")
        return self.restore_flag

    def monitor_rect(self) -> MonitorRect | None:
        self.asked.append("monitor_rect")
        return self.monitor

    def resize_borders(self) -> ResizeBorders:
        self.asked.append("resize_borders")
        return BORDERS


@dataclass
class RecordingNativeStateProbe:
    is_minimized: bool = False
    is_maximized: bool = False
    overhangs: bool = False
    asked: list[str] = field(default_factory=list)

    def minimized(self) -> bool:
        self.asked.append("minimized")
        return self.is_minimized

    def maximized(self) -> bool:
        self.asked.append("maximized")
        return self.is_maximized

    def overhangs_monitor(self) -> bool:
        self.asked.append("overhangs_monitor")
        return self.overhangs


class ClassifyCase(NamedTuple):
    name: str
    is_minimized: bool
    is_maximized: bool
    overhangs: bool
    expected: NativeWindowState
    expected_questions: list[str]


@pytest.mark.parametrize(
    "case",
    [
        ClassifyCase(
            name="a_window_within_its_monitor_is_normal",
            is_minimized=False,
            is_maximized=False,
            overhangs=False,
            expected=NativeNormal(),
            expected_questions=["minimized", "maximized", "overhangs_monitor"],
        ),
        ClassifyCase(
            name="a_window_larger_than_its_monitor_overhangs",
            is_minimized=False,
            is_maximized=False,
            overhangs=True,
            expected=NativeOverhangsMonitor(),
            expected_questions=["minimized", "maximized", "overhangs_monitor"],
        ),
        ClassifyCase(
            name="a_maximized_window_is_never_read_as_overhanging",
            is_minimized=False,
            is_maximized=True,
            overhangs=True,
            expected=NativeMaximized(),
            expected_questions=["minimized", "maximized"],
        ),
        ClassifyCase(
            name="a_minimized_window_is_never_read_as_overhanging",
            is_minimized=True,
            is_maximized=False,
            overhangs=True,
            expected=NativeMinimized(),
            expected_questions=["minimized"],
        ),
        ClassifyCase(
            name="a_minimized_window_is_never_read_as_maximized",
            is_minimized=True,
            is_maximized=True,
            overhangs=False,
            expected=NativeMinimized(),
            expected_questions=["minimized"],
        ),
    ],
    ids=lambda case: case.name,
)
def test_classify_native_state(case: ClassifyCase):
    probe = RecordingNativeStateProbe(
        is_minimized=case.is_minimized,
        is_maximized=case.is_maximized,
        overhangs=case.overhangs,
    )

    assert classify_native_state(probe) == case.expected
    assert probe.asked == case.expected_questions


class EnteringReadCase(NamedTuple):
    name: str
    entered_maximized: bool


@pytest.mark.parametrize(
    "case",
    [
        EnteringReadCase(name="entered_from_maximized", entered_maximized=True),
        EnteringReadCase(name="entered_from_normal", entered_maximized=False),
    ],
    ids=lambda case: case.name,
)
def test_read_while_entering_answers_from_the_session(case: EnteringReadCase):
    probe = RecordingWindowStateProbe()
    session = FullscreenSessionEntering(placement=placement(maximized=case.entered_maximized))

    snapshot, verdict = decide_window_state_read(session, Qt.WindowState.WindowNoState, probe)

    assert snapshot == WindowStateSnapshot(is_fullscreen=True, is_maximized=case.entered_maximized)
    assert verdict == KeepSession()
    assert probe.asked == []


class NoSessionCase(NamedTuple):
    name: str
    qt_states: Qt.WindowState
    restore_flag: bool
    expected_maximized: bool
    expected_questions: list[str]


@pytest.mark.parametrize(
    "case",
    [
        NoSessionCase(
            name="a_plain_window_asks_the_probe_nothing",
            qt_states=Qt.WindowState.WindowNoState,
            restore_flag=False,
            expected_maximized=False,
            expected_questions=[],
        ),
        NoSessionCase(
            name="answers_from_the_qt_states",
            qt_states=Qt.WindowState.WindowMaximized,
            restore_flag=False,
            expected_maximized=True,
            expected_questions=[],
        ),
        NoSessionCase(
            name="minimized_from_maximized_answers_from_the_flag_not_the_bit",
            qt_states=Qt.WindowState.WindowMaximized | Qt.WindowState.WindowMinimized,
            restore_flag=False,
            expected_maximized=False,
            expected_questions=["restores_to_maximized"],
        ),
        NoSessionCase(
            name="minimized_answers_from_the_restore_flag",
            qt_states=Qt.WindowState.WindowMinimized,
            restore_flag=True,
            expected_maximized=True,
            expected_questions=["restores_to_maximized"],
        ),
        NoSessionCase(
            name="minimized_from_normal",
            qt_states=Qt.WindowState.WindowMinimized,
            restore_flag=False,
            expected_maximized=False,
            expected_questions=["restores_to_maximized"],
        ),
    ],
    ids=lambda case: case.name,
)
def test_read_without_a_session(case: NoSessionCase):
    # Every probe question reaches the OS through the native window handle, so
    # a probe that was asked nothing is the guarantee the read created no
    # native window.
    probe = RecordingWindowStateProbe(restore_flag=case.restore_flag)

    snapshot, verdict = decide_window_state_read(FullscreenSessionAbsent(), case.qt_states, probe)

    assert snapshot == WindowStateSnapshot(is_fullscreen=False, is_maximized=case.expected_maximized)
    assert verdict == KeepSession()
    assert probe.asked == case.expected_questions


class RunningReadCase(NamedTuple):
    name: str
    entered_maximized: bool
    state: NativeWindowState
    expected: WindowStateSnapshot
    expected_verdict: SessionVerdict


@pytest.mark.parametrize(
    "case",
    [
        RunningReadCase(
            name="covering_the_monitor_stays_fullscreen",
            entered_maximized=True,
            state=NativeOverhangsMonitor(),
            expected=WindowStateSnapshot(is_fullscreen=True, is_maximized=True),
            expected_verdict=KeepSession(),
        ),
        RunningReadCase(
            name="a_session_from_a_normal_window_is_not_maximized",
            entered_maximized=False,
            state=NativeOverhangsMonitor(),
            expected=WindowStateSnapshot(is_fullscreen=True, is_maximized=False),
            expected_verdict=KeepSession(),
        ),
        RunningReadCase(
            name="minimized_keeps_the_session",
            entered_maximized=True,
            state=NativeMinimized(),
            expected=WindowStateSnapshot(is_fullscreen=True, is_maximized=True),
            expected_verdict=KeepSession(),
        ),
        RunningReadCase(
            name="restored_behind_the_apps_back_retires_without_repin",
            entered_maximized=True,
            state=NativeNormal(),
            expected=WindowStateSnapshot(is_fullscreen=False, is_maximized=False),
            expected_verdict=RetireSession(),
        ),
        RunningReadCase(
            name="maximized_behind_the_apps_back_retires_with_repin",
            entered_maximized=False,
            state=NativeMaximized(),
            expected=WindowStateSnapshot(is_fullscreen=False, is_maximized=True),
            expected_verdict=RetireAndRepinSession(normal_rect=NORMAL_RECT),
        ),
    ],
    ids=lambda case: case.name,
)
def test_read_with_a_running_session(case: RunningReadCase):
    session = FullscreenSessionRunning(placement=placement(maximized=case.entered_maximized))
    probe = RecordingWindowStateProbe(state=case.state)

    snapshot, verdict = decide_window_state_read(session, Qt.WindowState.WindowNoState, probe)

    assert snapshot == case.expected
    assert verdict == case.expected_verdict
    assert probe.asked == ["native_state"]


def test_a_running_session_outranks_the_qt_states():
    # Minimized while fullscreen: Qt's states and the native restore flag both
    # describe a window the session already answers for.
    session = FullscreenSessionRunning(placement=placement(maximized=False))
    probe = RecordingWindowStateProbe(state=NativeMinimized(), restore_flag=True)

    snapshot, _ = decide_window_state_read(session, Qt.WindowState.WindowMinimized, probe)

    assert snapshot == WindowStateSnapshot(is_fullscreen=True, is_maximized=False)
    assert probe.asked == ["native_state"]


class EntryCase(NamedTuple):
    name: str
    session: FullscreenSession
    state: NativeWindowState
    fresh_placement: WindowPlacement | None
    monitor: MonitorRect | None
    expected: FullscreenEntryPlan
    expected_questions: list[str]


@pytest.mark.parametrize(
    "case",
    [
        EntryCase(
            name="from_a_normal_window",
            session=FullscreenSessionAbsent(),
            state=NativeNormal(),
            fresh_placement=placement(),
            monitor=MONITOR,
            expected=EnterFromNormal(placement=placement(), rect=OVERHANG_RECT),
            expected_questions=["monitor_rect", "placement", "native_state", "resize_borders"],
        ),
        EntryCase(
            name="from_a_maximized_window",
            session=FullscreenSessionAbsent(),
            state=NativeMaximized(),
            fresh_placement=placement(maximized=True),
            monitor=MONITOR,
            expected=EnterFromMaximized(placement=placement(maximized=True), rect=OVERHANG_RECT),
            expected_questions=["monitor_rect", "placement", "native_state", "resize_borders"],
        ),
        EntryCase(
            name="a_running_session_keeps_its_first_placement",
            session=FullscreenSessionRunning(placement=placement(normal_rect=OTHER_RECT)),
            state=NativeOverhangsMonitor(),
            fresh_placement=placement(),
            monitor=MONITOR,
            expected=EnterFromNormal(placement=placement(normal_rect=OTHER_RECT), rect=OVERHANG_RECT),
            expected_questions=["monitor_rect", "native_state", "resize_borders"],
        ),
        EntryCase(
            name="a_minimized_window_shows_nothing_to_make_fullscreen",
            session=FullscreenSessionAbsent(),
            state=NativeMinimized(),
            fresh_placement=placement(),
            monitor=MONITOR,
            expected=EnterUnavailable(),
            expected_questions=["monitor_rect", "placement", "native_state"],
        ),
        EntryCase(
            name="without_a_monitor_there_is_nowhere_to_go",
            session=FullscreenSessionAbsent(),
            state=NativeNormal(),
            fresh_placement=placement(),
            monitor=None,
            expected=EnterUnavailable(),
            expected_questions=["monitor_rect"],
        ),
        EntryCase(
            name="without_a_placement_there_is_no_way_back",
            session=FullscreenSessionAbsent(),
            state=NativeNormal(),
            fresh_placement=None,
            monitor=MONITOR,
            expected=EnterUnavailable(),
            expected_questions=["monitor_rect", "placement"],
        ),
    ],
    ids=lambda case: case.name,
)
def test_plan_fullscreen_entry(case: EntryCase):
    probe = RecordingWindowStateProbe(
        state=case.state,
        fresh_placement=case.fresh_placement,
        monitor=case.monitor,
    )

    assert plan_fullscreen_entry(case.session, probe) == case.expected
    # The early returns are the point: a plan that cannot be made must not pay
    # for the questions it no longer needs.
    assert probe.asked == case.expected_questions


class VerdictCase(NamedTuple):
    name: str
    session: FullscreenSession


@pytest.mark.parametrize(
    "case",
    [
        VerdictCase(name="no_session", session=FullscreenSessionAbsent()),
        VerdictCase(name="still_entering", session=FullscreenSessionEntering(placement=placement())),
    ],
    ids=lambda case: case.name,
)
def test_only_a_running_session_can_be_retired(case: VerdictCase):
    # Entering is the reentrancy guard: enter_fullscreen moves the window, which
    # re-enters the read on a window that looks abandoned. Retiring there would
    # discard the session being built.
    probe = RecordingWindowStateProbe(state=NativeNormal())

    assert decide_session_verdict(case.session, probe) == KeepSession()
    assert probe.asked == []


class ExitCase(NamedTuple):
    name: str
    session: FullscreenSession
    expected: FullscreenExitPlan


@pytest.mark.parametrize(
    "case",
    [
        ExitCase(
            name="no_session",
            session=FullscreenSessionAbsent(),
            expected=NothingToLeave(),
        ),
        ExitCase(
            name="still_entering",
            session=FullscreenSessionEntering(placement=placement()),
            expected=NothingToLeave(),
        ),
        ExitCase(
            name="entered_from_normal",
            session=FullscreenSessionRunning(placement=placement()),
            expected=RestorePlacement(placement=placement()),
        ),
        ExitCase(
            name="entered_from_maximized",
            session=FullscreenSessionRunning(placement=placement(maximized=True)),
            expected=RestoreMaximized(placement=placement(maximized=True)),
        ),
    ],
    ids=lambda case: case.name,
)
def test_plan_fullscreen_exit(case: ExitCase):
    assert plan_fullscreen_exit(case.session) == case.expected


def test_the_decisions_reach_nothing_platform_specific():
    # A module-level reach would already break this file's own import on Linux.
    # The scan is what catches one hidden inside a function, where it would run
    # on Windows and raise everywhere else.
    tree = ast.parse(DECISIONS.read_text(encoding="utf-8"))
    targets = [
        alias.name if isinstance(node, ast.Import) else node.module or ""
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    ]

    assert targets, "the scan read no imports; it would pass on any module"
    assert not [target for target in targets if "ctypes" in target or "windows" in target.split(".")]
