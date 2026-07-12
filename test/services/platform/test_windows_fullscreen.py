# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
from dataclasses import dataclass, field

import pytest
from PySide6.QtGui import QWindow

if sys.platform != "win32":
    pytest.skip("Requires Windows", allow_module_level=True)

import win32con

from mpvqc.services.platform.win import fullscreen
from mpvqc.services.platform.win.fullscreen import WindowsFullscreenHandler

NORMAL_RECT = (100, 100, 900, 700)
MONITOR = (0, 0, 1920, 1080)
BORDER = 8
OVERHANG_RECT = (-BORDER, 0, 1920 + BORDER, 1080 + BORDER)
MINIMIZED_RECT = (-32000, -32000, -31840, -31840)


@dataclass
class FakeWin32Window:
    """Models the Windows state the fullscreen handler reads and writes."""

    placement: tuple = (0, win32con.SW_SHOWNORMAL, (-1, -1), (-1, -1), NORMAL_RECT)
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

    def get_window_placement(self) -> tuple:
        show_cmd = win32con.SW_SHOWMAXIMIZED if self.maximized else win32con.SW_SHOWNORMAL
        return (self.placement[0], show_cmd, self.placement[2], self.placement[3], self.placement[4])

    def set_window_placement(self, placement: tuple) -> None:
        self.calls.append(("set_placement", placement))
        self.placement = tuple(placement)
        if placement[1] == win32con.SW_SHOWMAXIMIZED:
            self.maximized = True
        else:
            self.maximized = False
            self.rect = placement[4]

    def set_outer_window_rect(self, rect: tuple) -> None:
        self.calls.append(("rect", rect))
        self.rect = rect
        if not self.maximized:
            # Windows tracks a restored window's outer rect as its normal geometry
            self.placement = (*self.placement[:4], rect)

    def maximize(self) -> None:
        self.calls.append(("maximize",))
        self.maximized = True


@pytest.fixture
def fake(monkeypatch) -> FakeWin32Window:
    fake = FakeWin32Window()

    def set_style_flag(_hwnd, flag, *, enabled):
        fake.calls.append(("style", flag, enabled))
        if flag == win32con.WS_MAXIMIZE:
            fake.maximized = enabled

    monkeypatch.setattr(fullscreen, "get_monitor_rect", lambda _hwnd: fake.monitor)
    monkeypatch.setattr(fullscreen, "get_resize_border_thickness", lambda _hwnd, *, horizontal=True: BORDER)
    monkeypatch.setattr(fullscreen, "is_maximized", lambda _hwnd: fake.maximized)
    monkeypatch.setattr(fullscreen, "is_minimized", lambda _hwnd: fake.minimized)
    monkeypatch.setattr(fullscreen, "is_fullscreen", lambda _hwnd: not fake.maximized and fake.covers_monitor())
    monkeypatch.setattr(fullscreen, "set_style_flag", set_style_flag)
    monkeypatch.setattr(fullscreen, "set_outer_window_rect", lambda _hwnd, rect: fake.set_outer_window_rect(rect))
    monkeypatch.setattr(
        fullscreen,
        "set_shell_fullscreen_marker",
        lambda _hwnd, *, fullscreen: fake.calls.append(("marker", fullscreen)),
    )
    monkeypatch.setattr(
        fullscreen, "set_window_corners_rounded", lambda _hwnd, *, rounded: fake.calls.append(("corners", rounded))
    )
    monkeypatch.setattr(
        fullscreen, "set_window_border_visible", lambda _hwnd, *, visible: fake.calls.append(("border", visible))
    )
    monkeypatch.setattr(
        fullscreen,
        "set_window_transitions_enabled",
        lambda _hwnd, *, enabled: fake.calls.append(("transitions", enabled)),
    )
    monkeypatch.setattr(fullscreen, "refresh_window_frame", lambda _hwnd: fake.calls.append(("refresh",)))
    monkeypatch.setattr(fullscreen, "get_window_placement", lambda _hwnd: fake.get_window_placement())
    monkeypatch.setattr(fullscreen, "set_window_placement", lambda _hwnd, p: fake.set_window_placement(p))
    monkeypatch.setattr(fullscreen, "maximize_window", lambda _hwnd: fake.maximize())
    return fake


@pytest.fixture
def handler() -> WindowsFullscreenHandler:
    return WindowsFullscreenHandler()


@pytest.fixture
def window(qt_app) -> QWindow:
    return QWindow()


def test_enter_from_normal(fake, handler, window):
    handler.enter(window)

    assert fake.rect == OVERHANG_RECT
    assert ("marker", True) in fake.calls
    assert ("corners", False) in fake.calls
    assert ("border", False) in fake.calls
    assert all(call[0] != "transitions" for call in fake.calls)
    assert handler.is_active(window)


def test_enter_from_maximized_wraps_move_in_transitions(fake, handler, window):
    fake.maximized = True
    fake.rect = MONITOR

    handler.enter(window)

    assert fake.maximized is False
    assert fake.rect == OVERHANG_RECT
    disabled = fake.calls.index(("transitions", False))
    moved = fake.calls.index(("rect", OVERHANG_RECT))
    enabled = fake.calls.index(("transitions", True))
    assert disabled < moved < enabled


def test_enter_without_monitor_is_noop(fake, handler, window):
    fake.monitor = None

    handler.enter(window)

    assert fake.calls == []
    assert not handler.is_active(window)


def test_exit_restores_normal_placement(fake, handler, window):
    handler.enter(window)
    fake.calls.clear()

    handler.exit(window)

    assert fake.rect == NORMAL_RECT
    assert fake.maximized is False
    assert ("marker", False) in fake.calls
    assert ("corners", True) in fake.calls
    assert ("border", True) in fake.calls
    assert ("refresh",) in fake.calls
    assert not handler.is_active(window)


def test_exit_to_maximized_repins_normal_geometry(fake, handler, window):
    fake.maximized = True
    handler.enter(window)
    fake.calls.clear()

    handler.exit(window)

    assert fake.maximized is True
    assert fake.placement[4] == NORMAL_RECT
    disabled = fake.calls.index(("transitions", False))
    maximize = fake.calls.index(("maximize",))
    enabled = fake.calls.index(("transitions", True))
    assert disabled < maximize < enabled


def test_exit_without_enter_is_noop(fake, handler, window):
    handler.exit(window)

    assert fake.calls == []


def test_repeated_enter_keeps_first_placement(fake, handler, window):
    handler.enter(window)
    handler.enter(window)

    handler.exit(window)

    assert fake.rect == NORMAL_RECT


def test_enter_with_abandoned_session_saves_fresh_placement(fake, handler, window):
    handler.enter(window)
    # The OS re-maximized the window behind the app's back (Win+Up)
    fake.maximized = True
    fake.rect = MONITOR

    handler.enter(window)

    assert fake.maximized is False
    assert fake.rect == OVERHANG_RECT

    handler.exit(window)

    assert fake.maximized is True
    assert fake.placement[4] == NORMAL_RECT


@dataclass(frozen=True)
class IsActiveCase:
    name: str
    maximized: bool
    minimized: bool
    rect: tuple
    expected: bool
    expects_repin: bool


@pytest.mark.parametrize(
    "case",
    [
        IsActiveCase(
            name="covering_monitor_is_fullscreen",
            maximized=False,
            minimized=False,
            rect=OVERHANG_RECT,
            expected=True,
            expects_repin=False,
        ),
        IsActiveCase(
            name="minimized_session_survives",
            maximized=False,
            minimized=True,
            rect=MINIMIZED_RECT,
            expected=True,
            expects_repin=False,
        ),
        IsActiveCase(
            # Known limitation: the restored path deliberately skips the repin
            name="restored_window_retires_without_repin",
            maximized=False,
            minimized=False,
            rect=NORMAL_RECT,
            expected=False,
            expects_repin=False,
        ),
        IsActiveCase(
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
def test_is_active(case: IsActiveCase, fake, handler, window):
    handler.enter(window)
    fake.maximized = case.maximized
    fake.minimized = case.minimized
    fake.rect = case.rect

    assert handler.is_active(window) is case.expected

    expected_normal_rect = NORMAL_RECT if case.expects_repin else OVERHANG_RECT
    assert fake.placement[4] == expected_normal_rect
    if not case.expected:
        assert ("marker", False) in fake.calls
        assert not handler.is_active(window)
