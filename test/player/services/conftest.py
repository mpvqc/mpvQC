# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.player.services import PlayerService, RawPropertyValue
from mpvqc.services import ApplicationPathsService
from test.player.recording import RecordingPlayerHandle


@pytest.fixture
def application_paths_service_mock() -> MagicMock:
    return MagicMock(spec_set=ApplicationPathsService)


@pytest.fixture
def player_handle() -> RecordingPlayerHandle:
    return RecordingPlayerHandle()


@pytest.fixture(autouse=True)
def configure_injections(
    common_bindings_with,
    application_paths_service_mock,
):
    def custom_bindings(binder: inject.Binder):
        binder.bind(ApplicationPathsService, application_paths_service_mock)

    common_bindings_with(custom_bindings)


@pytest.fixture
def player_service(configure_injections, player_handle) -> PlayerService:
    service = PlayerService(player_handle)
    service.init()
    return service


@pytest.fixture
def push_property(qt_app, player_handle):
    def _push(name: str, raw: RawPropertyValue) -> None:
        player_handle.push_property(name, raw)
        qt_app.processEvents()

    return _push


@pytest.fixture
def push_file_loaded(qt_app, player_handle):
    def _push() -> None:
        player_handle.push_file_loaded()
        qt_app.processEvents()

    return _push
