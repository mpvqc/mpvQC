# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable, Generator
from typing import NamedTuple
from unittest.mock import MagicMock

import inject
import pytest
from PySide6.QtCore import QEvent, QObject, Qt, Signal
from PySide6.QtGui import QGuiApplication, QWindow

from mpvqc.window.services import (
    MainWindowInputs,
    MainWindowProps,
    MainWindowService,
    PlatformService,
    WindowStateSnapshot,
    derive_main_window_props,
)


class PlatformServiceStub(QObject):
    """Carries a real drop_shadow_margin_changed signal so tests can drive pushes;
    everything else is a mock."""

    drop_shadow_margin_changed = Signal(int)

    def __init__(self) -> None:
        super().__init__()
        self.read_state = MagicMock(return_value=WindowStateSnapshot(is_fullscreen=False, is_maximized=False))
        self.drop_shadow_margin = MagicMock(return_value=0)
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
def service(qt_app) -> MainWindowService:
    return MainWindowService()


@pytest.fixture
def window(qt_app) -> QWindow:
    window = QWindow()
    window.resize(1280, 720)
    return window


@pytest.fixture
def initialized_service(service, window) -> MainWindowService:
    service.initialize(window)
    return service


@pytest.fixture
def spy_notifies(make_spy):
    def _spy(service: MainWindowService) -> dict:
        return {
            "drop_shadow_margin": make_spy(service.drop_shadow_margin_changed),
            "window_geometry_width": make_spy(service.window_geometry_width_changed),
            "window_geometry_height": make_spy(service.window_geometry_height_changed),
            "is_fullscreen": make_spy(service.is_fullscreen_changed),
            "is_maximized": make_spy(service.is_maximized_changed),
            "is_main_window_focused": make_spy(service.is_main_window_focused_changed),
            "display_zoom_factor": make_spy(service.display_zoom_factor_changed),
        }

    return _spy


def emissions(spies: dict) -> dict[str, int]:
    return {name: spy.count() for name, spy in spies.items()}


class DerivationCase(NamedTuple):
    name: str
    inputs: MainWindowInputs
    expected: MainWindowProps


@pytest.mark.parametrize(
    "case",
    [
        DerivationCase(
            name="no margin leaves the geometry at the surface",
            inputs=MainWindowInputs(
                surface_width=1280,
                surface_height=720,
                drop_shadow_margin=0,
                is_fullscreen=False,
                is_maximized=False,
                is_main_window_focused=True,
                display_zoom_factor=1.0,
            ),
            expected=MainWindowProps(
                drop_shadow_margin=0,
                window_geometry_width=1280,
                window_geometry_height=720,
                is_fullscreen=False,
                is_maximized=False,
                is_main_window_focused=True,
                display_zoom_factor=1.0,
            ),
        ),
        DerivationCase(
            name="margin comes off both sides of the surface",
            inputs=MainWindowInputs(
                surface_width=1280,
                surface_height=720,
                drop_shadow_margin=64,
                is_fullscreen=False,
                is_maximized=False,
                is_main_window_focused=True,
                display_zoom_factor=1.0,
            ),
            expected=MainWindowProps(
                drop_shadow_margin=64,
                window_geometry_width=1152,
                window_geometry_height=592,
                is_fullscreen=False,
                is_maximized=False,
                is_main_window_focused=True,
                display_zoom_factor=1.0,
            ),
        ),
        DerivationCase(
            name="zero surface before the window is bound derives zero geometry",
            inputs=MainWindowInputs(
                surface_width=0,
                surface_height=0,
                drop_shadow_margin=0,
                is_fullscreen=False,
                is_maximized=False,
                is_main_window_focused=True,
                display_zoom_factor=1.0,
            ),
            expected=MainWindowProps(
                drop_shadow_margin=0,
                window_geometry_width=0,
                window_geometry_height=0,
                is_fullscreen=False,
                is_maximized=False,
                is_main_window_focused=True,
                display_zoom_factor=1.0,
            ),
        ),
        DerivationCase(
            name="window states and focus pass through",
            inputs=MainWindowInputs(
                surface_width=640,
                surface_height=480,
                drop_shadow_margin=0,
                is_fullscreen=True,
                is_maximized=True,
                is_main_window_focused=False,
                display_zoom_factor=1.0,
            ),
            expected=MainWindowProps(
                drop_shadow_margin=0,
                window_geometry_width=640,
                window_geometry_height=480,
                is_fullscreen=True,
                is_maximized=True,
                is_main_window_focused=False,
                display_zoom_factor=1.0,
            ),
        ),
        DerivationCase(
            name="display zoom passes through untouched by the margin",
            inputs=MainWindowInputs(
                surface_width=1280,
                surface_height=720,
                drop_shadow_margin=88,
                is_fullscreen=False,
                is_maximized=False,
                is_main_window_focused=True,
                display_zoom_factor=2.0,
            ),
            expected=MainWindowProps(
                drop_shadow_margin=88,
                window_geometry_width=1104,
                window_geometry_height=544,
                is_fullscreen=False,
                is_maximized=False,
                is_main_window_focused=True,
                display_zoom_factor=2.0,
            ),
        ),
    ],
    ids=lambda case: case.name,
)
def test_derivation(case: DerivationCase):
    assert derive_main_window_props(case.inputs) == case.expected


def test_unbound_service_reports_the_zero_snapshot(service):
    assert service.window_geometry_width == 0
    assert service.window_geometry_height == 0
    assert service.drop_shadow_margin == 0
    assert not service.is_fullscreen
    assert not service.is_maximized
    assert service.is_main_window_focused
    assert service.display_zoom_factor == pytest.approx(1.0)


class InitialBroadcastCase(NamedTuple):
    name: str
    drop_shadow_margin: int
    expected_margin_emissions: int
    expected_width: int
    expected_height: int


@pytest.mark.parametrize(
    "case",
    [
        InitialBroadcastCase(
            name="with drop shadow margin",
            drop_shadow_margin=88,
            expected_margin_emissions=1,
            expected_width=1280 - 2 * 88,
            expected_height=720 - 2 * 88,
        ),
        InitialBroadcastCase(
            name="without drop shadow margin",
            drop_shadow_margin=0,
            expected_margin_emissions=0,
            expected_width=1280,
            expected_height=720,
        ),
    ],
    ids=lambda case: case.name,
)
def test_initialize_broadcasts_what_the_first_read_changed(case, platform_service_stub, service, window, spy_notifies):
    platform_service_stub.drop_shadow_margin.return_value = case.drop_shadow_margin
    spies = spy_notifies(service)

    service.initialize(window)

    # No window holds focus offscreen, so the first read takes focus off the zero snapshot.
    assert emissions(spies) == {
        "drop_shadow_margin": case.expected_margin_emissions,
        "window_geometry_width": 1,
        "window_geometry_height": 1,
        "is_fullscreen": 0,
        "is_maximized": 0,
        "is_main_window_focused": 1,
        "display_zoom_factor": 0,
    }
    assert spies["window_geometry_width"].at(0, 0) == case.expected_width
    assert spies["window_geometry_height"].at(0, 0) == case.expected_height
    assert spies["is_main_window_focused"].at(0, 0) is False
    assert service.drop_shadow_margin == case.drop_shadow_margin


def test_initialize_emits_in_the_props_field_order(platform_service_stub, service, window):
    platform_service_stub.drop_shadow_margin.return_value = 88
    platform_service_stub.read_state.return_value = WindowStateSnapshot(is_fullscreen=True, is_maximized=True)
    order: list[str] = []
    service.drop_shadow_margin_changed.connect(lambda _: order.append("drop_shadow_margin"))
    service.window_geometry_width_changed.connect(lambda _: order.append("window_geometry_width"))
    service.window_geometry_height_changed.connect(lambda _: order.append("window_geometry_height"))
    service.is_fullscreen_changed.connect(lambda _: order.append("is_fullscreen"))
    service.is_maximized_changed.connect(lambda _: order.append("is_maximized"))
    service.is_main_window_focused_changed.connect(lambda _: order.append("is_main_window_focused"))
    service.display_zoom_factor_changed.connect(lambda _: order.append("display_zoom_factor"))

    service.initialize(window)

    # Offscreen the device pixel ratio cannot leave 1.0, so the zoom notify has nothing to emit.
    assert order == [
        "drop_shadow_margin",
        "window_geometry_width",
        "window_geometry_height",
        "is_fullscreen",
        "is_maximized",
        "is_main_window_focused",
    ]


def test_initialize_configures_the_window_on_the_platform(platform_service_stub, qt_app, service, window):
    service.initialize(window)

    platform_service_stub.configure_window.assert_called_once_with(qt_app, window)


def test_resize_emits_the_geometry_alone(initialized_service, window, spy_notifies):
    spies = spy_notifies(initialized_service)

    window.resize(1000, 500)

    assert emissions(spies) == {
        "drop_shadow_margin": 0,
        "window_geometry_width": 1,
        "window_geometry_height": 1,
        "is_fullscreen": 0,
        "is_maximized": 0,
        "is_main_window_focused": 0,
        "display_zoom_factor": 0,
    }
    assert spies["window_geometry_width"].at(0, 0) == 1000
    assert spies["window_geometry_height"].at(0, 0) == 500


class ResizeCase(NamedTuple):
    name: str
    resize: Callable[[QWindow], None]
    expected_width_emissions: int
    expected_height_emissions: int


@pytest.mark.parametrize(
    "case",
    [
        ResizeCase(
            name="width",
            resize=lambda window: window.setWidth(1000),
            expected_width_emissions=1,
            expected_height_emissions=0,
        ),
        ResizeCase(
            name="height",
            resize=lambda window: window.setHeight(500),
            expected_width_emissions=0,
            expected_height_emissions=1,
        ),
    ],
    ids=lambda case: case.name,
)
def test_resize_re_reads_the_window_state_in_the_same_cycle(
    case, platform_service_stub, initialized_service, window, spy_notifies
):
    spies = spy_notifies(initialized_service)

    platform_service_stub.read_state.return_value = WindowStateSnapshot(is_fullscreen=True, is_maximized=False)
    case.resize(window)

    assert emissions(spies) == {
        "drop_shadow_margin": 0,
        "window_geometry_width": case.expected_width_emissions,
        "window_geometry_height": case.expected_height_emissions,
        "is_fullscreen": 1,
        "is_maximized": 0,
        "is_main_window_focused": 0,
        "display_zoom_factor": 0,
    }
    assert spies["is_fullscreen"].at(0, 0) is True


def test_pushed_margin_emits_margin_and_geometry(platform_service_stub, initialized_service, spy_notifies):
    spies = spy_notifies(initialized_service)

    platform_service_stub.drop_shadow_margin_changed.emit(88)

    assert emissions(spies) == {
        "drop_shadow_margin": 1,
        "window_geometry_width": 1,
        "window_geometry_height": 1,
        "is_fullscreen": 0,
        "is_maximized": 0,
        "is_main_window_focused": 0,
        "display_zoom_factor": 0,
    }
    assert spies["drop_shadow_margin"].at(0, 0) == 88
    assert spies["window_geometry_width"].at(0, 0) == 1280 - 2 * 88
    assert spies["window_geometry_height"].at(0, 0) == 720 - 2 * 88
    assert initialized_service.drop_shadow_margin == 88


def test_pushed_unchanged_margin_stays_silent(platform_service_stub, initialized_service, spy_notifies):
    spies = spy_notifies(initialized_service)

    platform_service_stub.drop_shadow_margin_changed.emit(0)

    assert emissions(spies) == {
        "drop_shadow_margin": 0,
        "window_geometry_width": 0,
        "window_geometry_height": 0,
        "is_fullscreen": 0,
        "is_maximized": 0,
        "is_main_window_focused": 0,
        "display_zoom_factor": 0,
    }


def test_window_state_signal_emits_the_states_the_platform_reads(
    platform_service_stub, initialized_service, window, spy_notifies
):
    spies = spy_notifies(initialized_service)

    platform_service_stub.read_state.return_value = WindowStateSnapshot(is_fullscreen=True, is_maximized=True)
    window.windowStateChanged.emit(Qt.WindowState.WindowFullScreen)

    assert emissions(spies) == {
        "drop_shadow_margin": 0,
        "window_geometry_width": 0,
        "window_geometry_height": 0,
        "is_fullscreen": 1,
        "is_maximized": 1,
        "is_main_window_focused": 0,
        "display_zoom_factor": 0,
    }
    assert spies["is_fullscreen"].at(0, 0) is True
    assert spies["is_maximized"].at(0, 0) is True
    assert initialized_service.is_fullscreen
    assert initialized_service.is_maximized


def test_position_signals_re_read_the_window_state(platform_service_stub, initialized_service, window, spy_notifies):
    spies = spy_notifies(initialized_service)

    platform_service_stub.read_state.return_value = WindowStateSnapshot(is_fullscreen=True, is_maximized=False)
    window.yChanged.emit(10)
    platform_service_stub.read_state.return_value = WindowStateSnapshot(is_fullscreen=False, is_maximized=False)
    window.xChanged.emit(50)

    assert emissions(spies) == {
        "drop_shadow_margin": 0,
        "window_geometry_width": 0,
        "window_geometry_height": 0,
        "is_fullscreen": 2,
        "is_maximized": 0,
        "is_main_window_focused": 0,
        "display_zoom_factor": 0,
    }
    assert spies["is_fullscreen"].at(0, 0) is True
    assert spies["is_fullscreen"].at(1, 0) is False
    assert not initialized_service.is_fullscreen


def test_move_with_unchanged_state_stays_silent_but_still_reads_the_state(
    platform_service_stub, initialized_service, window, spy_notifies
):
    spies = spy_notifies(initialized_service)
    reads_before = platform_service_stub.read_state.call_count

    window.xChanged.emit(50)
    window.yChanged.emit(20)

    assert emissions(spies) == {
        "drop_shadow_margin": 0,
        "window_geometry_width": 0,
        "window_geometry_height": 0,
        "is_fullscreen": 0,
        "is_maximized": 0,
        "is_main_window_focused": 0,
        "display_zoom_factor": 0,
    }
    assert platform_service_stub.read_state.call_count == reads_before + 2


def test_focus_window_signal_emits_the_focus_notify_alone(qt_app, initialized_service, window, spy_notifies):
    spies = spy_notifies(initialized_service)

    qt_app.focusWindowChanged.emit(window)

    assert emissions(spies) == {
        "drop_shadow_margin": 0,
        "window_geometry_width": 0,
        "window_geometry_height": 0,
        "is_fullscreen": 0,
        "is_maximized": 0,
        "is_main_window_focused": 1,
        "display_zoom_factor": 0,
    }
    assert spies["is_main_window_focused"].at(0, 0) is True
    assert initialized_service.is_main_window_focused


@pytest.fixture
def other_window(qt_app) -> Generator[QWindow]:
    other = QWindow()
    yield other
    other.destroy()


def _shown(other: QWindow) -> QWindow:
    other.setVisible(True)
    return other


class FocusCase(NamedTuple):
    name: str
    focused: Callable[[QWindow, QWindow], QWindow | None]
    expected_emissions: int
    expected_focused: bool


@pytest.mark.parametrize(
    "case",
    [
        FocusCase(
            name="focus leaving every window unfocuses",
            focused=lambda main, other: None,
            expected_emissions=1,
            expected_focused=False,
        ),
        FocusCase(
            name="focus on a window not yet shown keeps the main window focused",
            focused=lambda main, other: other,
            expected_emissions=0,
            expected_focused=True,
        ),
        FocusCase(
            name="focus on a shown window unfocuses",
            focused=lambda main, other: _shown(other),
            expected_emissions=1,
            expected_focused=False,
        ),
        FocusCase(
            name="focus staying on the main window stays silent",
            focused=lambda main, other: main,
            expected_emissions=0,
            expected_focused=True,
        ),
    ],
    ids=lambda case: case.name,
)
def test_focus_folds_to_the_one_bool_the_service_reports(
    case, qt_app, initialized_service, window, other_window, make_spy
):
    qt_app.focusWindowChanged.emit(window)
    spy = make_spy(initialized_service.is_main_window_focused_changed)

    qt_app.focusWindowChanged.emit(case.focused(window, other_window))

    assert spy.count() == case.expected_emissions
    assert initialized_service.is_main_window_focused is case.expected_focused


def test_unchanged_device_pixel_ratio_stays_silent(initialized_service, window, spy_notifies):
    spies = spy_notifies(initialized_service)

    QGuiApplication.sendEvent(window, QEvent(QEvent.Type.DevicePixelRatioChange))

    assert emissions(spies) == {
        "drop_shadow_margin": 0,
        "window_geometry_width": 0,
        "window_geometry_height": 0,
        "is_fullscreen": 0,
        "is_maximized": 0,
        "is_main_window_focused": 0,
        "display_zoom_factor": 0,
    }
    assert initialized_service.display_zoom_factor == pytest.approx(1.0)


def test_props_swap_completes_before_the_first_emission(platform_service_stub, initialized_service):
    service = initialized_service
    observed: list[tuple] = []

    # drop_shadow_margin_changed is the first notify the margin cycle emits, so a
    # swap after it would slip past an observer of any later one.
    service.drop_shadow_margin_changed.connect(
        lambda _: observed.append(
            (
                service.window_geometry_width,
                service.window_geometry_height,
                service.drop_shadow_margin,
                service.is_fullscreen,
                service.is_maximized,
                service.is_main_window_focused,
                service.display_zoom_factor,
            )
        )
    )

    platform_service_stub.drop_shadow_margin_changed.emit(88)

    assert observed == [(1280 - 2 * 88, 720 - 2 * 88, 88, False, False, False, 1.0)]


class CommandCase(NamedTuple):
    name: str
    invoke: Callable[[MainWindowService], None]
    platform_command: str


@pytest.mark.parametrize(
    "case",
    [
        CommandCase(name="minimize", invoke=lambda s: s.minimize(), platform_command="minimize"),
        CommandCase(name="show_maximized", invoke=lambda s: s.show_maximized(), platform_command="maximize"),
        CommandCase(name="show_normal", invoke=lambda s: s.show_normal(), platform_command="show_normal"),
        CommandCase(name="show_fullscreen", invoke=lambda s: s.show_fullscreen(), platform_command="enter_fullscreen"),
        CommandCase(name="exit_fullscreen", invoke=lambda s: s.exit_fullscreen(), platform_command="exit_fullscreen"),
    ],
    ids=lambda case: case.name,
)
def test_command_delegates_to_the_platform_with_the_bound_window(
    case, platform_service_stub, initialized_service, window
):
    command_mocks = {
        "minimize": platform_service_stub.minimize,
        "maximize": platform_service_stub.maximize,
        "show_normal": platform_service_stub.show_normal,
        "enter_fullscreen": platform_service_stub.enter_fullscreen,
        "exit_fullscreen": platform_service_stub.exit_fullscreen,
    }

    case.invoke(initialized_service)

    expected = {name: (1 if name == case.platform_command else 0) for name in command_mocks}
    assert {name: mock.call_count for name, mock in command_mocks.items()} == expected
    command_mocks[case.platform_command].assert_called_once_with(window)


def test_show_fullscreen_reports_the_state_the_platform_reads(platform_service_stub, initialized_service, make_spy):
    platform_service_stub.read_state.return_value = WindowStateSnapshot(is_fullscreen=True, is_maximized=False)
    fullscreen_spy = make_spy(initialized_service.is_fullscreen_changed)
    maximized_spy = make_spy(initialized_service.is_maximized_changed)

    initialized_service.show_fullscreen()
    initialized_service.show_fullscreen()

    assert initialized_service.is_fullscreen
    assert fullscreen_spy.count() == 1
    assert fullscreen_spy.at(0, 0) is True
    assert maximized_spy.count() == 0


def test_exit_fullscreen_without_prior_enter_stays_silent(platform_service_stub, initialized_service, make_spy):
    spy = make_spy(initialized_service.is_fullscreen_changed)

    initialized_service.exit_fullscreen()

    platform_service_stub.exit_fullscreen.assert_called_once()
    assert not initialized_service.is_fullscreen
    assert spy.count() == 0
