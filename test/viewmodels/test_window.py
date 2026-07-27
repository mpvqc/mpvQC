# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable
from typing import NamedTuple

import inject
import pytest
from PySide6.QtCore import QObject, Signal, SignalInstance

from mpvqc.services import MainWindowService
from mpvqc.viewmodels import MpvqcWindowViewModel


class MainWindowServiceFake(QObject):
    window_geometry_width_changed = Signal(int)
    window_geometry_height_changed = Signal(int)
    drop_shadow_margin_changed = Signal(int)
    is_fullscreen_changed = Signal(bool)
    is_maximized_changed = Signal(bool)
    is_main_window_focused_changed = Signal(bool)

    def __init__(self):
        super().__init__()
        self.window_geometry_width = 0
        self.window_geometry_height = 0
        self.drop_shadow_margin = 0
        self.is_fullscreen = False
        self.is_maximized = False
        self.is_main_window_focused = False
        self.commands: list[str] = []

    def set_window_geometry_width(self, width: int) -> None:
        self.window_geometry_width = width
        self.window_geometry_width_changed.emit(width)

    def set_window_geometry_height(self, height: int) -> None:
        self.window_geometry_height = height
        self.window_geometry_height_changed.emit(height)

    def set_drop_shadow_margin(self, margin: int) -> None:
        self.drop_shadow_margin = margin
        self.drop_shadow_margin_changed.emit(margin)

    def set_is_fullscreen(self, is_fullscreen: bool) -> None:
        self.is_fullscreen = is_fullscreen
        self.is_fullscreen_changed.emit(is_fullscreen)

    def set_is_maximized(self, is_maximized: bool) -> None:
        self.is_maximized = is_maximized
        self.is_maximized_changed.emit(is_maximized)

    def set_is_main_window_focused(self, is_focused: bool) -> None:
        self.is_main_window_focused = is_focused
        self.is_main_window_focused_changed.emit(is_focused)

    def minimize(self) -> None:
        self.commands.append("minimize")

    def show_maximized(self) -> None:
        self.commands.append("show_maximized")

    def show_normal(self) -> None:
        self.commands.append("show_normal")

    def show_fullscreen(self) -> None:
        self.commands.append("show_fullscreen")

    def exit_fullscreen(self) -> None:
        self.commands.append("exit_fullscreen")


@pytest.fixture
def main_window_service() -> MainWindowServiceFake:
    return MainWindowServiceFake()


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, main_window_service):
    def custom_bindings(binder: inject.Binder):
        binder.bind(MainWindowService, main_window_service)

    common_bindings_with(custom_bindings)


@pytest.fixture
def view_model() -> MpvqcWindowViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcWindowViewModel()


@pytest.mark.parametrize(
    "member",
    [
        "window_geometry_width",
        "window_geometry_height",
        "drop_shadow_margin",
        "is_fullscreen",
        "is_maximized",
        "is_main_window_focused",
        "window_geometry_width_changed",
        "window_geometry_height_changed",
        "drop_shadow_margin_changed",
        "is_fullscreen_changed",
        "is_maximized_changed",
        "is_main_window_focused_changed",
        "minimize",
        "show_maximized",
        "show_normal",
        "show_fullscreen",
        "exit_fullscreen",
    ],
)
def test_fake_mirrors_service_member(main_window_service, member):
    # The fake needs real signals, so it cannot be a spec_set mock. This keeps it from drifting.
    assert hasattr(MainWindowService, member)
    assert hasattr(main_window_service, member)


class ForwardCase(NamedTuple):
    tag: str
    change: Callable[[MainWindowServiceFake], None]
    read: Callable[[MpvqcWindowViewModel], object]
    expected: object


@pytest.mark.parametrize(
    "test_case",
    [
        ForwardCase(
            "windowGeometryWidth", lambda s: s.set_window_geometry_width(640), lambda vm: vm.windowGeometryWidth, 640
        ),
        ForwardCase(
            "windowGeometryHeight", lambda s: s.set_window_geometry_height(480), lambda vm: vm.windowGeometryHeight, 480
        ),
        ForwardCase("isFullscreen", lambda s: s.set_is_fullscreen(True), lambda vm: vm.isFullscreen, True),
        ForwardCase("isMaximized", lambda s: s.set_is_maximized(True), lambda vm: vm.isMaximized, True),
        ForwardCase("dropShadowMargin", lambda s: s.set_drop_shadow_margin(12), lambda vm: vm.dropShadowMargin, 12),
        ForwardCase(
            "isMainWindowFocused",
            lambda s: s.set_is_main_window_focused(True),
            lambda vm: vm.isMainWindowFocused,
            True,
        ),
    ],
    ids=lambda tc: tc.tag,
)
def test_property_mirrors_service(view_model, main_window_service, test_case: ForwardCase):
    test_case.change(main_window_service)

    assert test_case.read(view_model) == test_case.expected


class RelayCase(NamedTuple):
    tag: str
    change: Callable[[MainWindowServiceFake], None]
    signal: Callable[[MpvqcWindowViewModel], SignalInstance]
    expected_arguments: tuple[object, ...]


@pytest.mark.parametrize(
    "test_case",
    [
        RelayCase(
            "windowGeometryWidthChanged",
            lambda s: s.set_window_geometry_width(640),
            lambda vm: vm.windowGeometryWidthChanged,
            (640,),
        ),
        RelayCase(
            "windowGeometryHeightChanged",
            lambda s: s.set_window_geometry_height(480),
            lambda vm: vm.windowGeometryHeightChanged,
            (480,),
        ),
        RelayCase(
            "isFullscreenChanged", lambda s: s.set_is_fullscreen(True), lambda vm: vm.isFullscreenChanged, (True,)
        ),
        RelayCase("isMaximizedChanged", lambda s: s.set_is_maximized(True), lambda vm: vm.isMaximizedChanged, (True,)),
        RelayCase(
            "dropShadowMarginChanged",
            lambda s: s.set_drop_shadow_margin(12),
            lambda vm: vm.dropShadowMarginChanged,
            (12,),
        ),
        RelayCase("radiusChanged", lambda s: s.set_drop_shadow_margin(12), lambda vm: vm.radiusChanged, ()),
        RelayCase(
            "isMainWindowFocusedChanged",
            lambda s: s.set_is_main_window_focused(True),
            lambda vm: vm.isMainWindowFocusedChanged,
            (True,),
        ),
    ],
    ids=lambda tc: tc.tag,
)
def test_notify_relays_service_signal(view_model, main_window_service, make_spy, test_case: RelayCase):
    spy = make_spy(test_case.signal(view_model))

    test_case.change(main_window_service)

    assert spy.count() == 1
    arguments = tuple(spy.at(0, index) for index in range(len(test_case.expected_arguments)))
    assert arguments == test_case.expected_arguments


@pytest.mark.parametrize(
    ("drop_shadow_margin", "expected_radius"),
    [
        (0, 0),
        (1, 8),
        (88, 8),
    ],
)
def test_radius_follows_drop_shadow_margin(view_model, main_window_service, drop_shadow_margin, expected_radius):
    main_window_service.set_drop_shadow_margin(drop_shadow_margin)

    assert view_model.dropShadowMargin == drop_shadow_margin
    assert view_model.radius == expected_radius


class CommandCase(NamedTuple):
    tag: str
    is_fullscreen: bool
    is_maximized: bool
    invoke: Callable[[MpvqcWindowViewModel], None]
    expected_commands: list[str]


@pytest.mark.parametrize(
    "test_case",
    [
        CommandCase("minimize", False, False, lambda vm: vm.minimize(), ["minimize"]),
        CommandCase("not maximized -> maximize", False, False, lambda vm: vm.toggleMaximized(), ["show_maximized"]),
        CommandCase("maximized -> normal", False, True, lambda vm: vm.toggleMaximized(), ["show_normal"]),
        CommandCase(
            "not fullscreen -> fullscreen", False, False, lambda vm: vm.toggleFullScreen(), ["show_fullscreen"]
        ),
        CommandCase(
            "fullscreen -> exit fullscreen", True, False, lambda vm: vm.toggleFullScreen(), ["exit_fullscreen"]
        ),
        CommandCase(
            "fullscreen -> disable fullscreen", True, False, lambda vm: vm.disableFullScreen(), ["exit_fullscreen"]
        ),
        CommandCase("windowed -> disable fullscreen does nothing", False, False, lambda vm: vm.disableFullScreen(), []),
    ],
    ids=lambda tc: tc.tag,
)
def test_command_delegates_to_service(view_model, main_window_service, test_case: CommandCase):
    main_window_service.is_fullscreen = test_case.is_fullscreen
    main_window_service.is_maximized = test_case.is_maximized

    test_case.invoke(view_model)

    assert main_window_service.commands == test_case.expected_commands
