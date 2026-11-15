# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TYPE_CHECKING, NamedTuple

import pytest
from PySide6.QtGui import QWindow

from mpvqc.window.services import MainWindowService, PlatformService, SurfaceSnapshot, WindowStateSnapshot
from mpvqc.window.viewmodels import MpvqcWindowControlsViewModel

if TYPE_CHECKING:
    from collections.abc import Callable

    import inject

NO_OWN_FRAME = SurfaceSnapshot(draws_own_frame=False, drop_shadow_margin=0)
OWN_FRAME = SurfaceSnapshot(draws_own_frame=True, drop_shadow_margin=88)


@pytest.fixture
def main_window_service(qt_app) -> MainWindowService:
    return MainWindowService()


@pytest.fixture
def platform_service(make_platform_service, window_state, surface) -> PlatformService:
    return make_platform_service(window_state=window_state, surface=surface)


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, platform_service, main_window_service):
    def custom_bindings(binder: inject.Binder):
        binder.bind(PlatformService, platform_service)
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


def test_properties_read_the_main_window(surface, main_window_service, window, make_view_model):
    surface.snapshot = OWN_FRAME
    main_window_service.initialize(window)

    view_model = make_view_model()

    assert view_model.windowGeometryWidth == 1280 - 2 * 88
    assert view_model.windowGeometryHeight == 720 - 2 * 88
    assert view_model.drawsOwnFrame
    assert view_model.dropShadowMargin == 88
    assert not view_model.isFullscreen
    assert not view_model.isMaximized
    assert not view_model.isMainWindowFocused


def test_pushed_surface_emits_frame_margin_and_geometry(
    surface, initialized_service, make_view_model, record_emissions
):
    view_model = make_view_model()
    emissions = record_emissions(view_model)

    surface.push(OWN_FRAME)

    emissions.assert_exactly(
        windowGeometryWidthChanged=1, windowGeometryHeightChanged=1, drawsOwnFrameChanged=1, dropShadowMarginChanged=1
    )
    assert emissions["drawsOwnFrameChanged"].at(0, 0) is True
    assert emissions["dropShadowMarginChanged"].at(0, 0) == 88
    assert emissions["windowGeometryWidthChanged"].at(0, 0) == 1280 - 2 * 88
    assert emissions["windowGeometryHeightChanged"].at(0, 0) == 720 - 2 * 88


def test_margin_move_with_the_frame_already_drawn_keeps_frame_silent(
    surface, initialized_service, make_view_model, record_emissions
):
    surface.push(OWN_FRAME)
    view_model = make_view_model()
    emissions = record_emissions(view_model)

    surface.push(SurfaceSnapshot(draws_own_frame=True, drop_shadow_margin=64))

    emissions.assert_exactly(windowGeometryWidthChanged=1, windowGeometryHeightChanged=1, dropShadowMarginChanged=1)
    assert emissions["dropShadowMarginChanged"].at(0, 0) == 64
    assert view_model.drawsOwnFrame


def test_fullscreen_state_change_emits_the_fullscreen_notify_alone(
    window_state, initialized_service, window, make_view_model, record_emissions
):
    view_model = make_view_model()
    emissions = record_emissions(view_model)

    window_state.state = WindowStateSnapshot(is_fullscreen=True, is_maximized=False)
    window.xChanged.emit(50)

    emissions.assert_exactly(isFullscreenChanged=1)
    assert emissions["isFullscreenChanged"].at(0, 0) is True


def test_maximize_state_change_emits_the_maximize_notify_alone(
    window_state, initialized_service, window, make_view_model, record_emissions
):
    view_model = make_view_model()
    emissions = record_emissions(view_model)

    window_state.state = WindowStateSnapshot(is_fullscreen=False, is_maximized=True)
    window.xChanged.emit(50)

    emissions.assert_exactly(isMaximizedChanged=1)
    assert emissions["isMaximizedChanged"].at(0, 0) is True


def test_dropped_own_frame_emits_frame_margin_and_geometry(
    surface, initialized_service, make_view_model, record_emissions
):
    surface.push(OWN_FRAME)
    view_model = make_view_model()
    emissions = record_emissions(view_model)

    surface.push(NO_OWN_FRAME)

    emissions.assert_exactly(
        windowGeometryWidthChanged=1, windowGeometryHeightChanged=1, drawsOwnFrameChanged=1, dropShadowMarginChanged=1
    )
    assert emissions["drawsOwnFrameChanged"].at(0, 0) is False
    assert emissions["dropShadowMarginChanged"].at(0, 0) == 0
    assert emissions["windowGeometryWidthChanged"].at(0, 0) == 1280
    assert emissions["windowGeometryHeightChanged"].at(0, 0) == 720


def test_focus_change_emits_the_focus_notify_alone(
    qt_app, initialized_service, window, make_view_model, record_emissions
):
    view_model = make_view_model()
    emissions = record_emissions(view_model)

    qt_app.focusWindowChanged.emit(window)

    emissions.assert_exactly(isMainWindowFocusedChanged=1)
    assert emissions["isMainWindowFocusedChanged"].at(0, 0) is True


def test_display_zoom_change_emits_nothing(initialized_service, make_view_model, record_emissions):
    view_model = make_view_model()
    emissions = record_emissions(view_model)

    initialized_service.display_zoom_factor_changed.emit(2.0)

    emissions.assert_silent()


def test_observer_of_a_notify_reads_settled_state(surface, initialized_service, make_view_model):
    view_model = make_view_model()
    observed: list[tuple[bool, int, int]] = []

    # drawsOwnFrameChanged is the first notify the surface cycle emits, so a view
    # model holding copies of the service's values would still carry the old
    # margin and width here.
    view_model.drawsOwnFrameChanged.connect(
        lambda _: observed.append(
            (view_model.drawsOwnFrame, view_model.dropShadowMargin, view_model.windowGeometryWidth)
        )
    )

    surface.push(OWN_FRAME)

    assert observed == [(True, 88, 1280 - 2 * 88)]


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
    window_state, initialized_service, window, make_view_model, case: CommandCase
):
    window_state.state = WindowStateSnapshot(is_fullscreen=case.is_fullscreen, is_maximized=case.is_maximized)
    window.xChanged.emit(1)
    view_model = make_view_model()

    case.invoke(view_model)

    expected = [(case.expected_command, window)] if case.expected_command else []
    assert window_state.commands == expected
