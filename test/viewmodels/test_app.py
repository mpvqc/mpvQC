# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple
from unittest.mock import MagicMock

import inject
import pytest
from PySide6.QtCore import Qt

from mpvqc.services import (
    HostIntegrationService,
    KeyCommandGeneratorService,
    PlayerService,
    SettingsService,
    WindowPropertiesService,
)
from mpvqc.viewmodels import MpvqcAppViewModel


@pytest.fixture
def host_integration_service_mock():
    mock = MagicMock(spec_set=HostIntegrationService)
    mock.is_tiling_window_manager = False
    return mock


@pytest.fixture
def window_properties_service_mock():
    mock = MagicMock(spec_set=WindowPropertiesService)
    mock.is_fullscreen = False
    mock.is_maximized = False
    return mock


@pytest.fixture
def player_service_mock():
    return MagicMock(spec_set=PlayerService)


@pytest.fixture
def command_generator_mock():
    return MagicMock(spec_set=KeyCommandGeneratorService)


@pytest.fixture(autouse=True)
def configure_inject(
    common_bindings_with,
    host_integration_service_mock,
    window_properties_service_mock,
    player_service_mock,
    command_generator_mock,
    settings_service,
):
    def custom_bindings(binder: inject.Binder):
        binder.bind(HostIntegrationService, host_integration_service_mock)
        binder.bind(WindowPropertiesService, window_properties_service_mock)
        binder.bind(PlayerService, player_service_mock)
        binder.bind(KeyCommandGeneratorService, command_generator_mock)
        binder.bind(SettingsService, settings_service)

    common_bindings_with(custom_bindings)


@pytest.fixture
def view_model() -> MpvqcAppViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcAppViewModel()


class WindowBorderTestCase(NamedTuple):
    name: str
    is_tiling_wm: bool
    is_fullscreen: bool
    is_maximized: bool
    expected_border: int


@pytest.mark.parametrize(
    "test_case",
    [
        WindowBorderTestCase(
            name="normal_window_has_border",
            is_tiling_wm=False,
            is_fullscreen=False,
            is_maximized=False,
            expected_border=1,
        ),
        WindowBorderTestCase(
            name="fullscreen_has_no_border",
            is_tiling_wm=False,
            is_fullscreen=True,
            is_maximized=False,
            expected_border=0,
        ),
        WindowBorderTestCase(
            name="maximized_has_no_border",
            is_tiling_wm=False,
            is_fullscreen=False,
            is_maximized=True,
            expected_border=0,
        ),
        WindowBorderTestCase(
            name="fullscreen_and_maximized_has_no_border",
            is_tiling_wm=False,
            is_fullscreen=True,
            is_maximized=True,
            expected_border=0,
        ),
        WindowBorderTestCase(
            name="tiling_wm_normal_has_no_border",
            is_tiling_wm=True,
            is_fullscreen=False,
            is_maximized=False,
            expected_border=0,
        ),
        WindowBorderTestCase(
            name="tiling_wm_fullscreen_has_no_border",
            is_tiling_wm=True,
            is_fullscreen=True,
            is_maximized=False,
            expected_border=0,
        ),
        WindowBorderTestCase(
            name="tiling_wm_maximized_has_no_border",
            is_tiling_wm=True,
            is_fullscreen=False,
            is_maximized=True,
            expected_border=0,
        ),
    ],
    ids=lambda tc: tc.name,
)
def test_window_border(test_case: WindowBorderTestCase, host_integration_service_mock, window_properties_service_mock):
    host_integration_service_mock.is_tiling_window_manager = test_case.is_tiling_wm
    window_properties_service_mock.is_fullscreen = test_case.is_fullscreen
    window_properties_service_mock.is_maximized = test_case.is_maximized

    # noinspection PyCallingNonCallable
    view_model = MpvqcAppViewModel()

    assert view_model.windowBorder == test_case.expected_border


def test_forward_key_to_player_sends_generated_command(view_model, player_service_mock, command_generator_mock):
    command_generator_mock.generate_command.return_value = "SPACE"
    view_model.forwardKeyToPlayer(Qt.Key.Key_Space, Qt.KeyboardModifier.NoModifier)
    command_generator_mock.generate_command.assert_called_once_with(Qt.Key.Key_Space, Qt.KeyboardModifier.NoModifier)
    player_service_mock.press_key.assert_called_once_with("SPACE")


def test_forward_key_to_player_skips_when_no_command_generated(view_model, player_service_mock, command_generator_mock):
    command_generator_mock.generate_command.return_value = None
    view_model.forwardKeyToPlayer(Qt.Key.Key_unknown, Qt.KeyboardModifier.NoModifier)
    player_service_mock.press_key.assert_not_called()
