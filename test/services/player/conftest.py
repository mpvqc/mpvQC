# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.services import ApplicationPathsService, PlayerService


@pytest.fixture
def application_paths_service_mock() -> MagicMock:
    return MagicMock(spec_set=ApplicationPathsService)


@pytest.fixture
def mpv_mock() -> MagicMock:
    return MagicMock()


@pytest.fixture(autouse=True)
def configure_injections(
    common_bindings_with,
    application_paths_service_mock,
):
    def custom_bindings(binder: inject.Binder):
        binder.bind(ApplicationPathsService, application_paths_service_mock)

    common_bindings_with(custom_bindings)


@pytest.fixture
def player_service(mpv_mock) -> PlayerService:
    service = PlayerService()
    service._mpv = mpv_mock
    return service
