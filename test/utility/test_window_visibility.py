# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple
from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.services import MainWindowService
from mpvqc.viewmodels import MpvqcWindowVisibilityViewModel


@pytest.fixture
def main_window_service_mock():
    return MagicMock(spec_set=MainWindowService)


@pytest.fixture(autouse=True)
def configure_injections(
    common_bindings_with,
    main_window_service_mock,
):
    def custom_bindings(binder: inject.Binder):
        binder.bind(MainWindowService, main_window_service_mock)

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
            expected_method="show_fullscreen",
        ),
        ToggleTestCase(
            tag="no full, max before -> full",
            fullscreen=False,
            maximized=True,
            was_maximized_before=False,
            expected_method="show_fullscreen",
        ),
        ToggleTestCase(
            tag="full, not max before -> normal",
            fullscreen=True,
            maximized=False,
            was_maximized_before=False,
            expected_method="show_normal",
        ),
        ToggleTestCase(
            tag="full, max before -> max",
            fullscreen=True,
            maximized=False,
            was_maximized_before=True,
            expected_method="show_maximized",
        ),
    ],
    ids=lambda tc: tc.tag,
)
def test_toggle_fullscreen(main_window_service_mock, test_case: ToggleTestCase):
    # noinspection PyCallingNonCallable
    handler = MpvqcWindowVisibilityViewModel()
    main_window_service_mock.is_fullscreen = test_case.fullscreen
    main_window_service_mock.is_maximized = test_case.maximized
    handler._was_maximized_before = test_case.was_maximized_before

    handler.toggleFullScreen()

    expected_call = getattr(main_window_service_mock, test_case.expected_method)
    expected_call.assert_called_once()
