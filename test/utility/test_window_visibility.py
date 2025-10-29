# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple
from unittest.mock import MagicMock, patch

import inject
import pytest

from mpvqc.services import WindowPropertiesService
from mpvqc.utility.window_visibility import MpvqcWindowVisibilityHandler


@pytest.fixture
def window_mock():
    mock = MagicMock()
    mock.showNormal = MagicMock()
    mock.showMaximized = MagicMock()
    mock.showFullScreen = MagicMock()
    return mock


@pytest.fixture
def window_properties_service_mock():
    mock = MagicMock(spec_set=WindowPropertiesService)
    mock.is_fullscreen = False
    mock.is_maximized = False
    return mock


@pytest.fixture(autouse=True)
def configure_inject(window_properties_service_mock, window_mock):
    with patch("mpvqc.utility.window_visibility.get_main_window", return_value=window_mock):

        def config(binder: inject.Binder):
            binder.bind(WindowPropertiesService, window_properties_service_mock)

        inject.configure(config, clear=True)


@pytest.fixture
def handler(window_properties_service_mock):
    with patch("mpvqc.utility.window_visibility.get_main_window") as mock_window:
        window = MagicMock()
        mock_window.return_value = window
        # noinspection PyCallingNonCallable
        handler = MpvqcWindowVisibilityHandler()
        handler._window = window
        return handler


class ToggleTestCase(NamedTuple):
    tag: str
    fullscreen: bool
    maximized: bool
    was_maximized_before: bool
    expected_method: str


@pytest.mark.parametrize(
    "test_case",
    [
        ToggleTestCase(
            tag="no full, not max before -> full",
            fullscreen=False,
            maximized=False,
            was_maximized_before=False,
            expected_method="showFullScreen",
        ),
        ToggleTestCase(
            tag="no full, max before -> full",
            fullscreen=False,
            maximized=True,
            was_maximized_before=False,
            expected_method="showFullScreen",
        ),
        ToggleTestCase(
            tag="full, not max before -> normal",
            fullscreen=True,
            maximized=False,
            was_maximized_before=False,
            expected_method="showNormal",
        ),
        ToggleTestCase(
            tag="full, max before -> max",
            fullscreen=True,
            maximized=False,
            was_maximized_before=True,
            expected_method="showMaximized",
        ),
    ],
    ids=lambda tc: tc.tag,
)
def test_toggle_fullscreen(handler, window_properties_service_mock, test_case: ToggleTestCase):
    window_properties_service_mock.is_fullscreen = test_case.fullscreen
    window_properties_service_mock.is_maximized = test_case.maximized
    handler._was_maximized_before = test_case.was_maximized_before

    handler.toggleFullScreen()

    expected_call = getattr(handler._window, test_case.expected_method)
    expected_call.assert_called_once()
