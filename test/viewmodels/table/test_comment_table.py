# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.services import PlayerService, ResetService, SettingsService, StateService


@pytest.fixture(autouse=True)
def configure_injections(settings_service):
    def config(binder: inject.Binder):
        player_mock = MagicMock(spec_set=PlayerService)
        player_mock.current_time = 0.0

        binder.bind(PlayerService, player_mock)
        binder.bind(ResetService, MagicMock(spec_set=ResetService))
        binder.bind(SettingsService, settings_service)
        binder.bind(StateService, MagicMock(spec_set=StateService))

    inject.configure(config, clear=True)
