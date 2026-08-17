# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable
from typing import NamedTuple

import inject
import pytest
from PySide6.QtGui import QWindow

from mpvqc.window.services import MainWindowService, PlatformService, WindowStateSnapshot
from mpvqc.window.viewmodels import (
    MpvqcWindowControlsViewModel,
    WindowControlsInputs,
    WindowControlsProps,
    derive_window_controls_props,
)


@pytest.fixture
def main_window_service(qt_app) -> MainWindowService:
    return MainWindowService()


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, platform_service_stub, main_window_service):
    def custom_bindings(binder: inject.Binder):
        binder.bind(PlatformService, platform_service_stub)
        binder.bind(MainWindowService, main_window_service)

    common_bindings_with(custom_bindings)


@pytest.fixture
def window(qt_app) -> QWindow:
    window = QWindow()
    window.resize(1280, 720)
    return window


@pytest.fixture
def initialized_service(main_window_service, window) -> MainWindowService:
    main_window_service.initialize(window)
    return main_window_service


@pytest.fixture
def make_view_model():
    def _make() -> MpvqcWindowControlsViewModel:
        # noinspection PyCallingNonCallable
        return MpvqcWindowControlsViewModel()

    return _make


@pytest.fixture
def spy_notifies(make_spy):
    def _spy(view_model: MpvqcWindowControlsViewModel) -> dict:
        return {
            "windowGeometryWidth": make_spy(view_model.windowGeometryWidthChanged),
            "windowGeometryHeight": make_spy(view_model.windowGeometryHeightChanged),
            "isFullscreen": make_spy(view_model.isFullscreenChanged),
            "isMaximized": make_spy(view_model.isMaximizedChanged),
            "dropShadowMargin": make_spy(view_model.dropShadowMarginChanged),
            "radius": make_spy(view_model.radiusChanged),
            "isMainWindowFocused": make_spy(view_model.isMainWindowFocusedChanged),
        }

    return _spy


def emissions(spies: dict) -> dict[str, int]:
    return {name: spy.count() for name, spy in spies.items()}


class DerivationCase(NamedTuple):
    name: str
    inputs: WindowControlsInputs
    expected: WindowControlsProps


@pytest.mark.parametrize(
    "case",
    [
        DerivationCase(
            name="no margin keeps the radius off",
            inputs=WindowControlsInputs(
                window_geometry_width=1280,
                window_geometry_height=720,
                is_fullscreen=False,
                is_maximized=False,
                drop_shadow_margin=0,
                is_main_window_focused=True,
                keeps_native_frame=False,
                draws_drop_shadow=True,
            ),
            expected=WindowControlsProps(
                window_geometry_width=1280,
                window_geometry_height=720,
                is_fullscreen=False,
                is_maximized=False,
                drop_shadow_margin=0,
                radius=0,
                is_main_window_focused=True,
                keeps_native_frame=False,
                draws_drop_shadow=True,
            ),
        ),
        DerivationCase(
            name="hairline margin turns the radius on",
            inputs=WindowControlsInputs(
                window_geometry_width=1280,
                window_geometry_height=720,
                is_fullscreen=False,
                is_maximized=False,
                drop_shadow_margin=1,
                is_main_window_focused=True,
                keeps_native_frame=False,
                draws_drop_shadow=True,
            ),
            expected=WindowControlsProps(
                window_geometry_width=1280,
                window_geometry_height=720,
                is_fullscreen=False,
                is_maximized=False,
                drop_shadow_margin=1,
                radius=8,
                is_main_window_focused=True,
                keeps_native_frame=False,
                draws_drop_shadow=True,
            ),
        ),
        DerivationCase(
            name="wide margin keeps the radius fixed",
            inputs=WindowControlsInputs(
                window_geometry_width=1104,
                window_geometry_height=544,
                is_fullscreen=False,
                is_maximized=False,
                drop_shadow_margin=88,
                is_main_window_focused=True,
                keeps_native_frame=False,
                draws_drop_shadow=True,
            ),
            expected=WindowControlsProps(
                window_geometry_width=1104,
                window_geometry_height=544,
                is_fullscreen=False,
                is_maximized=False,
                drop_shadow_margin=88,
                radius=8,
                is_main_window_focused=True,
                keeps_native_frame=False,
                draws_drop_shadow=True,
            ),
        ),
        DerivationCase(
            name="window states and platform flags pass through",
            inputs=WindowControlsInputs(
                window_geometry_width=640,
                window_geometry_height=480,
                is_fullscreen=True,
                is_maximized=True,
                drop_shadow_margin=0,
                is_main_window_focused=False,
                keeps_native_frame=True,
                draws_drop_shadow=False,
            ),
            expected=WindowControlsProps(
                window_geometry_width=640,
                window_geometry_height=480,
                is_fullscreen=True,
                is_maximized=True,
                drop_shadow_margin=0,
                radius=0,
                is_main_window_focused=False,
                keeps_native_frame=True,
                draws_drop_shadow=False,
            ),
        ),
    ],
    ids=lambda case: case.name,
)
def test_derivation(case: DerivationCase):
    assert derive_window_controls_props(case.inputs) == case.expected


def test_initial_snapshot_reads_the_main_window_at_construction(
    platform_service_stub, main_window_service, window, make_view_model
):
    platform_service_stub.drop_shadow_margin.return_value = 88
    main_window_service.initialize(window)

    view_model = make_view_model()

    assert view_model.windowGeometryWidth == 1280 - 2 * 88
    assert view_model.windowGeometryHeight == 720 - 2 * 88
    assert view_model.dropShadowMargin == 88
    assert view_model.radius == 8
    assert not view_model.isFullscreen
    assert not view_model.isMaximized
    assert not view_model.isMainWindowFocused


def test_pushed_margin_emits_margin_radius_and_geometry(
    platform_service_stub, initialized_service, make_view_model, spy_notifies
):
    view_model = make_view_model()
    spies = spy_notifies(view_model)

    platform_service_stub.drop_shadow_margin_changed.emit(88)

    assert emissions(spies) == {
        "windowGeometryWidth": 1,
        "windowGeometryHeight": 1,
        "isFullscreen": 0,
        "isMaximized": 0,
        "dropShadowMargin": 1,
        "radius": 1,
        "isMainWindowFocused": 0,
    }
    assert spies["dropShadowMargin"].at(0, 0) == 88
    assert spies["radius"].at(0, 0) == 8
    assert spies["windowGeometryWidth"].at(0, 0) == 1280 - 2 * 88
    assert spies["windowGeometryHeight"].at(0, 0) == 720 - 2 * 88


def test_margin_move_with_the_radius_already_on_keeps_the_radius_silent(
    platform_service_stub, initialized_service, make_view_model, spy_notifies
):
    platform_service_stub.drop_shadow_margin_changed.emit(88)
    view_model = make_view_model()
    spies = spy_notifies(view_model)

    platform_service_stub.drop_shadow_margin_changed.emit(64)

    assert emissions(spies) == {
        "windowGeometryWidth": 1,
        "windowGeometryHeight": 1,
        "isFullscreen": 0,
        "isMaximized": 0,
        "dropShadowMargin": 1,
        "radius": 0,
        "isMainWindowFocused": 0,
    }
    assert spies["dropShadowMargin"].at(0, 0) == 64
    assert view_model.radius == 8


def test_fullscreen_state_change_emits_the_fullscreen_notify_alone(
    platform_service_stub, initialized_service, window, make_view_model, spy_notifies
):
    view_model = make_view_model()
    spies = spy_notifies(view_model)

    platform_service_stub.read_state.return_value = WindowStateSnapshot(is_fullscreen=True, is_maximized=False)
    window.xChanged.emit(50)

    assert emissions(spies) == {
        "windowGeometryWidth": 0,
        "windowGeometryHeight": 0,
        "isFullscreen": 1,
        "isMaximized": 0,
        "dropShadowMargin": 0,
        "radius": 0,
        "isMainWindowFocused": 0,
    }
    assert spies["isFullscreen"].at(0, 0) is True


def test_maximize_state_change_emits_the_maximize_notify_alone(
    platform_service_stub, initialized_service, window, make_view_model, spy_notifies
):
    view_model = make_view_model()
    spies = spy_notifies(view_model)

    platform_service_stub.read_state.return_value = WindowStateSnapshot(is_fullscreen=False, is_maximized=True)
    window.xChanged.emit(50)

    assert emissions(spies) == {
        "windowGeometryWidth": 0,
        "windowGeometryHeight": 0,
        "isFullscreen": 0,
        "isMaximized": 1,
        "dropShadowMargin": 0,
        "radius": 0,
        "isMainWindowFocused": 0,
    }
    assert spies["isMaximized"].at(0, 0) is True


def test_margin_drop_to_zero_turns_the_radius_off(
    platform_service_stub, initialized_service, make_view_model, spy_notifies
):
    platform_service_stub.drop_shadow_margin_changed.emit(88)
    view_model = make_view_model()
    spies = spy_notifies(view_model)

    platform_service_stub.drop_shadow_margin_changed.emit(0)

    assert emissions(spies) == {
        "windowGeometryWidth": 1,
        "windowGeometryHeight": 1,
        "isFullscreen": 0,
        "isMaximized": 0,
        "dropShadowMargin": 1,
        "radius": 1,
        "isMainWindowFocused": 0,
    }
    assert spies["dropShadowMargin"].at(0, 0) == 0
    assert spies["radius"].at(0, 0) == 0
    assert spies["windowGeometryWidth"].at(0, 0) == 1280
    assert spies["windowGeometryHeight"].at(0, 0) == 720


def test_focus_change_emits_the_focus_notify_alone(qt_app, initialized_service, window, make_view_model, spy_notifies):
    view_model = make_view_model()
    spies = spy_notifies(view_model)

    qt_app.focusWindowChanged.emit(window)

    assert emissions(spies) == {
        "windowGeometryWidth": 0,
        "windowGeometryHeight": 0,
        "isFullscreen": 0,
        "isMaximized": 0,
        "dropShadowMargin": 0,
        "radius": 0,
        "isMainWindowFocused": 1,
    }
    assert spies["isMainWindowFocused"].at(0, 0) is True


def test_props_swap_completes_before_the_first_emission(platform_service_stub, initialized_service, make_view_model):
    view_model = make_view_model()
    observed: list[tuple[int, int]] = []

    # dropShadowMarginChanged is the first notify the margin cycle emits, so a
    # swap after it would slip past an observer of any later one.
    view_model.dropShadowMarginChanged.connect(
        lambda _: observed.append((view_model.dropShadowMargin, view_model.radius))
    )

    platform_service_stub.drop_shadow_margin_changed.emit(88)

    assert observed == [(88, 8)]


def test_platform_flags_forward(platform_service_stub, initialized_service, make_view_model):
    view_model = make_view_model()

    assert view_model.keepsNativeFrame is False
    assert view_model.drawsDropShadow is True


class CommandCase(NamedTuple):
    tag: str
    is_fullscreen: bool
    is_maximized: bool
    invoke: Callable[[MpvqcWindowControlsViewModel], None]
    expected_command: str | None


@pytest.mark.parametrize(
    "case",
    [
        CommandCase(
            tag="minimize",
            is_fullscreen=False,
            is_maximized=False,
            invoke=lambda vm: vm.minimize(),
            expected_command="minimize",
        ),
        CommandCase(
            tag="not maximized -> maximize",
            is_fullscreen=False,
            is_maximized=False,
            invoke=lambda vm: vm.toggleMaximized(),
            expected_command="maximize",
        ),
        CommandCase(
            tag="maximized -> normal",
            is_fullscreen=False,
            is_maximized=True,
            invoke=lambda vm: vm.toggleMaximized(),
            expected_command="show_normal",
        ),
        CommandCase(
            tag="not fullscreen -> fullscreen",
            is_fullscreen=False,
            is_maximized=False,
            invoke=lambda vm: vm.toggleFullScreen(),
            expected_command="enter_fullscreen",
        ),
        CommandCase(
            tag="fullscreen -> exit fullscreen",
            is_fullscreen=True,
            is_maximized=False,
            invoke=lambda vm: vm.toggleFullScreen(),
            expected_command="exit_fullscreen",
        ),
        CommandCase(
            tag="fullscreen -> disable fullscreen",
            is_fullscreen=True,
            is_maximized=False,
            invoke=lambda vm: vm.disableFullScreen(),
            expected_command="exit_fullscreen",
        ),
        CommandCase(
            tag="windowed -> disable fullscreen does nothing",
            is_fullscreen=False,
            is_maximized=False,
            invoke=lambda vm: vm.disableFullScreen(),
            expected_command=None,
        ),
    ],
    ids=lambda case: case.tag,
)
def test_command_delegates_to_the_platform(
    platform_service_stub, initialized_service, window, make_view_model, case: CommandCase
):
    platform_service_stub.read_state.return_value = WindowStateSnapshot(
        is_fullscreen=case.is_fullscreen, is_maximized=case.is_maximized
    )
    window.xChanged.emit(1)
    view_model = make_view_model()

    case.invoke(view_model)

    command_mocks = {
        "minimize": platform_service_stub.minimize,
        "maximize": platform_service_stub.maximize,
        "show_normal": platform_service_stub.show_normal,
        "enter_fullscreen": platform_service_stub.enter_fullscreen,
        "exit_fullscreen": platform_service_stub.exit_fullscreen,
    }
    expected = {name: (1 if name == case.expected_command else 0) for name in command_mocks}
    assert {name: mock.call_count for name, mock in command_mocks.items()} == expected
