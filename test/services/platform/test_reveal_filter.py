# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
from dataclasses import dataclass

import pytest
from PySide6.QtCore import QCoreApplication, QEvent
from PySide6.QtGui import QShowEvent, QWindow
from PySide6.QtQuick import QQuickItem, QQuickWindow

if sys.platform != "win32":
    pytest.skip("Requires Windows", allow_module_level=True)

from mpvqc.services.platform.win import reveal_filter


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with):
    common_bindings_with()


@pytest.fixture
def cloak_calls(monkeypatch):
    calls: list[bool] = []
    monkeypatch.setattr(reveal_filter, "set_window_cloaked", lambda _hwnd, *, cloaked: calls.append(cloaked))
    monkeypatch.setattr(reveal_filter, "wait_for_next_composition", lambda: None)
    return calls


@pytest.fixture
def make_reveal_setup(qt_app):
    # The filter and each window reference each other through signal connections;
    # let Qt tear them down on the event loop so Python's cyclic GC never has to
    # destroy two interconnected QObjects in an arbitrary order (which faults).
    created = []

    def _make():
        window_filter = reveal_filter.WindowRevealFilter()
        window = QQuickWindow()
        # setParentItem only sets the visual parent, not the QObject parent, so
        # PySide keeps Python ownership: the list holds a reference, or the item
        # is garbage-collected and drops out of the window's contentItem.
        content = QQuickItem()
        content.setParentItem(window.contentItem())
        created.append((window_filter, window, content))
        return window_filter, window

    yield _make

    for window_filter, window, _content in created:
        window.deleteLater()
        window_filter.deleteLater()
    QCoreApplication.processEvents()


def _apply_action(action: str, window_filter, window) -> None:
    if action == "show":
        window_filter.eventFilter(window, QShowEvent())
    elif action == "frame":
        # frameSwapped is a queued connection; deliver only that slot call to the
        # filter rather than pumping the whole loop, which would also fire the real
        # window's own visibleChanged and corrupt the synthetic sequence.
        window.frameSwapped.emit()
        QCoreApplication.sendPostedEvents(window_filter, QEvent.Type.MetaCall)
    elif action == "hide":
        window.visibleChanged.emit(False)
    elif action == "teardown":
        for item in window.contentItem().childItems():
            item.setParentItem(None)
    else:
        msg = f"Unknown action: {action}"
        raise ValueError(msg)


@dataclass(frozen=True)
class RevealTestCase:
    name: str
    is_main: bool
    actions: tuple[str, ...]
    expected: list[bool]


@pytest.mark.parametrize(
    "case",
    [
        RevealTestCase(
            name="main_show_cloaks",
            is_main=True,
            actions=("show",),
            expected=[True],
        ),
        RevealTestCase(
            name="main_first_frame_reveals",
            is_main=True,
            actions=("show", "frame"),
            expected=[True, False],
        ),
        RevealTestCase(
            name="main_later_frames_are_ignored",
            is_main=True,
            actions=("show", "frame", "frame"),
            expected=[True, False],
        ),
        RevealTestCase(
            name="main_reshow_cloaks_again",
            is_main=True,
            actions=("show", "frame", "show"),
            expected=[True, False, True],
        ),
        RevealTestCase(
            name="main_show_while_pending_is_ignored",
            is_main=True,
            actions=("show", "show"),
            expected=[True],
        ),
        RevealTestCase(
            name="main_hide_is_ignored",
            is_main=True,
            actions=("show", "frame", "hide"),
            expected=[True, False],
        ),
        RevealTestCase(
            name="transient_show_cloaks",
            is_main=False,
            actions=("show",),
            expected=[True],
        ),
        RevealTestCase(
            name="transient_hide_conceals_again",
            is_main=False,
            actions=("show", "frame", "hide"),
            expected=[True, False, True],
        ),
        RevealTestCase(
            name="transient_hidden_before_first_frame_stays_concealed",
            is_main=False,
            actions=("show", "hide"),
            expected=[True, True],
        ),
        RevealTestCase(
            name="transient_frame_after_hide_is_ignored",
            is_main=False,
            actions=("show", "hide", "frame"),
            expected=[True, True],
        ),
        RevealTestCase(
            name="transient_reopen_repeats_the_cycle",
            is_main=False,
            actions=("show", "frame", "hide", "show", "frame"),
            expected=[True, False, True, True, False],
        ),
        RevealTestCase(
            name="transient_content_teardown_conceals",
            is_main=False,
            actions=("show", "frame", "teardown"),
            expected=[True, False, True],
        ),
        RevealTestCase(
            name="transient_frame_after_teardown_is_ignored",
            is_main=False,
            actions=("show", "teardown", "frame"),
            expected=[True, True],
        ),
        RevealTestCase(
            name="empty_transient_reshow_never_arms_a_reveal",
            is_main=False,
            actions=("show", "frame", "teardown", "show", "frame"),
            expected=[True, False, True, True],
        ),
    ],
    ids=lambda case: case.name,
)
def test_reveal_sequences(case: RevealTestCase, cloak_calls, make_reveal_setup):
    window_filter, window = make_reveal_setup()

    if case.is_main:
        window_filter.set_main_window_hwnd(int(window.winId()))

    for action in case.actions:
        _apply_action(action, window_filter, window)

    assert cloak_calls == case.expected


def test_non_quick_windows_are_ignored(cloak_calls, make_reveal_setup):
    window_filter, _window = make_reveal_setup()

    window_filter.eventFilter(QWindow(), QShowEvent())

    assert cloak_calls == []
