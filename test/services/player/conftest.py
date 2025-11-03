# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.services import ApplicationPathsService, PlayerService


@pytest.fixture
def mpv_mock() -> MagicMock:
    return MagicMock()


@pytest.fixture
def player_service(ubiquitous_bindings, mpv_mock) -> PlayerService:
    def config(binder: inject.Binder):
        binder.install(ubiquitous_bindings)
        binder.bind(ApplicationPathsService, MagicMock(spec_set=ApplicationPathsService))

    inject.configure(config, bind_in_runtime=False, clear=True)

    service = PlayerService()
    service._mpv = mpv_mock
    return service
