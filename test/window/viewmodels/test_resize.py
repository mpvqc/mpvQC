# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.player.services import PlayerService
from mpvqc.window.services import VideoResizeService
from mpvqc.window.viewmodels import MpvqcResizeViewModel


@pytest.fixture
def player_mock() -> MagicMock:
    return MagicMock(spec_set=PlayerService)


@pytest.fixture
def resize_service_mock() -> MagicMock:
    mock = MagicMock(spec_set=VideoResizeService)
    mock.resizes_on_video_change = True
    return mock


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, player_mock, resize_service_mock):
    def custom_bindings(binder: inject.Binder):
        binder.bind(PlayerService, player_mock)
        binder.bind(VideoResizeService, resize_service_mock)

    common_bindings_with(custom_bindings)


@pytest.mark.parametrize(
    ("resizes_on_video_change", "expected_connections"),
    [(True, 1), (False, 0)],
    ids=["app sizes its window", "desktop sizes it"],
)
def test_video_loads_recalculate_only_when_the_app_resizes_itself(
    resizes_on_video_change: bool,
    expected_connections: int,
    player_mock,
    resize_service_mock,
):
    resize_service_mock.resizes_on_video_change = resizes_on_video_change

    MpvqcResizeViewModel()

    assert player_mock.video_dimensions_changed.connect.call_count == expected_connections


def test_no_size_is_requested_when_the_service_declines(resize_service_mock, make_spy):
    resize_service_mock.compute_resize.return_value = None
    view_model = MpvqcResizeViewModel()

    window_spy = make_spy(view_model.appWindowSizeRequested)
    table_spy = make_spy(view_model.splitViewTableSizeRequested)

    view_model.recalculateSizes()

    assert window_spy.count() == 0
    assert table_spy.count() == 0
