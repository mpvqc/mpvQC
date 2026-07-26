# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple
from unittest.mock import MagicMock

import inject
import pytest
from PySide6.QtGui import QWindow

from mpvqc.services import MainWindowService, PlatformService


@pytest.fixture
def platform_service_mock():
    mock = MagicMock(spec_set=PlatformService)
    mock.is_fullscreen.return_value = False
    mock.is_maximized.return_value = False
    mock.shadow_margin.return_value = 0
    return mock


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, platform_service_mock):
    def custom_bindings(binder: inject.Binder):
        binder.bind(PlatformService, platform_service_mock)

    common_bindings_with(custom_bindings)


@pytest.fixture
def service() -> MainWindowService:
    return MainWindowService()


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


def test_refresh_shadow_margin_applies_and_emits_content_size(qt_app, service, platform_service_mock):
    service._window = QWindow()
    service._outer_width = 1280
    service._outer_height = 720
    platform_service_mock.shadow_margin.return_value = 88

    margins: list[int] = []
    widths: list[int] = []
    service.shadow_margin_changed.connect(margins.append)
    service.content_width_changed.connect(widths.append)

    service._refresh_shadow_margin()

    assert service.shadow_margin == 88
    platform_service_mock.apply_content_margins.assert_called_once_with(88)
    assert margins == [88]
    assert widths == [1280 - 2 * 88]


def test_refresh_shadow_margin_is_noop_when_unchanged(qt_app, service, platform_service_mock):
    service._window = QWindow()

    margins: list[int] = []
    service.shadow_margin_changed.connect(margins.append)

    service._refresh_shadow_margin()

    assert service.shadow_margin == 0
    platform_service_mock.apply_content_margins.assert_not_called()
    assert margins == []


class InitializeBroadcastTestCase(NamedTuple):
    name: str
    shadow_margin: int
    expected_width: int
    expected_height: int


@pytest.mark.parametrize(
    "case",
    [
        InitializeBroadcastTestCase(
            "with_shadow_margin",
            shadow_margin=88,
            expected_width=1280 - 2 * 88,
            expected_height=720 - 2 * 88,
        ),
        InitializeBroadcastTestCase(
            "without_shadow_margin",
            shadow_margin=0,
            expected_width=1280,
            expected_height=720,
        ),
    ],
    ids=lambda case: case.name,
)
def test_initialize_broadcasts_content_size(case, qt_app, service, platform_service_mock, make_spy):
    platform_service_mock.shadow_margin.return_value = case.shadow_margin

    window = QWindow()
    window.resize(1280, 720)

    width_spy = make_spy(service.content_width_changed)
    height_spy = make_spy(service.content_height_changed)

    service.initialize(window)

    assert width_spy.count() >= 1
    assert height_spy.count() >= 1
    assert width_spy.at(width_spy.count() - 1, 0) == case.expected_width
    assert height_spy.at(height_spy.count() - 1, 0) == case.expected_height


def test_minimize_delegates_to_platform(qt_app, service, platform_service_mock):
    window = QWindow()
    service._window = window

    service.minimize()

    platform_service_mock.minimize.assert_called_once_with(window)


def test_show_maximized_delegates_to_platform(qt_app, service, platform_service_mock):
    window = QWindow()
    service._window = window

    service.show_maximized()

    platform_service_mock.maximize.assert_called_once_with(window)


def test_show_normal_delegates_to_platform(qt_app, service, platform_service_mock):
    window = QWindow()
    service._window = window

    service.show_normal()

    platform_service_mock.show_normal.assert_called_once_with(window)


def test_show_fullscreen_delegates_to_platform(qt_app, service, platform_service_mock):
    window = QWindow()
    service._window = window

    service.show_fullscreen()

    platform_service_mock.enter_fullscreen.assert_called_once_with(window)


def test_exit_fullscreen_delegates_to_platform(qt_app, service, platform_service_mock):
    window = QWindow()
    service._window = window

    service.exit_fullscreen()

    platform_service_mock.exit_fullscreen.assert_called_once_with(window)


def test_state_reads_report_platform_answers(qt_app, service, platform_service_mock):
    service._window = QWindow()

    platform_service_mock.is_fullscreen.return_value = True
    platform_service_mock.is_maximized.return_value = True
    service._sync_window_state()
    assert service.is_fullscreen
    assert service.is_maximized

    platform_service_mock.is_fullscreen.return_value = False
    platform_service_mock.is_maximized.return_value = False
    service._sync_window_state()
    assert not service.is_fullscreen
    assert not service.is_maximized


def test_state_sync_reads_fullscreen_before_maximized(qt_app, service, platform_service_mock):
    service._window = QWindow()

    service._sync_window_state()

    calls = [name for name, *_ in platform_service_mock.mock_calls]
    assert calls.index("is_fullscreen") < calls.index("is_maximized")


def test_unchanged_states_emit_nothing(qt_app, service, platform_service_mock, make_spy):
    service._window = QWindow()
    platform_service_mock.is_fullscreen.return_value = True
    platform_service_mock.is_maximized.return_value = True

    fullscreen_spy = make_spy(service.is_fullscreen_changed)
    maximized_spy = make_spy(service.is_maximized_changed)

    service._sync_window_state()
    service._sync_window_state()

    assert fullscreen_spy.count() == 1
    assert maximized_spy.count() == 1


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
