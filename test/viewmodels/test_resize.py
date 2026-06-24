# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple
from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.services import PlayerService, VideoResizeService
from mpvqc.viewmodels import MpvqcResizeViewModel


@pytest.fixture
def player_mock() -> MagicMock:
    return MagicMock(spec_set=PlayerService)


@pytest.fixture
def resize_service_mock() -> MagicMock:
    return MagicMock(spec_set=VideoResizeService)


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, player_mock, resize_service_mock):
    def custom_bindings(binder: inject.Binder):
        binder.bind(PlayerService, player_mock)
        binder.bind(VideoResizeService, resize_service_mock)

    common_bindings_with(custom_bindings)


class ConnectionTestCase(NamedTuple):
    name: str
    resizes_on_video_load: bool
    should_connect: bool


@pytest.mark.parametrize(
    "case",
    [
        ConnectionTestCase("resizing enabled", resizes_on_video_load=True, should_connect=True),
        ConnectionTestCase("resizing disabled", resizes_on_video_load=False, should_connect=False),
    ],
    ids=lambda case: case.name,
)
def test_video_load_connection_follows_resize_policy(player_mock, resize_service_mock, case: ConnectionTestCase):
    resize_service_mock.resizes_on_video_load = case.resizes_on_video_load

    MpvqcResizeViewModel()

    if case.should_connect:
        player_mock.video_dimensions_changed.connect.assert_called_once()
    else:
        player_mock.video_dimensions_changed.connect.assert_not_called()
