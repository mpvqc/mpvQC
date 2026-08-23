# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable, Generator
from typing import NamedTuple

import inject
import pytest
from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QGuiApplication, QWindow

from mpvqc.window.services import (
    MainWindowInputs,
    MainWindowProps,
    MainWindowService,
    PlatformService,
    SurfaceSnapshot,
    WindowStateSnapshot,
    derive_main_window_props,
)
from test.window.conftest import ReentrantWindowState

NO_OWN_FRAME = SurfaceSnapshot(draws_own_frame=False, drop_shadow_margin=0)
OWN_FRAME = SurfaceSnapshot(draws_own_frame=True, drop_shadow_margin=88)

FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT = 1920, 1080
RETIRED_WIDTH, RETIRED_HEIGHT = 1280, 720


@pytest.fixture
def platform_service(make_platform_service, window_state, surface, window_configurator) -> PlatformService:
    return make_platform_service(
        window_state=window_state,
        surface=surface,
        window_configuration=window_configurator,
    )


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, platform_service):
    def custom_bindings(binder: inject.Binder):
        binder.bind(PlatformService, platform_service)

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
            "draws_own_frame": make_spy(service.draws_own_frame_changed),
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
            name="no own frame leaves the geometry at the surface",
            inputs=MainWindowInputs(
                surface_width=1280,
                surface_height=720,
                surface=NO_OWN_FRAME,
                is_fullscreen=False,
                is_maximized=False,
                is_main_window_focused=True,
                display_zoom_factor=1.0,
            ),
            expected=MainWindowProps(
                draws_own_frame=False,
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
                surface=SurfaceSnapshot(draws_own_frame=True, drop_shadow_margin=64),
                is_fullscreen=False,
                is_maximized=False,
                is_main_window_focused=True,
                display_zoom_factor=1.0,
            ),
            expected=MainWindowProps(
                draws_own_frame=True,
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
            name="own frame without margin keeps the geometry at the surface",
            inputs=MainWindowInputs(
                surface_width=1280,
                surface_height=720,
                surface=SurfaceSnapshot(draws_own_frame=True, drop_shadow_margin=0),
                is_fullscreen=False,
                is_maximized=False,
                is_main_window_focused=True,
                display_zoom_factor=1.0,
            ),
            expected=MainWindowProps(
                draws_own_frame=True,
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
            name="zero surface before the window is bound derives zero geometry",
            inputs=MainWindowInputs(
                surface_width=0,
                surface_height=0,
                surface=NO_OWN_FRAME,
                is_fullscreen=False,
                is_maximized=False,
                is_main_window_focused=True,
                display_zoom_factor=1.0,
            ),
            expected=MainWindowProps(
                draws_own_frame=False,
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
                surface=NO_OWN_FRAME,
                is_fullscreen=True,
                is_maximized=True,
                is_main_window_focused=False,
                display_zoom_factor=1.0,
            ),
            expected=MainWindowProps(
                draws_own_frame=False,
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
                surface=OWN_FRAME,
                is_fullscreen=False,
                is_maximized=False,
                is_main_window_focused=True,
                display_zoom_factor=2.0,
            ),
            expected=MainWindowProps(
                draws_own_frame=True,
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
    assert not service.draws_own_frame
    assert service.drop_shadow_margin == 0
    assert service.window_geometry_width == 0
    assert service.window_geometry_height == 0
    assert not service.is_fullscreen
    assert not service.is_maximized
    assert service.is_main_window_focused
    assert service.display_zoom_factor == pytest.approx(1.0)


class InitialBroadcastCase(NamedTuple):
    name: str
    surface: SurfaceSnapshot
    expected_surface_emissions: int
    expected_width: int
    expected_height: int


@pytest.mark.parametrize(
    "case",
    [
        InitialBroadcastCase(
            name="with an own frame",
            surface=OWN_FRAME,
            expected_surface_emissions=1,
            expected_width=1280 - 2 * 88,
            expected_height=720 - 2 * 88,
        ),
        InitialBroadcastCase(
            name="without an own frame",
            surface=NO_OWN_FRAME,
            expected_surface_emissions=0,
            expected_width=1280,
            expected_height=720,
        ),
    ],
    ids=lambda case: case.name,
)
def test_initialize_broadcasts_what_the_first_read_changed(case, surface, service, window, spy_notifies):
    surface.snapshot = case.surface
    spies = spy_notifies(service)

    service.initialize(window)

    assert surface.reads == [window]
    # No window holds focus offscreen, so the first read takes focus off the zero snapshot.
    assert emissions(spies) == {
        "draws_own_frame": case.expected_surface_emissions,
        "drop_shadow_margin": case.expected_surface_emissions,
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
    assert service.draws_own_frame is case.surface.draws_own_frame
    assert service.drop_shadow_margin == case.surface.drop_shadow_margin


def test_initialize_emits_in_the_props_field_order(surface, window_state, service, window):
    surface.snapshot = OWN_FRAME
    window_state.state = WindowStateSnapshot(is_fullscreen=True, is_maximized=True)
    order: list[str] = []
    service.draws_own_frame_changed.connect(lambda _: order.append("draws_own_frame"))
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
        "draws_own_frame",
        "drop_shadow_margin",
        "window_geometry_width",
        "window_geometry_height",
        "is_fullscreen",
        "is_maximized",
        "is_main_window_focused",
    ]


def test_initialize_configures_the_window_on_the_platform(window_configurator, qt_app, service, window):
    service.initialize(window)

    assert window_configurator.configured == [(qt_app, window)]


def test_resize_emits_the_geometry_alone(initialized_service, window, spy_notifies):
    spies = spy_notifies(initialized_service)

    window.resize(1000, 500)

    assert emissions(spies) == {
        "draws_own_frame": 0,
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
    case, window_state, initialized_service, window, spy_notifies
):
    spies = spy_notifies(initialized_service)

    window_state.state = WindowStateSnapshot(is_fullscreen=True, is_maximized=False)
    case.resize(window)

    assert emissions(spies) == {
        "draws_own_frame": 0,
        "drop_shadow_margin": 0,
        "window_geometry_width": case.expected_width_emissions,
        "window_geometry_height": case.expected_height_emissions,
        "is_fullscreen": 1,
        "is_maximized": 0,
        "is_main_window_focused": 0,
        "display_zoom_factor": 0,
    }
    assert spies["is_fullscreen"].at(0, 0) is True


def test_pushed_surface_emits_the_frame_the_margin_and_the_geometry(surface, initialized_service, spy_notifies):
    spies = spy_notifies(initialized_service)

    surface.push(OWN_FRAME)

    assert emissions(spies) == {
        "draws_own_frame": 1,
        "drop_shadow_margin": 1,
        "window_geometry_width": 1,
        "window_geometry_height": 1,
        "is_fullscreen": 0,
        "is_maximized": 0,
        "is_main_window_focused": 0,
        "display_zoom_factor": 0,
    }
    assert spies["draws_own_frame"].at(0, 0) is True
    assert spies["drop_shadow_margin"].at(0, 0) == 88
    assert spies["window_geometry_width"].at(0, 0) == 1280 - 2 * 88
    assert spies["window_geometry_height"].at(0, 0) == 720 - 2 * 88
    assert initialized_service.draws_own_frame
    assert initialized_service.drop_shadow_margin == 88


def test_pushed_surface_that_only_flips_the_frame_emits_the_frame_alone(surface, initialized_service, spy_notifies):
    spies = spy_notifies(initialized_service)

    surface.push(SurfaceSnapshot(draws_own_frame=True, drop_shadow_margin=0))

    assert emissions(spies) == {
        "draws_own_frame": 1,
        "drop_shadow_margin": 0,
        "window_geometry_width": 0,
        "window_geometry_height": 0,
        "is_fullscreen": 0,
        "is_maximized": 0,
        "is_main_window_focused": 0,
        "display_zoom_factor": 0,
    }
    assert spies["draws_own_frame"].at(0, 0) is True


def test_pushed_unchanged_surface_stays_silent(surface, initialized_service, spy_notifies):
    spies = spy_notifies(initialized_service)

    surface.push(NO_OWN_FRAME)

    assert emissions(spies) == {
        "draws_own_frame": 0,
        "drop_shadow_margin": 0,
        "window_geometry_width": 0,
        "window_geometry_height": 0,
        "is_fullscreen": 0,
        "is_maximized": 0,
        "is_main_window_focused": 0,
        "display_zoom_factor": 0,
    }


def test_window_state_signal_emits_the_states_the_platform_reads(
    window_state, initialized_service, window, spy_notifies
):
    spies = spy_notifies(initialized_service)

    window_state.state = WindowStateSnapshot(is_fullscreen=True, is_maximized=True)
    window.windowStateChanged.emit(Qt.WindowState.WindowFullScreen)

    assert emissions(spies) == {
        "draws_own_frame": 0,
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


def test_position_signals_re_read_the_window_state(window_state, initialized_service, window, spy_notifies):
    spies = spy_notifies(initialized_service)

    window_state.state = WindowStateSnapshot(is_fullscreen=True, is_maximized=False)
    window.yChanged.emit(10)
    window_state.state = WindowStateSnapshot(is_fullscreen=False, is_maximized=False)
    window.xChanged.emit(50)

    assert emissions(spies) == {
        "draws_own_frame": 0,
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
    window_state, initialized_service, window, spy_notifies
):
    spies = spy_notifies(initialized_service)
    reads_before = len(window_state.reads)

    window.xChanged.emit(50)
    window.yChanged.emit(20)

    assert emissions(spies) == {
        "draws_own_frame": 0,
        "drop_shadow_margin": 0,
        "window_geometry_width": 0,
        "window_geometry_height": 0,
        "is_fullscreen": 0,
        "is_maximized": 0,
        "is_main_window_focused": 0,
        "display_zoom_factor": 0,
    }
    assert len(window_state.reads) == reads_before + 2


class ReentryCase(NamedTuple):
    name: str
    fire: Callable[[QWindow], None]


class TestReentrantStateRead:
    """Pins the read-before-replace ordering every fold that reads window state
    depends on: when a retire re-enters, hoisting the input read above the state
    read would settle the props on the pre-retire geometry.
    """

    @pytest.fixture
    def window_state(self) -> ReentrantWindowState:
        return ReentrantWindowState(
            state=WindowStateSnapshot(is_fullscreen=True, is_maximized=False),
            retired_state=WindowStateSnapshot(is_fullscreen=False, is_maximized=False),
            retired_size=(RETIRED_WIDTH, RETIRED_HEIGHT),
        )

    @pytest.fixture
    def window(self, qt_app) -> QWindow:
        window = QWindow()
        window.resize(FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT)
        return window

    @pytest.mark.parametrize(
        "case",
        [
            ReentryCase(name="window move", fire=lambda w: w.xChanged.emit(0)),
            ReentryCase(name="width snap", fire=lambda w: w.widthChanged.emit(RETIRED_WIDTH)),
            ReentryCase(name="height snap", fire=lambda w: w.heightChanged.emit(RETIRED_HEIGHT)),
        ],
        ids=lambda case: case.name,
    )
    def test_retire_mid_read_settles_on_the_nested_geometry(self, case, window_state, initialized_service, window):
        service = initialized_service
        assert service.is_fullscreen
        assert service.window_geometry_width == FULLSCREEN_WIDTH
        assert service.window_geometry_height == FULLSCREEN_HEIGHT

        window_state.armed = True
        reads_before = len(window_state.reads)
        case.fire(window)

        # The triggering fold's own read, plus the width and height folds the
        # retire's resize fired back into the service: the read re-entered.
        assert len(window_state.reads) - reads_before == 3
        assert not service.is_fullscreen
        assert service.window_geometry_width == RETIRED_WIDTH
        assert service.window_geometry_height == RETIRED_HEIGHT


def test_focus_window_signal_emits_the_focus_notify_alone(qt_app, initialized_service, window, spy_notifies):
    spies = spy_notifies(initialized_service)

    qt_app.focusWindowChanged.emit(window)

    assert emissions(spies) == {
        "draws_own_frame": 0,
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
        "draws_own_frame": 0,
        "drop_shadow_margin": 0,
        "window_geometry_width": 0,
        "window_geometry_height": 0,
        "is_fullscreen": 0,
        "is_maximized": 0,
        "is_main_window_focused": 0,
        "display_zoom_factor": 0,
    }
    assert initialized_service.display_zoom_factor == pytest.approx(1.0)


def test_props_swap_completes_before_the_first_emission(surface, initialized_service):
    service = initialized_service
    observed: list[tuple] = []

    # draws_own_frame_changed is the first notify the surface cycle emits, so a
    # swap after it would slip past an observer of any later one.
    service.draws_own_frame_changed.connect(
        lambda _: observed.append(
            (
                service.draws_own_frame,
                service.drop_shadow_margin,
                service.window_geometry_width,
                service.window_geometry_height,
                service.is_fullscreen,
                service.is_maximized,
                service.is_main_window_focused,
                service.display_zoom_factor,
            )
        )
    )

    surface.push(OWN_FRAME)

    assert observed == [(True, 88, 1280 - 2 * 88, 720 - 2 * 88, False, False, False, 1.0)]


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
def test_command_delegates_to_the_platform_with_the_bound_window(case, window_state, initialized_service, window):
    case.invoke(initialized_service)

    assert window_state.commands == [(case.platform_command, window)]


def test_show_fullscreen_reports_the_state_the_platform_reads(window_state, initialized_service, make_spy):
    window_state.state = WindowStateSnapshot(is_fullscreen=True, is_maximized=False)
    fullscreen_spy = make_spy(initialized_service.is_fullscreen_changed)
    maximized_spy = make_spy(initialized_service.is_maximized_changed)

    initialized_service.show_fullscreen()
    initialized_service.show_fullscreen()

    assert initialized_service.is_fullscreen
    assert fullscreen_spy.count() == 1
    assert fullscreen_spy.at(0, 0) is True
    assert maximized_spy.count() == 0


def test_exit_fullscreen_without_prior_enter_stays_silent(window_state, initialized_service, window, make_spy):
    spy = make_spy(initialized_service.is_fullscreen_changed)

    initialized_service.exit_fullscreen()

    assert window_state.commands == [("exit_fullscreen", window)]
    assert not initialized_service.is_fullscreen
    assert spy.count() == 0
