# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass

import pytest
from PySide6.QtGui import QHideEvent, QShowEvent, QWindow
from PySide6.QtQuick import QQuickWindow

reveal_filter = pytest.importorskip(
    "mpvqc.services.platform.win.reveal_filter", reason="Requires the Windows platform modules"
)


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with):
    common_bindings_with()


@pytest.fixture
def cloak_calls(monkeypatch):
    calls: list[bool] = []
    monkeypatch.setattr(reveal_filter, "set_window_cloaked", lambda _hwnd, *, cloaked: calls.append(cloaked))
    monkeypatch.setattr(reveal_filter, "wait_for_next_composition", lambda: None)
    return calls


_ACTIONS = {
    "show": lambda window_filter, window: window_filter.eventFilter(window, QShowEvent()),
    "hide": lambda window_filter, window: window_filter.eventFilter(window, QHideEvent()),
    "frame": lambda _window_filter, window: window.frameSwapped.emit(),
}


@dataclass(frozen=True)
class RevealTestCase:
    name: str
    actions: tuple[str, ...]
    expected: list[bool]


@pytest.mark.parametrize(
    "case",
    [
        RevealTestCase("show_cloaks", actions=("show",), expected=[True]),
        RevealTestCase("first_frame_reveals", actions=("show", "frame"), expected=[True, False]),
        RevealTestCase("later_frames_are_ignored", actions=("show", "frame", "frame"), expected=[True, False]),
        RevealTestCase("hide_before_first_frame_reveals", actions=("show", "hide"), expected=[True, False]),
        RevealTestCase("frame_after_hide_is_ignored", actions=("show", "hide", "frame"), expected=[True, False]),
        RevealTestCase("reshow_cloaks_again", actions=("show", "frame", "show"), expected=[True, False, True]),
        RevealTestCase("show_while_pending_is_ignored", actions=("show", "show"), expected=[True]),
        RevealTestCase("hide_without_show_is_ignored", actions=("hide",), expected=[]),
    ],
    ids=lambda case: case.name,
)
def test_reveal_sequences(case: RevealTestCase, qt_app, cloak_calls):
    window_filter = reveal_filter.WindowRevealFilter()
    window = QQuickWindow()

    for action in case.actions:
        _ACTIONS[action](window_filter, window)

    assert cloak_calls == case.expected


def test_plain_windows_are_ignored(qt_app, cloak_calls):
    window_filter = reveal_filter.WindowRevealFilter()
    window = QWindow()

    window_filter.eventFilter(window, QShowEvent())

    assert cloak_calls == []
