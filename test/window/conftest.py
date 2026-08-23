# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable
from dataclasses import dataclass, field

import pytest
from PySide6.QtGui import QGuiApplication, QWindow

from mpvqc.window.services import (
    EmbeddedPlayerTracker,
    NoEmbeddedPlayerTracker,
    NoSurfaceHandler,
    NoWindowConfigurator,
    NoWindowRevealer,
    PlatformBackend,
    PlatformCapabilities,
    PlatformService,
    QtWindowStateHandler,
    StaticWindowButtons,
    SurfaceHandler,
    WindowButtonPreference,
    WindowButtonSource,
    WindowConfigurator,
    WindowRevealer,
    WindowStateHandler,
    WindowStateSnapshot,
    linux_tiling_capabilities,
)

WINDOWED = WindowStateSnapshot(is_fullscreen=False, is_maximized=False)


@dataclass
class RecordingWindowState:
    state: WindowStateSnapshot = WINDOWED
    commands: list[tuple[str, QWindow]] = field(default_factory=list)
    reads: list[QWindow] = field(default_factory=list)

    def minimize(self, window: QWindow) -> None:
        self.commands.append(("minimize", window))

    def maximize(self, window: QWindow) -> None:
        self.commands.append(("maximize", window))

    def show_normal(self, window: QWindow) -> None:
        self.commands.append(("show_normal", window))

    def enter_fullscreen(self, window: QWindow) -> None:
        self.commands.append(("enter_fullscreen", window))

    def exit_fullscreen(self, window: QWindow) -> None:
        self.commands.append(("exit_fullscreen", window))

    def read_state(self, window: QWindow) -> WindowStateSnapshot:
        self.reads.append(window)
        return self.state


@dataclass
class RecordingSurface:
    margin: int = 0
    reads: list[QWindow] = field(default_factory=list)
    callbacks: list[Callable[[int], None]] = field(default_factory=list)

    def drop_shadow_margin(self, window: QWindow) -> int:
        self.reads.append(window)
        return self.margin

    def on_drop_shadow_margin_changed(self, callback: Callable[[int], None]) -> None:
        self.callbacks.append(callback)

    def push(self, margin: int) -> None:
        self.margin = margin
        for callback in self.callbacks:
            callback(margin)


@dataclass
class RecordingWindowConfigurator:
    configured: list[tuple[QGuiApplication, QWindow]] = field(default_factory=list)

    def configure_window(self, app: QGuiApplication, window: QWindow) -> None:
        self.configured.append((app, window))


@dataclass
class RecordingWindowRevealer:
    installed: list[tuple[QGuiApplication, QWindow]] = field(default_factory=list)

    def install(self, app: QGuiApplication, main_window: QWindow) -> None:
        self.installed.append((app, main_window))


@dataclass
class RecordingEmbeddedPlayer:
    tracked: list[int] = field(default_factory=list)

    def track(self, win_id: int) -> None:
        self.tracked.append(win_id)


class FakeWindowButtons:
    def __init__(self, preference: WindowButtonPreference) -> None:
        self._preference = preference
        self._callbacks: list[Callable[[WindowButtonPreference], None]] = []

    @property
    def preference(self) -> WindowButtonPreference:
        return self._preference

    def on_preference_changed(self, callback: Callable[[WindowButtonPreference], None]) -> None:
        self._callbacks.append(callback)

    def push(self, preference: WindowButtonPreference) -> None:
        self._preference = preference
        for callback in self._callbacks:
            callback(preference)


@pytest.fixture
def window_state() -> RecordingWindowState:
    return RecordingWindowState()


@pytest.fixture
def surface() -> RecordingSurface:
    return RecordingSurface()


@pytest.fixture
def window_configurator() -> RecordingWindowConfigurator:
    return RecordingWindowConfigurator()


@pytest.fixture
def window_revealer() -> RecordingWindowRevealer:
    return RecordingWindowRevealer()


@pytest.fixture
def embedded_player() -> RecordingEmbeddedPlayer:
    return RecordingEmbeddedPlayer()


@pytest.fixture
def make_window_buttons() -> Callable[[WindowButtonPreference], FakeWindowButtons]:
    def _make(preference: WindowButtonPreference) -> FakeWindowButtons:
        return FakeWindowButtons(preference)

    return _make


@pytest.fixture
def make_platform_service(qt_app) -> Callable[..., PlatformService]:
    def _make(
        *,
        capabilities: PlatformCapabilities | None = None,
        window_state: WindowStateHandler | None = None,
        surface: SurfaceHandler | None = None,
        window_configuration: WindowConfigurator | None = None,
        window_reveal: WindowRevealer | None = None,
        embedded_player: EmbeddedPlayerTracker | None = None,
        window_buttons: WindowButtonSource | None = None,
    ) -> PlatformService:
        backend = PlatformBackend(
            capabilities=linux_tiling_capabilities() if capabilities is None else capabilities,
            window_state=QtWindowStateHandler() if window_state is None else window_state,
            surface=NoSurfaceHandler() if surface is None else surface,
            window_configuration=NoWindowConfigurator() if window_configuration is None else window_configuration,
            window_reveal=NoWindowRevealer() if window_reveal is None else window_reveal,
            embedded_player=NoEmbeddedPlayerTracker() if embedded_player is None else embedded_player,
            window_buttons=StaticWindowButtons() if window_buttons is None else window_buttons,
        )
        return PlatformService(backend)

    return _make
