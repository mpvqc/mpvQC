# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TYPE_CHECKING, NamedTuple

import pytest
from PySide6.QtCore import Qt

from mpvqc.window.services import NoSurfaceHandler
from mpvqc.window.services.linux import SurfaceController

if TYPE_CHECKING:
    from mpvqc.window.services import SurfaceHandler

SURFACE = "mpvqc.window.services.linux.surface"

NO_STATE = Qt.WindowState.WindowNoState
MINIMIZED = Qt.WindowState.WindowMinimized
MAXIMIZED = Qt.WindowState.WindowMaximized
FULLSCREEN = Qt.WindowState.WindowFullScreen


class DropShadowMarginTestCase(NamedTuple):
    name: str
    drop_shadow_margin: int
    states: Qt.WindowState
    expected: int


@pytest.mark.parametrize(
    "case",
    [
        DropShadowMarginTestCase(
            "zero_margin_reads_zero",
            drop_shadow_margin=0,
            states=NO_STATE,
            expected=0,
        ),
        DropShadowMarginTestCase(
            "normal_keeps_margin",
            drop_shadow_margin=88,
            states=NO_STATE,
            expected=88,
        ),
        DropShadowMarginTestCase(
            "maximized_collapses_margin",
            drop_shadow_margin=88,
            states=MAXIMIZED,
            expected=0,
        ),
        DropShadowMarginTestCase(
            "fullscreen_collapses_margin",
            drop_shadow_margin=88,
            states=FULLSCREEN,
            expected=0,
        ),
        DropShadowMarginTestCase(
            "minimized_from_maximized_stays_collapsed",
            drop_shadow_margin=88,
            states=MAXIMIZED | MINIMIZED,
            expected=0,
        ),
        DropShadowMarginTestCase(
            "minimized_from_normal_keeps_margin",
            drop_shadow_margin=88,
            states=MINIMIZED,
            expected=88,
        ),
    ],
    ids=lambda case: case.name,
)
def test_drop_shadow_margin(case: DropShadowMarginTestCase, make_recording_window):
    window = make_recording_window(case.states)
    handler: SurfaceHandler = SurfaceController(drop_shadow_margin=case.drop_shadow_margin)

    assert handler.drop_shadow_margin(window) == case.expected


class PushTestCase(NamedTuple):
    name: str
    initial_states: Qt.WindowState
    transitions: list[Qt.WindowState]
    pushed: list[int]


@pytest.mark.parametrize(
    "case",
    [
        PushTestCase(
            "configure_normal_pushes_margin",
            initial_states=NO_STATE,
            transitions=[],
            pushed=[88],
        ),
        PushTestCase(
            "configure_maximized_stays_silent",
            initial_states=MAXIMIZED,
            transitions=[],
            pushed=[],
        ),
        PushTestCase(
            "maximize_collapses_and_restore_brings_back",
            initial_states=NO_STATE,
            transitions=[MAXIMIZED, NO_STATE],
            pushed=[88, 0, 88],
        ),
        PushTestCase(
            "fullscreen_to_maximized_pushes_only_the_collapse",
            initial_states=NO_STATE,
            transitions=[FULLSCREEN, MAXIMIZED],
            pushed=[88, 0],
        ),
        PushTestCase(
            "minimize_from_normal_stays_silent",
            initial_states=NO_STATE,
            transitions=[MINIMIZED, NO_STATE],
            pushed=[88],
        ),
        PushTestCase(
            "minimize_from_maximized_stays_collapsed",
            initial_states=MAXIMIZED,
            transitions=[MAXIMIZED | MINIMIZED, MAXIMIZED],
            pushed=[],
        ),
    ],
    ids=lambda case: case.name,
)
def test_drop_shadow_margin_pushes(case: PushTestCase, qt_app, make_recording_window):
    window = make_recording_window(case.initial_states)
    controller = SurfaceController(drop_shadow_margin=88)
    pushed: list[int] = []
    controller.on_drop_shadow_margin_changed(pushed.append)

    controller.configure_window(qt_app, window)
    for states in case.transitions:
        window.setWindowStates(states)

    assert pushed == case.pushed


def test_screen_change_reapplies_content_margins(qt_app, make_recording_window, monkeypatch):
    applied: list[int] = []
    monkeypatch.setattr(f"{SURFACE}.apply_wayland_content_margins", lambda _window, margin: applied.append(margin))
    monkeypatch.setattr(f"{SURFACE}.QGuiApplication.platformName", staticmethod(lambda: "wayland"))

    window = make_recording_window(NO_STATE)
    controller = SurfaceController(drop_shadow_margin=88)
    controller.configure_window(qt_app, window)
    assert applied == [88]

    window.screenChanged.emit(window.screen())

    assert applied == [88, 88]


def test_no_surface_handler_reads_zero_and_never_pushes(make_recording_window):
    handler: SurfaceHandler = NoSurfaceHandler()
    pushed: list[int] = []
    handler.on_drop_shadow_margin_changed(pushed.append)

    for states in (NO_STATE, MINIMIZED, MAXIMIZED, FULLSCREEN):
        window = make_recording_window(states)
        assert handler.drop_shadow_margin(window) == 0
        window.setWindowStates(states)

    assert pushed == []
