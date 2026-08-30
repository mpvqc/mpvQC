# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest
from PySide6.QtCore import Qt

from mpvqc.player.services import PlayerService
from mpvqc.services import SettingsService
from mpvqc.viewmodels import MpvqcAppViewModel


@pytest.fixture
def player_service_mock():
    return MagicMock(spec_set=PlayerService)


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, player_service_mock, settings_service):
    def custom_bindings(binder: inject.Binder):
        binder.bind(PlayerService, player_service_mock)
        binder.bind(SettingsService, settings_service)

    common_bindings_with(custom_bindings)


@pytest.fixture
def view_model() -> MpvqcAppViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcAppViewModel()


def test_forward_key_to_player_presses_the_key(view_model, player_service_mock):
    view_model.forwardKeyToPlayer(Qt.Key.Key_Space, Qt.KeyboardModifier.NoModifier)
    player_service_mock.press_key.assert_called_once_with("SPACE")


def test_forward_key_to_player_skips_a_key_without_a_name(view_model, player_service_mock):
    view_model.forwardKeyToPlayer(Qt.Key.Key_F1, Qt.KeyboardModifier.NoModifier)
    player_service_mock.press_key.assert_not_called()
