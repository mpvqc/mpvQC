# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.player.services import PlayerService
from mpvqc.services import QuitService


@pytest.fixture
def player_service_mock() -> MagicMock:
    return MagicMock(spec_set=PlayerService)


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, player_service_mock):
    def custom_bindings(binder: inject.Binder):
        binder.bind(PlayerService, player_service_mock)

    common_bindings_with(custom_bindings)


def test_shutdown_terminates_the_player(qt_app, player_service_mock):
    QuitService().shutdown()

    player_service_mock.terminate.assert_called_once_with()
