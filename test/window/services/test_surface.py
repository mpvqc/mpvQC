# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TYPE_CHECKING, NamedTuple

import pytest
from PySide6.QtCore import Qt

from mpvqc.window.services import NoSurfaceHandler, SurfaceSnapshot
from mpvqc.window.services.linux import SurfaceController

if TYPE_CHECKING:
    from mpvqc.window.services import SurfaceHandler

SURFACE = "mpvqc.window.services.linux.surface"

NO_STATE = Qt.WindowState.WindowNoState
MINIMIZED = Qt.WindowState.WindowMinimized
MAXIMIZED = Qt.WindowState.WindowMaximized
FULLSCREEN = Qt.WindowState.WindowFullScreen

NO_OWN_FRAME = SurfaceSnapshot(draws_own_frame=False, drop_shadow_margin=0)
OWN_FRAME = SurfaceSnapshot(draws_own_frame=True, drop_shadow_margin=88)


class ReadSurfaceTestCase(NamedTuple):
    name: str
    drop_shadow_margin: int
    states: Qt.WindowState
    expected: SurfaceSnapshot


@pytest.mark.parametrize(
    "case",
    [
        ReadSurfaceTestCase(
            name="zero_margin_still_draws_the_frame",
            drop_shadow_margin=0,
            states=NO_STATE,
            expected=SurfaceSnapshot(draws_own_frame=True, drop_shadow_margin=0),
        ),
        ReadSurfaceTestCase(
            name="normal_draws_the_frame_with_the_margin",
            drop_shadow_margin=88,
            states=NO_STATE,
            expected=OWN_FRAME,
        ),
        ReadSurfaceTestCase(
            name="maximized_drops_the_frame_and_the_margin",
            drop_shadow_margin=88,
            states=MAXIMIZED,
            expected=NO_OWN_FRAME,
        ),
        ReadSurfaceTestCase(
            name="fullscreen_drops_the_frame_and_the_margin",
            drop_shadow_margin=88,
            states=FULLSCREEN,
            expected=NO_OWN_FRAME,
        ),
        ReadSurfaceTestCase(
            name="minimized_from_maximized_stays_without_frame",
            drop_shadow_margin=88,
            states=MAXIMIZED | MINIMIZED,
            expected=NO_OWN_FRAME,
        ),
        ReadSurfaceTestCase(
            name="minimized_from_normal_keeps_the_frame",
            drop_shadow_margin=88,
            states=MINIMIZED,
            expected=OWN_FRAME,
        ),
    ],
    ids=lambda case: case.name,
)
def test_read_surface(case: ReadSurfaceTestCase, make_recording_window):
    window = make_recording_window(case.states)
    handler: SurfaceHandler = SurfaceController(drop_shadow_margin=case.drop_shadow_margin)

    assert handler.read_surface(window) == case.expected


class PushTestCase(NamedTuple):
    name: str
    initial_states: Qt.WindowState
    transitions: list[Qt.WindowState]
    pushed: list[SurfaceSnapshot]


@pytest.mark.parametrize(
    "case",
    [
        PushTestCase(
            name="configure_normal_pushes_the_frame",
            initial_states=NO_STATE,
            transitions=[],
            pushed=[OWN_FRAME],
        ),
        PushTestCase(
            name="configure_maximized_stays_silent",
            initial_states=MAXIMIZED,
            transitions=[],
            pushed=[],
        ),
        PushTestCase(
            name="maximize_drops_the_frame_and_restore_brings_it_back",
            initial_states=NO_STATE,
            transitions=[MAXIMIZED, NO_STATE],
            pushed=[OWN_FRAME, NO_OWN_FRAME, OWN_FRAME],
        ),
        PushTestCase(
            name="fullscreen_to_maximized_pushes_only_the_drop",
            initial_states=NO_STATE,
            transitions=[FULLSCREEN, MAXIMIZED],
            pushed=[OWN_FRAME, NO_OWN_FRAME],
        ),
        PushTestCase(
            name="minimize_from_normal_stays_silent",
            initial_states=NO_STATE,
            transitions=[MINIMIZED, NO_STATE],
            pushed=[OWN_FRAME],
        ),
        PushTestCase(
            name="minimize_from_maximized_stays_without_frame",
            initial_states=MAXIMIZED,
            transitions=[MAXIMIZED | MINIMIZED, MAXIMIZED],
            pushed=[],
        ),
    ],
    ids=lambda case: case.name,
)
def test_surface_pushes(case: PushTestCase, qt_app, make_recording_window):
    window = make_recording_window(case.initial_states)
    controller = SurfaceController(drop_shadow_margin=88)
    pushed: list[SurfaceSnapshot] = []
    controller.on_surface_changed(pushed.append)

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


def test_no_surface_handler_reads_no_own_frame_and_never_pushes(make_recording_window):
    handler: SurfaceHandler = NoSurfaceHandler()
    pushed: list[SurfaceSnapshot] = []
    handler.on_surface_changed(pushed.append)

    for states in (NO_STATE, MINIMIZED, MAXIMIZED, FULLSCREEN):
        window = make_recording_window(states)
        assert handler.read_surface(window) == NO_OWN_FRAME
        window.setWindowStates(states)

    assert pushed == []
