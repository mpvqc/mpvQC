# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

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


def test_recalculates_on_every_video_load(player_mock):
    MpvqcResizeViewModel()

    player_mock.video_dimensions_changed.connect.assert_called_once()


def test_no_size_is_requested_when_the_service_declines(resize_service_mock, make_spy):
    resize_service_mock.compute_resize.return_value = None
    view_model = MpvqcResizeViewModel()

    window_spy = make_spy(view_model.appWindowSizeRequested)
    table_spy = make_spy(view_model.splitViewTableSizeRequested)

    view_model.recalculateSizes()

    assert window_spy.count() == 0
    assert table_spy.count() == 0
