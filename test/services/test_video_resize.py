# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple
from unittest.mock import MagicMock

import inject
import pytest
from PySide6.QtCore import Qt

from mpvqc.services import (
    HostIntegrationService,
    PlayerService,
    SettingsService,
    VideoResizeService,
    WindowPropertiesService,
)
from mpvqc.services.video_resize import (
    ResizeResult,
    ViewDimensions,
    calculate_horizontal_layout_sizes,
    calculate_vertical_layout_sizes,
)

HEADER_HEIGHT = 40
BORDER_SIZE = 6
HANDLE_WIDTH = 6
HANDLE_HEIGHT = 6


class VerticalLayoutTestCase(NamedTuple):
    video_width: int
    video_height: int
    table_height: int
    available_height: int
    expected: ResizeResult


@pytest.mark.parametrize(
    "case",
    [
        VerticalLayoutTestCase(
            video_width=854,
            video_height=480,
            table_height=200,
            available_height=int(1440 * 0.95),
            expected=ResizeResult(
                window_width=866,
                window_height=738,
                table_width=854,
                table_height=200,
            ),
        ),
        VerticalLayoutTestCase(
            video_width=854,
            video_height=480,
            table_height=900,
            available_height=int(1440 * 0.95),
            expected=ResizeResult(
                window_width=866,
                window_height=1368,
                table_width=854,
                table_height=830,
            ),
        ),
    ],
)
def test_calculate_vertical_layout_sizes(case: VerticalLayoutTestCase):
    actual = calculate_vertical_layout_sizes(
        video_width=case.video_width,
        video_height=case.video_height,
        header_height=HEADER_HEIGHT,
        border_size=BORDER_SIZE,
        handle_height=HANDLE_HEIGHT,
        table_height=case.table_height,
        available_height=case.available_height,
    )
    assert actual == case.expected


class HorizontalLayoutTestCase(NamedTuple):
    video_width: int
    video_height: int
    table_width: int
    available_width: int
    expected: ResizeResult


@pytest.mark.parametrize(
    "case",
    [
        HorizontalLayoutTestCase(
            video_width=854,
            video_height=480,
            table_width=300,
            available_width=int(2560 * 0.95),
            expected=ResizeResult(
                window_width=1172,
                window_height=532,
                table_width=300,
                table_height=480,
            ),
        ),
        HorizontalLayoutTestCase(
            video_width=854,
            video_height=480,
            table_width=5000,
            available_width=int(2560 * 0.95),
            expected=ResizeResult(
                window_width=2432,
                window_height=532,
                table_width=1560,
                table_height=480,
            ),
        ),
    ],
)
def test_calculate_horizontal_layout_sizes(case: HorizontalLayoutTestCase):
    actual = calculate_horizontal_layout_sizes(
        video_width=case.video_width,
        video_height=case.video_height,
        header_height=HEADER_HEIGHT,
        border_size=BORDER_SIZE,
        handle_width=HANDLE_WIDTH,
        table_width=case.table_width,
        available_width=case.available_width,
    )
    assert actual == case.expected


VIEW_DIMS = ViewDimensions(
    header_height=HEADER_HEIGHT,
    border_size=BORDER_SIZE,
    handle_width=HANDLE_WIDTH,
    handle_height=HANDLE_HEIGHT,
    table_width=300,
    table_height=200,
)


@pytest.fixture
def player_mock() -> MagicMock:
    mock = MagicMock(spec_set=PlayerService)
    mock.video_loaded = True
    mock.width = 854
    mock.height = 480
    return mock


@pytest.fixture
def settings_mock() -> MagicMock:
    mock = MagicMock(spec_set=SettingsService)
    mock.layout_orientation = Qt.Orientation.Vertical.value
    return mock


@pytest.fixture
def window_properties_mock() -> MagicMock:
    mock = MagicMock(spec_set=WindowPropertiesService)
    mock.is_fullscreen = False
    mock.is_maximized = False
    mock.screen_width = 2560
    mock.screen_height = 1440
    return mock


@pytest.fixture
def host_integration_mock() -> MagicMock:
    mock = MagicMock(spec_set=HostIntegrationService)
    mock.display_zoom_factor = 1.0
    return mock


@pytest.fixture(autouse=True)
def configure_injections(
    common_bindings_with,
    player_mock,
    settings_mock,
    window_properties_mock,
    host_integration_mock,
):
    def custom_bindings(binder: inject.Binder):
        binder.bind(PlayerService, player_mock)
        binder.bind(SettingsService, settings_mock)
        binder.bind(WindowPropertiesService, window_properties_mock)
        binder.bind(HostIntegrationService, host_integration_mock)

    common_bindings_with(custom_bindings)


@pytest.fixture
def service() -> VideoResizeService:
    return VideoResizeService()


def test_compute_resize_returns_none_when_fullscreen(service, window_properties_mock):
    window_properties_mock.is_fullscreen = True
    assert service.compute_resize(VIEW_DIMS) is None


def test_compute_resize_returns_none_when_maximized(service, window_properties_mock):
    window_properties_mock.is_maximized = True
    assert service.compute_resize(VIEW_DIMS) is None


def test_compute_resize_returns_none_when_no_video_loaded(service, player_mock):
    player_mock.video_loaded = False
    assert service.compute_resize(VIEW_DIMS) is None


def test_compute_resize_returns_none_when_video_does_not_fit(service, player_mock):
    player_mock.width = 99999
    player_mock.height = 99999
    assert service.compute_resize(VIEW_DIMS) is None


def test_compute_resize_returns_none_when_screen_unavailable(service, window_properties_mock):
    window_properties_mock.screen_width = 0
    window_properties_mock.screen_height = 0
    assert service.compute_resize(VIEW_DIMS) is None


def test_compute_resize_returns_vertical_layout(service):
    result = service.compute_resize(VIEW_DIMS)
    assert result == ResizeResult(
        window_width=866,
        window_height=738,
        table_width=854,
        table_height=200,
    )


def test_compute_resize_returns_horizontal_layout(service, settings_mock):
    settings_mock.layout_orientation = Qt.Orientation.Horizontal.value
    result = service.compute_resize(VIEW_DIMS)
    assert result == ResizeResult(
        window_width=1172,
        window_height=532,
        table_width=300,
        table_height=480,
    )


def test_compute_resize_raises_for_unknown_layout(service, settings_mock):
    settings_mock.layout_orientation = 999
    with pytest.raises(ValueError, match="Unexpected layout orientation"):
        service.compute_resize(VIEW_DIMS)


def test_compute_resize_applies_display_zoom_factor(service, host_integration_mock):
    host_integration_mock.display_zoom_factor = 2.0
    result = service.compute_resize(VIEW_DIMS)
    # Scaled video: 854/2 = 427, 480/2 = 240
    assert result is not None
    assert result.window_width == 427 + 2 * BORDER_SIZE
