# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import NamedTuple

import pytest
from PySide6.QtCore import Qt
from PySide6.QtGui import QWindow

if sys.platform != "win32":
    pytest.skip("Requires Windows", allow_module_level=True)

from mpvqc.window.services.windows import WindowsWindowStateHandler
from mpvqc.window.services.windows_decisions import WindowPlacement

WINDOW_STATE = "mpvqc.window.services.windows.window_state"
PROBES = "mpvqc.window.services.windows.probes"

NORMAL_RECT = (100, 100, 900, 700)
MONITOR = (0, 0, 1920, 1080)
BORDER = 8
OVERHANG_RECT = (-BORDER, 0, 1920 + BORDER, 1080 + BORDER)

SW_SHOWNORMAL = 1
SW_SHOWMINIMIZED = 2
SW_SHOWMAXIMIZED = 3
WPF_RESTORETOMAXIMIZED = 2

INITIAL_PLACEMENT = WindowPlacement(
    flags=0,
    show_cmd=SW_SHOWNORMAL,
    min_position=(-1, -1),
    max_position=(-1, -1),
    normal_rect=NORMAL_RECT,
)


@dataclass
class FakeWin32Window:
    placement: WindowPlacement = INITIAL_PLACEMENT
    maximized: bool = False
    minimized: bool = False
    restores_to_maximized: bool = False
    rect: tuple = NORMAL_RECT
    monitor: tuple | None = MONITOR
    calls: list[tuple] = field(default_factory=list)

    def overhangs_monitor(self) -> bool:
        if self.monitor is None:
            return False
        left, top, right, bottom = self.rect
        m_left, m_top, m_right, m_bottom = self.monitor
        covers = left <= m_left and top <= m_top and right >= m_right and bottom >= m_bottom
        return covers and self.rect != self.monitor

    def get_window_placement(self) -> WindowPlacement:
        if self.minimized:
            show_cmd = SW_SHOWMINIMIZED
        elif self.maximized:
            show_cmd = SW_SHOWMAXIMIZED
        else:
            show_cmd = SW_SHOWNORMAL
        flags = WPF_RESTORETOMAXIMIZED if self.restores_to_maximized else 0
        return self.placement._replace(flags=flags, show_cmd=show_cmd)

    def set_window_placement(self, placement: WindowPlacement) -> None:
        self.calls.append(("set_placement", placement))
        self.placement = placement
        if placement.shows_maximized:
            self.maximized = True
        else:
            self.maximized = False
            self.rect = placement.normal_rect

    def set_outer_window_rect(self, rect: tuple) -> None:
        self.calls.append(("rect", rect))
        self.rect = rect
        if not self.maximized:
            # Windows tracks a restored window's outer rect as its normal geometry
            self.placement = self.placement._replace(normal_rect=rect)

    def maximize(self) -> None:
        self.calls.append(("maximize",))
        self.maximized = True

    def minimize(self) -> None:
        self.calls.append(("minimize",))
        self.restores_to_maximized = self.maximized
        self.maximized = False
        self.minimized = True


@pytest.fixture
def fake(monkeypatch) -> FakeWin32Window:
    fake = FakeWin32Window()

    def strip_maximize_style(_hwnd):
        fake.calls.append(("strip_maximize",))
        fake.maximized = False

    monkeypatch.setattr(
        f"{PROBES}.get_monitor_rect",
        lambda _hwnd: fake.monitor,
    )
    monkeypatch.setattr(
        f"{PROBES}.get_resize_border_thickness",
        lambda _hwnd, *, horizontal=True: BORDER,
    )
    monkeypatch.setattr(
        # Real is_maximized reads show_cmd, not WS_MAXIMIZE, which is what makes
        # maximized and minimized mutually exclusive. Deriving it here keeps the
        # fake from disagreeing with the window it models.
        f"{PROBES}.is_maximized",
        lambda _hwnd: fake.get_window_placement().shows_maximized,
    )
    monkeypatch.setattr(
        f"{PROBES}.is_minimized",
        lambda _hwnd: fake.minimized,
    )
    monkeypatch.setattr(
        f"{PROBES}.overhangs_monitor",
        lambda _hwnd: fake.overhangs_monitor(),
    )
    monkeypatch.setattr(
        f"{PROBES}.get_window_placement",
        lambda _hwnd: fake.get_window_placement(),
    )
    monkeypatch.setattr(
        f"{WINDOW_STATE}.strip_maximize_style",
        strip_maximize_style,
    )
    monkeypatch.setattr(
        f"{WINDOW_STATE}.set_outer_window_rect",
        lambda _hwnd, rect: fake.set_outer_window_rect(rect),
    )
    monkeypatch.setattr(
        f"{WINDOW_STATE}.mark_fullscreen_window",
        lambda _hwnd, *, fullscreen: fake.calls.append(("marker", fullscreen)),
    )
    monkeypatch.setattr(
        f"{WINDOW_STATE}.set_window_corners_rounded",
        lambda _hwnd, *, rounded: fake.calls.append(("corners", rounded)),
    )
    monkeypatch.setattr(
        f"{WINDOW_STATE}.set_window_border_visible",
        lambda _hwnd, *, visible: fake.calls.append(("border", visible)),
    )
    monkeypatch.setattr(
        f"{WINDOW_STATE}.set_window_transitions_enabled",
        lambda _hwnd, *, enabled: fake.calls.append(("transitions", enabled)),
    )
    monkeypatch.setattr(
        f"{WINDOW_STATE}.refresh_window_frame",
        lambda _hwnd: fake.calls.append(("refresh",)),
    )
    monkeypatch.setattr(
        f"{WINDOW_STATE}.get_window_placement",
        lambda _hwnd: fake.get_window_placement(),
    )
    monkeypatch.setattr(
        f"{WINDOW_STATE}.set_window_placement",
        lambda _hwnd, p: fake.set_window_placement(p),
    )
    monkeypatch.setattr(
        f"{WINDOW_STATE}.maximize_window",
        lambda _hwnd: fake.maximize(),
    )
    monkeypatch.setattr(
        f"{WINDOW_STATE}.minimize_window",
        lambda _hwnd: fake.minimize(),
    )
    return fake


@pytest.fixture
def handler() -> WindowsWindowStateHandler:
    return WindowsWindowStateHandler()


@pytest.fixture
def window(qt_app) -> QWindow:
    return QWindow()


def test_enter_from_normal(fake, handler, window):
    handler.enter_fullscreen(window)

    assert fake.rect == OVERHANG_RECT
    assert ("marker", True) in fake.calls
    assert ("corners", False) in fake.calls
    assert ("border", False) in fake.calls
    assert all(call[0] != "transitions" for call in fake.calls)
    assert handler.read_state(window).is_fullscreen


def test_enter_from_maximized_wraps_move_in_transitions(fake, handler, window):
    fake.maximized = True
    fake.rect = MONITOR

    handler.enter_fullscreen(window)

    assert not fake.maximized
    assert fake.rect == OVERHANG_RECT
    disabled = fake.calls.index(("transitions", False))
    moved = fake.calls.index(("rect", OVERHANG_RECT))
    enabled = fake.calls.index(("transitions", True))
    assert disabled < moved < enabled


def test_enter_without_monitor_is_noop(fake, handler, window):
    fake.monitor = None

    handler.enter_fullscreen(window)

    assert fake.calls == []
    assert not handler.read_state(window).is_fullscreen


def test_exit_restores_normal_placement(fake, handler, window):
    handler.enter_fullscreen(window)
    fake.calls.clear()

    handler.exit_fullscreen(window)

    assert fake.rect == NORMAL_RECT
    assert not fake.maximized
    assert ("marker", False) in fake.calls
    assert ("corners", True) in fake.calls
    assert ("border", True) in fake.calls
    assert ("refresh",) in fake.calls
    assert not handler.read_state(window).is_fullscreen


def test_exit_to_maximized_repins_normal_geometry(fake, handler, window):
    fake.maximized = True
    handler.enter_fullscreen(window)
    fake.calls.clear()

    handler.exit_fullscreen(window)

    assert fake.maximized
    assert fake.placement.normal_rect == NORMAL_RECT
    disabled = fake.calls.index(("transitions", False))
    maximize = fake.calls.index(("maximize",))
    enabled = fake.calls.index(("transitions", True))
    assert disabled < maximize < enabled


def test_exit_without_enter_is_noop(fake, handler, window):
    handler.exit_fullscreen(window)

    assert fake.calls == []


def test_repeated_enter_does_not_retire_the_live_session(fake, handler, window):
    handler.enter_fullscreen(window)
    fake.calls.clear()

    handler.enter_fullscreen(window)

    assert ("corners", True) not in fake.calls
    assert ("marker", False) not in fake.calls


def test_read_retires_a_session_the_os_ended(fake, handler, window):
    handler.enter_fullscreen(window)
    fake.maximized = True
    fake.rect = MONITOR
    fake.calls.clear()

    state = handler.read_state(window)

    assert not state.is_fullscreen
    assert state.is_maximized
    assert ("marker", False) in fake.calls
    assert ("corners", True) in fake.calls
    assert ("border", True) in fake.calls
    assert fake.placement.normal_rect == NORMAL_RECT


def test_a_retired_session_is_not_retired_again(fake, handler, window):
    handler.enter_fullscreen(window)
    fake.maximized = True
    fake.rect = MONITOR
    handler.read_state(window)
    fake.calls.clear()

    handler.read_state(window)

    assert fake.calls == []


def test_read_without_a_session_does_not_create_the_native_window(fake, handler, make_recording_window):
    # winId() on a window without a native handle creates one, and the frame
    # configuration then arrives too late to reclaim the caption: two title bars.
    window = make_recording_window()

    handler.read_state(window)

    assert window.win_id_calls == 0


def test_read_while_minimized_keeps_the_session(fake, handler, window):
    handler.enter_fullscreen(window)
    # Windows parks a minimized window off-screen, so its rect no longer
    # overhangs the monitor. That must not read as the OS ending fullscreen.
    fake.minimized = True
    fake.rect = (-32000, -32000, -31000, -31000)
    fake.calls.clear()

    assert handler.read_state(window).is_fullscreen
    assert fake.calls == []


def test_enter_with_abandoned_session_saves_fresh_placement(fake, handler, window):
    handler.enter_fullscreen(window)
    fake.maximized = True
    fake.rect = MONITOR

    handler.enter_fullscreen(window)

    assert not fake.maximized
    assert fake.rect == OVERHANG_RECT

    handler.exit_fullscreen(window)

    assert fake.maximized
    assert fake.placement.normal_rect == NORMAL_RECT


class QtMechanismTestCase(NamedTuple):
    name: str
    operation: Callable[[WindowsWindowStateHandler, QWindow], None]
    initial_states: Qt.WindowState
    expected_request: object


@pytest.mark.parametrize(
    "case",
    [
        QtMechanismTestCase(
            name="maximize_replaces_minimized",
            operation=WindowsWindowStateHandler.maximize,
            initial_states=Qt.WindowState.WindowMinimized,
            expected_request=Qt.WindowState.WindowMaximized,
        ),
        QtMechanismTestCase(
            name="show_normal_replaces_maximized",
            operation=WindowsWindowStateHandler.show_normal,
            initial_states=Qt.WindowState.WindowMaximized,
            expected_request=Qt.WindowState.WindowNoState,
        ),
    ],
    ids=lambda case: case.name,
)
def test_operations_use_qt_mechanisms(case: QtMechanismTestCase, handler, make_recording_window):
    window = make_recording_window(case.initial_states)

    case.operation(handler, window)

    assert window.requests == [case.expected_request]


def test_minimize_dispatches_to_native_wrapper(fake, handler, make_recording_window):
    window = make_recording_window()

    handler.minimize(window)

    assert ("minimize",) in fake.calls
    assert window.requests == []
