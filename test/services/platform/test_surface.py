# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TYPE_CHECKING, NamedTuple

import pytest
from PySide6.QtCore import Qt

from mpvqc.services import PlatformService
from mpvqc.services.platform.backend import PlatformBackend
from mpvqc.services.platform.embedded_player import NoEmbeddedPlayerTracker
from mpvqc.services.platform.linux.surface import SurfaceController
from mpvqc.services.platform.surface import NoSurfaceHandler
from mpvqc.services.platform.window_buttons import StaticWindowButtons
from mpvqc.services.platform.window_configuration import NoWindowConfigurator
from mpvqc.services.platform.window_reveal import NoWindowRevealer
from mpvqc.services.platform.window_state import QtWindowStateHandler

if TYPE_CHECKING:
    from mpvqc.services.platform.surface import SurfaceHandler

NO_STATE = Qt.WindowState.WindowNoState
MINIMIZED = Qt.WindowState.WindowMinimized
MAXIMIZED = Qt.WindowState.WindowMaximized
FULLSCREEN = Qt.WindowState.WindowFullScreen


class ShadowMarginTestCase(NamedTuple):
    name: str
    composed_margin: int
    states: Qt.WindowState
    expected: int


@pytest.mark.parametrize(
    "case",
    [
        ShadowMarginTestCase(
            "zero_composed_margin_reads_zero",
            composed_margin=0,
            states=NO_STATE,
            expected=0,
        ),
        ShadowMarginTestCase(
            "normal_uses_composed_margin",
            composed_margin=88,
            states=NO_STATE,
            expected=88,
        ),
        ShadowMarginTestCase(
            "maximized_collapses_margin",
            composed_margin=88,
            states=MAXIMIZED,
            expected=0,
        ),
        ShadowMarginTestCase(
            "fullscreen_collapses_margin",
            composed_margin=88,
            states=FULLSCREEN,
            expected=0,
        ),
        ShadowMarginTestCase(
            "minimized_from_maximized_stays_collapsed",
            composed_margin=88,
            states=MAXIMIZED | MINIMIZED,
            expected=0,
        ),
        ShadowMarginTestCase(
            "minimized_from_normal_keeps_margin",
            composed_margin=88,
            states=MINIMIZED,
            expected=88,
        ),
    ],
    ids=lambda case: case.name,
)
def test_shadow_margin(case: ShadowMarginTestCase, make_recording_window):
    window = make_recording_window(case.states)
    handler: SurfaceHandler = SurfaceController(shadow_margin=case.composed_margin)

    assert handler.shadow_margin(window) == case.expected


class EmissionTestCase(NamedTuple):
    name: str
    initial_states: Qt.WindowState
    transitions: list[Qt.WindowState]
    emitted: list[int]


@pytest.mark.parametrize(
    "case",
    [
        EmissionTestCase(
            "configure_normal_emits_composed_margin",
            initial_states=NO_STATE,
            transitions=[],
            emitted=[88],
        ),
        EmissionTestCase(
            "configure_maximized_stays_silent",
            initial_states=MAXIMIZED,
            transitions=[],
            emitted=[],
        ),
        EmissionTestCase(
            "maximize_collapses_and_restore_brings_back",
            initial_states=NO_STATE,
            transitions=[MAXIMIZED, NO_STATE],
            emitted=[88, 0, 88],
        ),
        EmissionTestCase(
            "fullscreen_to_maximized_emits_only_the_collapse",
            initial_states=NO_STATE,
            transitions=[FULLSCREEN, MAXIMIZED],
            emitted=[88, 0],
        ),
        EmissionTestCase(
            "minimize_from_normal_stays_silent",
            initial_states=NO_STATE,
            transitions=[MINIMIZED, NO_STATE],
            emitted=[88],
        ),
        EmissionTestCase(
            "minimize_from_maximized_stays_collapsed",
            initial_states=MAXIMIZED,
            transitions=[MAXIMIZED | MINIMIZED, MAXIMIZED],
            emitted=[],
        ),
    ],
    ids=lambda case: case.name,
)
def test_shadow_margin_changed_emissions(case: EmissionTestCase, qt_app, make_recording_window, make_spy):
    window = make_recording_window(case.initial_states)
    controller = SurfaceController(shadow_margin=88)
    spy = make_spy(controller.shadow_margin_changed)

    controller.configure_window(qt_app, window)
    for states in case.transitions:
        window.setWindowStates(states)

    assert [spy.at(index, 0) for index in range(spy.count())] == case.emitted


def test_no_surface_handler_reads_zero_and_never_emits(make_recording_window, make_spy):
    no_surface = NoSurfaceHandler()
    handler: SurfaceHandler = no_surface
    spy = make_spy(no_surface.shadow_margin_changed)

    for states in (NO_STATE, MINIMIZED, MAXIMIZED, FULLSCREEN):
        window = make_recording_window(states)
        assert handler.shadow_margin(window) == 0
        window.setWindowStates(states)

    assert spy.count() == 0


def test_platform_service_forwards_shadow_margin_changed(qt_app, make_spy):
    surface = NoSurfaceHandler()
    backend = PlatformBackend(
        root_qml_url="",
        desktop_sizes_window=False,
        window_state=QtWindowStateHandler(),
        surface=surface,
        window_configuration=NoWindowConfigurator(),
        window_reveal=NoWindowRevealer(),
        embedded_player=NoEmbeddedPlayerTracker(),
        window_buttons=StaticWindowButtons(),
    )
    service = PlatformService(backend=backend)
    spy = make_spy(service.shadow_margin_changed)

    surface.shadow_margin_changed.emit(88)

    assert spy.count() == 1
    assert spy.at(0, 0) == 88
