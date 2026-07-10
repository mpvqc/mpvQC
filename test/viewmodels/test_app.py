# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest
from PySide6.QtCore import Qt

from mpvqc.services import (
    KeyCommandGeneratorService,
    MainWindowService,
    PlatformService,
    PlayerService,
    SettingsService,
)
from mpvqc.viewmodels import MpvqcAppViewModel


@pytest.fixture
def platform_service_mock():
    return MagicMock(spec_set=PlatformService)


@pytest.fixture
def main_window_service_mock():
    mock = MagicMock(spec_set=MainWindowService)
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
    platform_service_mock,
    main_window_service_mock,
    player_service_mock,
    command_generator_mock,
    settings_service,
):
    def custom_bindings(binder: inject.Binder):
        binder.bind(PlatformService, platform_service_mock)
        binder.bind(MainWindowService, main_window_service_mock)
        binder.bind(PlayerService, player_service_mock)
        binder.bind(KeyCommandGeneratorService, command_generator_mock)
        binder.bind(SettingsService, settings_service)

    common_bindings_with(custom_bindings)


@pytest.fixture
def view_model() -> MpvqcAppViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcAppViewModel()


def test_shadow_margin_forwards_service_value(main_window_service_mock):
    main_window_service_mock.shadow_margin = 128

    # noinspection PyCallingNonCallable
    view_model = MpvqcAppViewModel()

    assert view_model.shadowMargin == 128


def test_forward_key_to_player_sends_generated_command(view_model, player_service_mock, command_generator_mock):
    command_generator_mock.generate_command.return_value = "SPACE"
    view_model.forwardKeyToPlayer(Qt.Key.Key_Space, Qt.KeyboardModifier.NoModifier)
    command_generator_mock.generate_command.assert_called_once_with(Qt.Key.Key_Space, Qt.KeyboardModifier.NoModifier)
    player_service_mock.press_key.assert_called_once_with("SPACE")


def test_forward_key_to_player_skips_when_no_command_generated(view_model, player_service_mock, command_generator_mock):
    command_generator_mock.generate_command.return_value = None
    view_model.forwardKeyToPlayer(Qt.Key.Key_unknown, Qt.KeyboardModifier.NoModifier)
    player_service_mock.press_key.assert_not_called()
