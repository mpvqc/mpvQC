# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple
from unittest.mock import MagicMock, patch

import inject
import pytest

from mpvqc.services import WindowPropertiesService
from mpvqc.utility import MpvqcWindowVisibilityHandler


@pytest.fixture(autouse=True)
def mock_main_window():
    with patch("mpvqc.utility.window_visibility.get_main_window", return_value=MagicMock()):
        yield


@pytest.fixture
def window_properties_service_mock():
    return MagicMock(spec_set=WindowPropertiesService)


@pytest.fixture(autouse=True)
def configure_injections(
    common_bindings_with,
    window_properties_service_mock,
):
    def custom_bindings(binder: inject.Binder):
        binder.bind(WindowPropertiesService, window_properties_service_mock)

    common_bindings_with(custom_bindings)


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
def test_toggle_fullscreen(window_properties_service_mock, test_case: ToggleTestCase):
    # noinspection PyCallingNonCallable
    handler = MpvqcWindowVisibilityHandler()
    window_properties_service_mock.is_fullscreen = test_case.fullscreen
    window_properties_service_mock.is_maximized = test_case.maximized
    handler._was_maximized_before = test_case.was_maximized_before

    handler.toggleFullScreen()

    expected_call = getattr(handler._window, test_case.expected_method)
    expected_call.assert_called_once()
