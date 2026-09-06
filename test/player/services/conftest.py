# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.appdata.services import ApplicationPathsService
from mpvqc.player.services import RawPropertyValue


@pytest.fixture
def application_paths_service_mock() -> MagicMock:
    return MagicMock(spec_set=ApplicationPathsService)


@pytest.fixture(autouse=True)
def configure_injections(
    common_bindings_with,
    application_paths_service_mock,
):
    def custom_bindings(binder: inject.Binder):
        binder.bind(ApplicationPathsService, application_paths_service_mock)

    common_bindings_with(custom_bindings)


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


@pytest.fixture
def push_file_load_failed(qt_app, player_handle):
    def _push() -> None:
        player_handle.push_file_load_failed()
        qt_app.processEvents()

    return _push
