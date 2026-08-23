# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
from dataclasses import dataclass, field
from typing import NamedTuple

import pytest

if sys.platform != "win32":
    pytest.skip("Requires Windows", allow_module_level=True)

from ctypes import addressof
from ctypes.wintypes import MSG

from mpvqc.window.services.windows import WindowsEventFilter
from mpvqc.window.services.windows_decisions import route_window_message

EVENT = "mpvqc.window.services.windows.event"

TOP_LEVEL = 0x00010001
POPUP = 0x00030003

WM_PAINT = 0x000F
WM_NCCREATE = 0x0081
WM_NCHITTEST = 0x0084
WM_TIMER = 0x0113

UNHANDLED_REPLY = (False, 0)
HIT_TEST_REPLY = (True, 12)


@dataclass
class Recorder:
    routed: list[tuple[int | None, int]] = field(default_factory=list)
    stripped: list[int] = field(default_factory=list)
    hit_tested: list[int] = field(default_factory=list)


@pytest.fixture
def recorder(monkeypatch) -> Recorder:
    recorder = Recorder()

    def route(probe, *, top_level_hwnd, embedded_player_hwnd):
        recorder.routed.append((probe.hwnd(), probe.message_id()))
        return route_window_message(probe, top_level_hwnd=top_level_hwnd, embedded_player_hwnd=embedded_player_hwnd)

    def hit_test(probe):
        recorder.hit_tested.append(probe.hwnd)
        return HIT_TEST_REPLY

    monkeypatch.setattr(f"{EVENT}.route_window_message", route)
    monkeypatch.setattr(f"{EVENT}.prevent_window_resize_for", recorder.stripped.append)
    monkeypatch.setattr(f"{EVENT}.handle_non_client_hit_test", hit_test)
    return recorder


@pytest.fixture
def event_filter() -> WindowsEventFilter:
    event_filter = WindowsEventFilter()
    event_filter.set_top_level_hwnd(TOP_LEVEL)
    return event_filter


def deliver(event_filter: WindowsEventFilter, *, hwnd: int, message_id: int) -> tuple[bool, int]:
    message = MSG(hWnd=hwnd, message=message_id, wParam=0, lParam=0)
    return event_filter.nativeEventFilter(b"windows_generic_MSG", addressof(message))


class UnansweredCase(NamedTuple):
    name: str
    hwnd: int
    message_id: int


@pytest.mark.parametrize(
    "case",
    [
        UnansweredCase(name="paint_to_the_main_window", hwnd=TOP_LEVEL, message_id=WM_PAINT),
        UnansweredCase(name="timer_to_a_popup", hwnd=POPUP, message_id=WM_TIMER),
    ],
    ids=lambda case: case.name,
)
def test_a_message_the_filter_never_answers_stops_before_the_routing(case: UnansweredCase, recorder, event_filter):
    reply = deliver(event_filter, hwnd=case.hwnd, message_id=case.message_id)

    assert reply == UNHANDLED_REPLY
    assert recorder.routed == []
    assert recorder.stripped == []


def test_a_popup_being_created_gets_its_resize_style_stripped(recorder, event_filter):
    reply = deliver(event_filter, hwnd=POPUP, message_id=WM_NCCREATE)

    assert reply == UNHANDLED_REPLY
    assert recorder.routed == [(POPUP, WM_NCCREATE)]
    assert recorder.stripped == [POPUP]


def test_a_hit_test_on_the_main_window_is_routed_to_its_handler(recorder, event_filter):
    reply = deliver(event_filter, hwnd=TOP_LEVEL, message_id=WM_NCHITTEST)

    assert reply == HIT_TEST_REPLY
    assert recorder.routed == [(TOP_LEVEL, WM_NCHITTEST)]
    assert recorder.hit_tested == [TOP_LEVEL]
