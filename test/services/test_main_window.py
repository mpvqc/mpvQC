# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple
from unittest.mock import MagicMock

import inject
import pytest
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QWindow

from mpvqc.services import MainWindowService, PlatformService
from mpvqc.services.platform.window_state import WindowStateSnapshot


class PlatformServiceStub(QObject):
    """Carries a real shadow_margin_changed signal so tests can drive pushes;
    everything else is a mock."""

    shadow_margin_changed = Signal(int)

    def __init__(self) -> None:
        super().__init__()
        self.read_state = MagicMock(return_value=WindowStateSnapshot(is_fullscreen=False, is_maximized=False))
        self.shadow_margin = MagicMock(return_value=0)
        self.configure_window = MagicMock()
        self.minimize = MagicMock()
        self.maximize = MagicMock()
        self.show_normal = MagicMock()
        self.enter_fullscreen = MagicMock()
        self.exit_fullscreen = MagicMock()


@pytest.fixture
def platform_service_stub():
    return PlatformServiceStub()


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, platform_service_stub):
    def custom_bindings(binder: inject.Binder):
        binder.bind(PlatformService, platform_service_stub)

    common_bindings_with(custom_bindings)


@pytest.fixture
def service() -> MainWindowService:
    return MainWindowService()


def test_width_and_height_subtract_the_shadow_margin(service):
    service._surface_width = 1280
    service._surface_height = 720
    service._shadow_margin = 64
    assert service.window_geometry_width == 1280 - 2 * 64
    assert service.window_geometry_height == 720 - 2 * 64


def test_width_and_height_equal_surface_without_margin(service):
    service._surface_width = 1280
    service._surface_height = 720
    service._shadow_margin = 0
    assert service.window_geometry_width == 1280
    assert service.window_geometry_height == 720


def test_pushed_margin_updates_shadow_margin_and_emits_window_geometry(qt_app, service, platform_service_stub):
    window = QWindow()
    window.resize(1280, 720)
    service.initialize(window)

    margins: list[int] = []
    widths: list[int] = []
    heights: list[int] = []
    service.shadow_margin_changed.connect(margins.append)
    service.window_geometry_width_changed.connect(widths.append)
    service.window_geometry_height_changed.connect(heights.append)

    platform_service_stub.shadow_margin_changed.emit(88)

    assert service.shadow_margin == 88
    assert margins == [88]
    assert widths == [1280 - 2 * 88]
    assert heights == [720 - 2 * 88]


def test_pushed_unchanged_margin_emits_nothing(qt_app, service, platform_service_stub, make_spy):
    window = QWindow()
    window.resize(1280, 720)
    service.initialize(window)

    margin_spy = make_spy(service.shadow_margin_changed)
    width_spy = make_spy(service.window_geometry_width_changed)

    platform_service_stub.shadow_margin_changed.emit(0)

    assert service.shadow_margin == 0
    assert margin_spy.count() == 0
    assert width_spy.count() == 0


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
def test_initialize_broadcasts_window_geometry(case, qt_app, service, platform_service_stub, make_spy):
    platform_service_stub.shadow_margin.return_value = case.shadow_margin

    window = QWindow()
    window.resize(1280, 720)

    width_spy = make_spy(service.window_geometry_width_changed)
    height_spy = make_spy(service.window_geometry_height_changed)

    service.initialize(window)

    assert width_spy.count() >= 1
    assert height_spy.count() >= 1
    assert width_spy.at(width_spy.count() - 1, 0) == case.expected_width
    assert height_spy.at(height_spy.count() - 1, 0) == case.expected_height


def test_minimize_delegates_to_platform(qt_app, service, platform_service_stub):
    window = QWindow()
    service._window = window

    service.minimize()

    platform_service_stub.minimize.assert_called_once_with(window)


def test_show_maximized_delegates_to_platform(qt_app, service, platform_service_stub):
    window = QWindow()
    service._window = window

    service.show_maximized()

    platform_service_stub.maximize.assert_called_once_with(window)


def test_show_normal_delegates_to_platform(qt_app, service, platform_service_stub):
    window = QWindow()
    service._window = window

    service.show_normal()

    platform_service_stub.show_normal.assert_called_once_with(window)


def test_show_fullscreen_delegates_to_platform(qt_app, service, platform_service_stub):
    window = QWindow()
    service._window = window

    service.show_fullscreen()

    platform_service_stub.enter_fullscreen.assert_called_once_with(window)


def test_exit_fullscreen_delegates_to_platform(qt_app, service, platform_service_stub):
    window = QWindow()
    service._window = window

    service.exit_fullscreen()

    platform_service_stub.exit_fullscreen.assert_called_once_with(window)


def test_state_read_reports_platform_answers(qt_app, service, platform_service_stub):
    service._window = QWindow()

    platform_service_stub.read_state.return_value = WindowStateSnapshot(is_fullscreen=True, is_maximized=True)
    service._apply_window_state()
    assert service.is_fullscreen
    assert service.is_maximized

    platform_service_stub.read_state.return_value = WindowStateSnapshot(is_fullscreen=False, is_maximized=False)
    service._apply_window_state()
    assert not service.is_fullscreen
    assert not service.is_maximized


def test_unchanged_states_emit_nothing(qt_app, service, platform_service_stub, make_spy):
    service._window = QWindow()
    platform_service_stub.read_state.return_value = WindowStateSnapshot(is_fullscreen=True, is_maximized=True)

    fullscreen_spy = make_spy(service.is_fullscreen_changed)
    maximized_spy = make_spy(service.is_maximized_changed)

    service._apply_window_state()
    service._apply_window_state()

    assert fullscreen_spy.count() == 1
    assert maximized_spy.count() == 1


def test_exit_fullscreen_without_prior_enter_emits_nothing(qt_app, service, platform_service_stub, make_spy):
    service._window = QWindow()

    spy = make_spy(service.is_fullscreen_changed)

    service.exit_fullscreen()

    platform_service_stub.exit_fullscreen.assert_called_once()
    assert not service.is_fullscreen
    assert spy.count() == 0


def test_repeated_show_fullscreen_emits_once(qt_app, service, platform_service_stub, make_spy):
    service._window = QWindow()
    platform_service_stub.read_state.return_value = WindowStateSnapshot(is_fullscreen=True, is_maximized=False)

    spy = make_spy(service.is_fullscreen_changed)

    service.show_fullscreen()
    service.show_fullscreen()

    assert service.is_fullscreen
    assert spy.count() == 1


def test_position_only_change_updates_fullscreen_state(qt_app, service, platform_service_stub):
    window = QWindow()
    window.resize(1280, 720)
    service.initialize(window)

    platform_service_stub.read_state.return_value = WindowStateSnapshot(is_fullscreen=True, is_maximized=False)
    service.show_fullscreen()
    assert service.is_fullscreen

    # The OS moved the window off the monitor without resizing it (keyboard move)
    platform_service_stub.read_state.return_value = WindowStateSnapshot(is_fullscreen=False, is_maximized=False)
    window.xChanged.emit(50)

    assert not service.is_fullscreen


def test_on_width_changed_reports_window_geometry_width(qt_app, service):
    service._window = QWindow()
    service._shadow_margin = 64

    widths: list[int] = []
    service.window_geometry_width_changed.connect(widths.append)

    service._on_width_changed(1280)

    assert service.window_geometry_width == 1280 - 2 * 64
    assert widths == [1280 - 2 * 64]
