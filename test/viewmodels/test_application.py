# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple
from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.services import HostIntegrationService, WindowPropertiesService
from mpvqc.viewmodels import MpvqcApplicationViewModel


@pytest.fixture
def host_integration_service_mock():
    mock = MagicMock(spec_set=HostIntegrationService)
    mock.is_tiling_window_manager = False
    return mock


@pytest.fixture
def window_properties_service_mock():
    mock = MagicMock(spec_set=WindowPropertiesService)
    mock.is_fullscreen = False
    mock.is_maximized = False
    return mock


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, host_integration_service_mock, window_properties_service_mock):
    def custom_bindings(binder: inject.Binder):
        binder.bind(HostIntegrationService, host_integration_service_mock)
        binder.bind(WindowPropertiesService, window_properties_service_mock)

    common_bindings_with(custom_bindings)


class WindowBorderTestCase(NamedTuple):
    name: str
    is_tiling_wm: bool
    is_fullscreen: bool
    is_maximized: bool
    expected_border: int


@pytest.mark.parametrize(
    "test_case",
    [
        WindowBorderTestCase(
            name="normal_window_has_border",
            is_tiling_wm=False,
            is_fullscreen=False,
            is_maximized=False,
            expected_border=1,
        ),
        WindowBorderTestCase(
            name="fullscreen_has_no_border",
            is_tiling_wm=False,
            is_fullscreen=True,
            is_maximized=False,
            expected_border=0,
        ),
        WindowBorderTestCase(
            name="maximized_has_no_border",
            is_tiling_wm=False,
            is_fullscreen=False,
            is_maximized=True,
            expected_border=0,
        ),
        WindowBorderTestCase(
            name="fullscreen_and_maximized_has_no_border",
            is_tiling_wm=False,
            is_fullscreen=True,
            is_maximized=True,
            expected_border=0,
        ),
        WindowBorderTestCase(
            name="tiling_wm_normal_has_no_border",
            is_tiling_wm=True,
            is_fullscreen=False,
            is_maximized=False,
            expected_border=0,
        ),
        WindowBorderTestCase(
            name="tiling_wm_fullscreen_has_no_border",
            is_tiling_wm=True,
            is_fullscreen=True,
            is_maximized=False,
            expected_border=0,
        ),
        WindowBorderTestCase(
            name="tiling_wm_maximized_has_no_border",
            is_tiling_wm=True,
            is_fullscreen=False,
            is_maximized=True,
            expected_border=0,
        ),
    ],
    ids=lambda tc: tc.name,
)
def test_window_border(test_case: WindowBorderTestCase, host_integration_service_mock, window_properties_service_mock):
    host_integration_service_mock.is_tiling_window_manager = test_case.is_tiling_wm
    window_properties_service_mock.is_fullscreen = test_case.is_fullscreen
    window_properties_service_mock.is_maximized = test_case.is_maximized

    # noinspection PyCallingNonCallable
    view_model = MpvqcApplicationViewModel()

    assert view_model.windowBorder == test_case.expected_border
