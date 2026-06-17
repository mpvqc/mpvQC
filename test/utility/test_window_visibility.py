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
def configure_injections(common_bindings_with, main_window_service_mock):
    def custom_bindings(binder: inject.Binder):
        binder.bind(MainWindowService, main_window_service_mock)

    common_bindings_with(custom_bindings)


@pytest.fixture
def handler() -> MpvqcWindowVisibilityViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcWindowVisibilityViewModel()


class ToggleTestCase(NamedTuple):
    tag: str
    fullscreen: bool
    maximized: bool
    expected_method: str


@pytest.mark.parametrize(
    "test_case",
    [
        ToggleTestCase(
            "not maximized -> maximize", fullscreen=False, maximized=False, expected_method="show_maximized"
        ),
        ToggleTestCase("maximized -> normal", fullscreen=False, maximized=True, expected_method="show_normal"),
    ],
    ids=lambda tc: tc.tag,
)
def test_toggle_maximized(handler, main_window_service_mock, test_case: ToggleTestCase):
    main_window_service_mock.is_fullscreen = test_case.fullscreen
    main_window_service_mock.is_maximized = test_case.maximized

    handler.toggleMaximized()

    getattr(main_window_service_mock, test_case.expected_method).assert_called_once()


@pytest.mark.parametrize(
    "test_case",
    [
        ToggleTestCase(
            "not fullscreen -> fullscreen", fullscreen=False, maximized=False, expected_method="show_fullscreen"
        ),
        ToggleTestCase(
            "fullscreen -> exit fullscreen", fullscreen=True, maximized=False, expected_method="exit_fullscreen"
        ),
    ],
    ids=lambda tc: tc.tag,
)
def test_toggle_fullscreen(handler, main_window_service_mock, test_case: ToggleTestCase):
    main_window_service_mock.is_fullscreen = test_case.fullscreen
    main_window_service_mock.is_maximized = test_case.maximized

    handler.toggleFullScreen()

    getattr(main_window_service_mock, test_case.expected_method).assert_called_once()


def test_disable_fullscreen_exits_when_fullscreen(handler, main_window_service_mock):
    main_window_service_mock.is_fullscreen = True

    handler.disableFullScreen()

    main_window_service_mock.exit_fullscreen.assert_called_once()


def test_disable_fullscreen_is_noop_when_not_fullscreen(handler, main_window_service_mock):
    main_window_service_mock.is_fullscreen = False

    handler.disableFullScreen()

    main_window_service_mock.exit_fullscreen.assert_not_called()
