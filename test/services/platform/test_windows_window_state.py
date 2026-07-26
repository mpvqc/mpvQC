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

from mpvqc.services.platform.win import window_state
from mpvqc.services.platform.win.native import WindowPlacement
from mpvqc.services.platform.win.window_state import WindowsWindowStateHandler

NORMAL_RECT = (100, 100, 900, 700)
MONITOR = (0, 0, 1920, 1080)
BORDER = 8
OVERHANG_RECT = (-BORDER, 0, 1920 + BORDER, 1080 + BORDER)
MINIMIZED_RECT = (-32000, -32000, -31840, -31840)

SW_SHOWNORMAL = 1
SW_SHOWMAXIMIZED = 3

INITIAL_PLACEMENT = WindowPlacement(0, SW_SHOWNORMAL, (-1, -1), (-1, -1), NORMAL_RECT)


@dataclass
class FakeWin32Window:
    """Models the Windows state the window-state handler reads and writes."""

    placement: WindowPlacement = INITIAL_PLACEMENT
    maximized: bool = False
    minimized: bool = False
    rect: tuple = NORMAL_RECT
    monitor: tuple | None = MONITOR
    calls: list[tuple] = field(default_factory=list)

    def covers_monitor(self) -> bool:
        if self.monitor is None:
            return False
        left, top, right, bottom = self.rect
        m_left, m_top, m_right, m_bottom = self.monitor
        return left <= m_left and top <= m_top and right >= m_right and bottom >= m_bottom

    def get_window_placement(self) -> WindowPlacement:
        show_cmd = SW_SHOWMAXIMIZED if self.maximized else SW_SHOWNORMAL
        return self.placement._replace(show_cmd=show_cmd)

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


@pytest.fixture
def fake(monkeypatch) -> FakeWin32Window:
    fake = FakeWin32Window()

    def strip_maximize_style(_hwnd):
        fake.calls.append(("strip_maximize",))
        fake.maximized = False

    monkeypatch.setattr(
        window_state,
        "get_monitor_rect",
        lambda _hwnd: fake.monitor,
    )
    monkeypatch.setattr(
        window_state,
        "get_resize_border_thickness",
        lambda _hwnd, *, horizontal=True: BORDER,
    )
    monkeypatch.setattr(
        window_state,
        "is_maximized",
        lambda _hwnd: fake.maximized,
    )
    monkeypatch.setattr(
        window_state,
        "is_minimized",
        lambda _hwnd: fake.minimized,
    )
    monkeypatch.setattr(
        window_state,
        "is_fullscreen",
        lambda _hwnd: not fake.maximized and fake.covers_monitor(),
    )
    monkeypatch.setattr(
        window_state,
        "strip_maximize_style",
        strip_maximize_style,
    )
    monkeypatch.setattr(
        window_state,
        "set_outer_window_rect",
        lambda _hwnd, rect: fake.set_outer_window_rect(rect),
    )
    monkeypatch.setattr(
        window_state,
        "mark_fullscreen_window",
        lambda _hwnd, *, fullscreen: fake.calls.append(("marker", fullscreen)),
    )
    monkeypatch.setattr(
        window_state,
        "set_window_corners_rounded",
        lambda _hwnd, *, rounded: fake.calls.append(("corners", rounded)),
    )
    monkeypatch.setattr(
        window_state,
        "set_window_border_visible",
        lambda _hwnd, *, visible: fake.calls.append(("border", visible)),
    )
    monkeypatch.setattr(
        window_state,
        "set_window_transitions_enabled",
        lambda _hwnd, *, enabled: fake.calls.append(("transitions", enabled)),
    )
    monkeypatch.setattr(
        window_state,
        "refresh_window_frame",
        lambda _hwnd: fake.calls.append(("refresh",)),
    )
    monkeypatch.setattr(
        window_state,
        "get_window_placement",
        lambda _hwnd: fake.get_window_placement(),
    )
    monkeypatch.setattr(
        window_state,
        "set_window_placement",
        lambda _hwnd, p: fake.set_window_placement(p),
    )
    monkeypatch.setattr(
        window_state,
        "maximize_window",
        lambda _hwnd: fake.maximize(),
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
    assert handler.is_fullscreen(window)


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
    assert not handler.is_fullscreen(window)


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
    assert not handler.is_fullscreen(window)


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


def test_repeated_enter_keeps_first_placement(fake, handler, window):
    handler.enter_fullscreen(window)
    handler.enter_fullscreen(window)

    handler.exit_fullscreen(window)

    assert fake.rect == NORMAL_RECT


def test_enter_with_abandoned_session_saves_fresh_placement(fake, handler, window):
    handler.enter_fullscreen(window)
    # The OS re-maximized the window behind the app's back (Win+Up)
    fake.maximized = True
    fake.rect = MONITOR

    handler.enter_fullscreen(window)

    assert not fake.maximized
    assert fake.rect == OVERHANG_RECT

    handler.exit_fullscreen(window)

    assert fake.maximized
    assert fake.placement.normal_rect == NORMAL_RECT


@dataclass(frozen=True)
class IsFullscreenCase:
    name: str
    maximized: bool
    minimized: bool
    rect: tuple
    expected: bool
    expects_repin: bool


@pytest.mark.parametrize(
    "case",
    [
        IsFullscreenCase(
            name="covering_monitor_is_fullscreen",
            maximized=False,
            minimized=False,
            rect=OVERHANG_RECT,
            expected=True,
            expects_repin=False,
        ),
        IsFullscreenCase(
            name="minimized_session_survives",
            maximized=False,
            minimized=True,
            rect=MINIMIZED_RECT,
            expected=True,
            expects_repin=False,
        ),
        IsFullscreenCase(
            # Known limitation: the restored path deliberately skips the repin
            name="restored_window_retires_without_repin",
            maximized=False,
            minimized=False,
            rect=NORMAL_RECT,
            expected=False,
            expects_repin=False,
        ),
        IsFullscreenCase(
            # Win+Up out of fullscreen on a setup whose work area equals the monitor
            name="maximized_covering_monitor_retires",
            maximized=True,
            minimized=False,
            rect=MONITOR,
            expected=False,
            expects_repin=True,
        ),
    ],
    ids=lambda case: case.name,
)
def test_is_fullscreen(case: IsFullscreenCase, fake, handler, window):
    handler.enter_fullscreen(window)
    fake.maximized = case.maximized
    fake.minimized = case.minimized
    fake.rect = case.rect

    assert handler.is_fullscreen(window) is case.expected

    expected_normal_rect = NORMAL_RECT if case.expects_repin else OVERHANG_RECT
    assert fake.placement.normal_rect == expected_normal_rect
    if not case.expected:
        assert ("marker", False) in fake.calls
        assert not handler.is_fullscreen(window)


class QtMechanismTestCase(NamedTuple):
    name: str
    operation: Callable[[WindowsWindowStateHandler, QWindow], None]
    expected_request: object


@pytest.mark.parametrize(
    "case",
    [
        QtMechanismTestCase(
            "minimize_via_show_minimized",
            WindowsWindowStateHandler.minimize,
            "showMinimized",
        ),
        QtMechanismTestCase(
            "maximize_replaces_states",
            WindowsWindowStateHandler.maximize,
            Qt.WindowState.WindowMaximized,
        ),
        QtMechanismTestCase(
            "show_normal_replaces_states",
            WindowsWindowStateHandler.show_normal,
            Qt.WindowState.WindowNoState,
        ),
    ],
    ids=lambda case: case.name,
)
def test_operations_use_qt_mechanisms(case: QtMechanismTestCase, handler, make_recording_window):
    window = make_recording_window()

    case.operation(handler, window)

    assert window.requests == [case.expected_request]


class IsMaximizedCase(NamedTuple):
    name: str
    fullscreen_session: bool
    entered_from_maximized: bool
    qt_states: Qt.WindowState
    expected: bool


@pytest.mark.parametrize(
    "case",
    [
        IsMaximizedCase(
            "plain_answers_from_qt_states",
            fullscreen_session=False,
            entered_from_maximized=False,
            qt_states=Qt.WindowState.WindowMaximized,
            expected=True,
        ),
        IsMaximizedCase(
            "plain_normal_window",
            fullscreen_session=False,
            entered_from_maximized=False,
            qt_states=Qt.WindowState.WindowNoState,
            expected=False,
        ),
        IsMaximizedCase(
            # WS_MAXIMIZE is stripped while fullscreen; the saved placement remembers
            "session_from_maximized_stays_maximized",
            fullscreen_session=True,
            entered_from_maximized=True,
            qt_states=Qt.WindowState.WindowNoState,
            expected=True,
        ),
        IsMaximizedCase(
            "session_from_normal",
            fullscreen_session=True,
            entered_from_maximized=False,
            qt_states=Qt.WindowState.WindowNoState,
            expected=False,
        ),
    ],
    ids=lambda case: case.name,
)
def test_is_maximized(case: IsMaximizedCase, fake, handler, window):
    if case.fullscreen_session:
        fake.maximized = case.entered_from_maximized
        if fake.maximized:
            fake.rect = MONITOR
        handler.enter_fullscreen(window)

    window.setWindowStates(case.qt_states)

    assert handler.is_maximized(window) is case.expected


def test_is_maximized_after_retired_session_answers_from_qt_states(fake, handler, window):
    handler.enter_fullscreen(window)
    # The OS restored the window behind the app's back
    fake.rect = NORMAL_RECT

    assert not handler.is_fullscreen(window)

    window.setWindowStates(Qt.WindowState.WindowMaximized)
    assert handler.is_maximized(window)


def test_shadow_margin_is_always_zero(fake, handler, window):
    assert handler.shadow_margin(window) == 0

    handler.enter_fullscreen(window)
    assert handler.shadow_margin(window) == 0

    handler.apply_content_margins(88)
    assert handler.shadow_margin(window) == 0
