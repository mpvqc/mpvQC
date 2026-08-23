# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
from PySide6.QtGui import QWindow

from mpvqc.window.services import SurfaceSnapshot, WindowButtonPreference, windows_capabilities

ALL_BUTTONS = WindowButtonPreference(minimize=True, maximize=True, close=True)
CLOSE_ONLY = WindowButtonPreference(minimize=False, maximize=False, close=True)
OWN_FRAME = SurfaceSnapshot(draws_own_frame=True, drop_shadow_margin=88)


@pytest.fixture
def window(qt_app) -> QWindow:
    return QWindow()


def test_the_capabilities_are_handed_out_whole(make_platform_service):
    capabilities = windows_capabilities()
    platform = make_platform_service(capabilities=capabilities)

    assert platform.capabilities is capabilities


def test_configure_window_configures_the_window_and_installs_the_revealer(
    make_platform_service, window_configurator, window_revealer, qt_app, window
):
    platform = make_platform_service(window_configuration=window_configurator, window_reveal=window_revealer)

    platform.configure_window(qt_app, window)

    assert window_configurator.configured == [(qt_app, window)]
    assert window_revealer.installed == [(qt_app, window)]


def test_tracking_the_embedded_player_reaches_the_tracker(make_platform_service, embedded_player):
    platform = make_platform_service(embedded_player=embedded_player)

    platform.track_embedded_player(42)

    assert embedded_player.tracked == [42]


def test_a_pushed_button_preference_arrives_as_a_signal(make_platform_service, make_window_buttons, make_spy):
    window_buttons = make_window_buttons(ALL_BUTTONS)
    platform = make_platform_service(window_buttons=window_buttons)
    spy = make_spy(platform.window_button_preference_changed)

    window_buttons.push(CLOSE_ONLY)

    assert spy.count() == 1
    assert spy.at(0, 0) == CLOSE_ONLY


def test_read_surface_hands_out_the_handler_snapshot(make_platform_service, surface, window):
    surface.snapshot = OWN_FRAME
    platform = make_platform_service(surface=surface)

    assert platform.read_surface(window) == OWN_FRAME
    assert surface.reads == [window]


def test_a_pushed_surface_arrives_as_a_signal(make_platform_service, surface, make_spy):
    platform = make_platform_service(surface=surface)
    spy = make_spy(platform.surface_changed)

    surface.push(OWN_FRAME)

    assert spy.count() == 1
    assert spy.at(0, 0) == OWN_FRAME
