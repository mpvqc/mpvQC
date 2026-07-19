# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple
from unittest.mock import MagicMock

import inject
import pytest
from PySide6.QtCore import Qt
from PySide6.QtGui import QWindow

from mpvqc.services import MainWindowService, PlatformService


@pytest.fixture
def platform_service_mock():
    mock = MagicMock(spec_set=PlatformService)
    mock.draws_own_shadow = True
    mock.is_fullscreen.return_value = False
    return mock


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, platform_service_mock):
    def custom_bindings(binder: inject.Binder):
        binder.bind(PlatformService, platform_service_mock)

    common_bindings_with(custom_bindings)


@pytest.fixture
def service() -> MainWindowService:
    return MainWindowService()


class ShadowMarginTestCase(NamedTuple):
    name: str
    draws_own_shadow: bool
    is_fullscreen: bool
    is_maximized: bool
    expected: int


@pytest.mark.parametrize(
    "case",
    [
        ShadowMarginTestCase(
            "normal_window_draws_shadow", draws_own_shadow=True, is_fullscreen=False, is_maximized=False, expected=88
        ),
        ShadowMarginTestCase(
            "no_shadow_no_margin", draws_own_shadow=False, is_fullscreen=False, is_maximized=False, expected=0
        ),
        ShadowMarginTestCase(
            "fullscreen_has_no_margin", draws_own_shadow=True, is_fullscreen=True, is_maximized=False, expected=0
        ),
        ShadowMarginTestCase(
            "maximized_has_no_margin", draws_own_shadow=True, is_fullscreen=False, is_maximized=True, expected=0
        ),
    ],
    ids=lambda case: case.name,
)
def test_compute_shadow_margin(case: ShadowMarginTestCase, service, platform_service_mock):
    platform_service_mock.draws_own_shadow = case.draws_own_shadow
    service._is_fullscreen = case.is_fullscreen
    service._is_maximized = case.is_maximized
    assert service._compute_shadow_margin() == case.expected


def test_width_and_height_subtract_the_shadow_margin(service):
    service._outer_width = 1280
    service._outer_height = 720
    service._shadow_margin = 64
    assert service.content_width == 1280 - 2 * 64
    assert service.content_height == 720 - 2 * 64


def test_width_and_height_equal_surface_without_margin(service):
    service._outer_width = 1280
    service._outer_height = 720
    service._shadow_margin = 0
    assert service.content_width == 1280
    assert service.content_height == 720


def test_refresh_shadow_margin_applies_and_emits_content_size(service, platform_service_mock):
    service._outer_width = 1280
    service._outer_height = 720
    platform_service_mock.draws_own_shadow = True

    margins: list[int] = []
    widths: list[int] = []
    service.shadow_margin_changed.connect(margins.append)
    service.content_width_changed.connect(widths.append)

    service._refresh_shadow_margin()

    assert service.shadow_margin == 88
    platform_service_mock.apply_content_margins.assert_called_once_with(88)
    assert margins == [88]
    assert widths == [1280 - 2 * 88]


def test_refresh_shadow_margin_is_noop_when_unchanged(service, platform_service_mock):
    platform_service_mock.draws_own_shadow = False

    margins: list[int] = []
    service.shadow_margin_changed.connect(margins.append)

    service._refresh_shadow_margin()

    assert service.shadow_margin == 0
    platform_service_mock.apply_content_margins.assert_not_called()
    assert margins == []


class InitializeBroadcastTestCase(NamedTuple):
    name: str
    draws_own_shadow: bool
    expected_width: int
    expected_height: int


@pytest.mark.parametrize(
    "case",
    [
        InitializeBroadcastTestCase(
            "with_shadow_margin", draws_own_shadow=True, expected_width=1280 - 2 * 88, expected_height=720 - 2 * 88
        ),
        InitializeBroadcastTestCase(
            "without_shadow_margin", draws_own_shadow=False, expected_width=1280, expected_height=720
        ),
    ],
    ids=lambda case: case.name,
)
def test_initialize_broadcasts_content_size(case, qt_app, service, platform_service_mock, make_spy):
    platform_service_mock.draws_own_shadow = case.draws_own_shadow

    window = QWindow()
    window.resize(1280, 720)

    width_spy = make_spy(service.content_width_changed)
    height_spy = make_spy(service.content_height_changed)

    service.initialize(window)

    assert width_spy.count() >= 1
    assert height_spy.count() >= 1
    assert width_spy.at(width_spy.count() - 1, 0) == case.expected_width
    assert height_spy.at(height_spy.count() - 1, 0) == case.expected_height


def test_fullscreen_delegates_to_platform(qt_app, service, platform_service_mock):
    window = QWindow()
    service._window = window

    platform_service_mock.is_fullscreen.return_value = True
    service.show_fullscreen()
    platform_service_mock.enter_fullscreen.assert_called_once_with(window)
    assert service.is_fullscreen

    platform_service_mock.is_fullscreen.return_value = False
    service.exit_fullscreen()
    platform_service_mock.exit_fullscreen.assert_called_once_with(window)
    assert not service.is_fullscreen


def test_exit_fullscreen_without_prior_enter_emits_nothing(qt_app, service, platform_service_mock, make_spy):
    service._window = QWindow()

    spy = make_spy(service.is_fullscreen_changed)

    service.exit_fullscreen()

    platform_service_mock.exit_fullscreen.assert_called_once()
    assert not service.is_fullscreen
    assert spy.count() == 0


def test_repeated_show_fullscreen_emits_once(qt_app, service, platform_service_mock, make_spy):
    service._window = QWindow()
    platform_service_mock.is_fullscreen.return_value = True

    spy = make_spy(service.is_fullscreen_changed)

    service.show_fullscreen()
    service.show_fullscreen()

    assert service.is_fullscreen
    assert spy.count() == 1


def test_is_maximized_stays_parked_while_platform_fullscreen(qt_app, service, platform_service_mock):
    window = QWindow()
    window.setWindowStates(Qt.WindowState.WindowMaximized)
    service._window = window

    service._sync_window_state()
    assert service.is_maximized

    # Windows parks the WS_MAXIMIZE style bit while fullscreen
    platform_service_mock.is_fullscreen.return_value = True
    window.setWindowStates(Qt.WindowState.WindowNoState)
    service._sync_window_state()
    assert service.is_fullscreen
    assert service.is_maximized

    platform_service_mock.is_fullscreen.return_value = False
    window.setWindowStates(Qt.WindowState.WindowMaximized)
    service._sync_window_state()
    assert not service.is_fullscreen
    assert service.is_maximized


def test_position_only_change_updates_fullscreen_state(qt_app, service, platform_service_mock):
    service._window = QWindow()

    platform_service_mock.is_fullscreen.return_value = True
    service.show_fullscreen()
    assert service.is_fullscreen

    # The OS moved the window off the monitor without resizing it (keyboard move)
    platform_service_mock.is_fullscreen.return_value = False
    service._on_position_changed(50)

    assert not service.is_fullscreen


def test_on_width_changed_reports_content_width(qt_app, service):
    service._window = QWindow()
    service._shadow_margin = 64

    widths: list[int] = []
    service.content_width_changed.connect(widths.append)

    service._on_width_changed(1280)

    assert service.content_width == 1280 - 2 * 64
    assert widths == [1280 - 2 * 64]
