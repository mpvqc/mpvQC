# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass, field
from typing import NamedTuple

import pytest

from mpvqc.window.services.windows_decisions import (
    ANSWERED_MESSAGE_IDS,
    PASS_THROUGH,
    CalculateFrameSize,
    HitTestFrame,
    MessageRoute,
    PreventResize,
    route_window_message,
)

TOP_LEVEL = 0x00010001
EMBEDDED_PLAYER = 0x00020002
POPUP = 0x00030003

WM_PAINT = 0x000F
WM_STYLECHANGING = 0x007C
WM_STYLECHANGED = 0x007D
WM_NCCREATE = 0x0081
WM_NCCALCSIZE = 0x0083
WM_NCHITTEST = 0x0084
WM_TIMER = 0x0113
WM_USER = 0x0400

CURSOR_POINT = 0x01900140
CALC_SIZE_PARAMS = 0x7FFE1000


@dataclass
class RecordingMessageProbe:
    handle: int | None = TOP_LEVEL
    identifier: int = WM_PAINT
    word_param: int = 0
    long_param: int = 0
    asked: list[str] = field(default_factory=list)

    def hwnd(self) -> int | None:
        self.asked.append("hwnd")
        return self.handle

    def message_id(self) -> int:
        self.asked.append("message_id")
        return self.identifier

    def w_param(self) -> int:
        self.asked.append("w_param")
        return self.word_param

    def l_param(self) -> int:
        self.asked.append("l_param")
        return self.long_param


def route(
    probe: RecordingMessageProbe,
    *,
    top_level: int | None = TOP_LEVEL,
    embedded_player: int | None = EMBEDDED_PLAYER,
) -> MessageRoute:
    return route_window_message(probe, top_level_hwnd=top_level, embedded_player_hwnd=embedded_player)


def test_a_message_without_a_window_stops_at_the_handle():
    probe = RecordingMessageProbe(handle=None, identifier=WM_NCHITTEST)

    assert route(probe) is PASS_THROUGH
    assert probe.asked == ["hwnd"]


def test_the_embedded_player_answers_its_own_messages():
    probe = RecordingMessageProbe(handle=EMBEDDED_PLAYER, identifier=WM_NCHITTEST)

    assert route(probe) is PASS_THROUGH
    assert probe.asked == ["hwnd"]


def test_a_message_that_decides_nothing_asks_two_questions():
    probe = RecordingMessageProbe(identifier=WM_PAINT)

    assert route(probe) is PASS_THROUGH
    assert probe.asked == ["hwnd", "message_id"]


def test_the_hit_test_carries_the_window_and_the_cursor():
    probe = RecordingMessageProbe(identifier=WM_NCHITTEST, long_param=CURSOR_POINT)

    assert route(probe) == HitTestFrame(hwnd=TOP_LEVEL, l_param=CURSOR_POINT)
    assert probe.asked == ["hwnd", "message_id", "l_param"]


def test_the_size_calculation_carries_the_window_and_the_size_parameters():
    probe = RecordingMessageProbe(identifier=WM_NCCALCSIZE, word_param=1, long_param=CALC_SIZE_PARAMS)

    assert route(probe) == CalculateFrameSize(hwnd=TOP_LEVEL, l_param=CALC_SIZE_PARAMS)
    assert probe.asked == ["hwnd", "message_id", "w_param", "l_param"]


def test_a_size_calculation_without_the_frame_flag_stops_before_the_parameters():
    probe = RecordingMessageProbe(identifier=WM_NCCALCSIZE, word_param=0, long_param=CALC_SIZE_PARAMS)

    assert route(probe) is PASS_THROUGH
    assert probe.asked == ["hwnd", "message_id", "w_param"]


class MessageCase(NamedTuple):
    name: str
    identifier: int


@pytest.mark.parametrize(
    "case",
    [
        MessageCase(name="creation", identifier=WM_NCCREATE),
        MessageCase(name="style_changed", identifier=WM_STYLECHANGED),
    ],
    ids=lambda case: case.name,
)
def test_a_popup_gets_its_resize_style_stripped_when_its_style_can_have_changed(case: MessageCase):
    probe = RecordingMessageProbe(handle=POPUP, identifier=case.identifier)

    assert route(probe) == PreventResize(hwnd=POPUP)
    assert probe.asked == ["hwnd", "message_id"]


@pytest.mark.parametrize(
    "case",
    [
        MessageCase(name="paint", identifier=WM_PAINT),
        MessageCase(name="timer", identifier=WM_TIMER),
        MessageCase(name="hit_test", identifier=WM_NCHITTEST),
    ],
    ids=lambda case: case.name,
)
def test_a_popup_message_that_cannot_have_changed_its_style_passes_through(case: MessageCase):
    probe = RecordingMessageProbe(handle=POPUP, identifier=case.identifier)

    assert route(probe) is PASS_THROUGH
    assert probe.asked == ["hwnd", "message_id"]


def test_a_popup_style_changing_message_is_left_alone():
    probe = RecordingMessageProbe(handle=POPUP, identifier=WM_STYLECHANGING)

    assert route(probe) is PASS_THROUGH


@pytest.mark.parametrize(
    "case",
    [
        MessageCase(name="style_changing", identifier=WM_STYLECHANGING),
        MessageCase(name="style_changed", identifier=WM_STYLECHANGED),
    ],
    ids=lambda case: case.name,
)
def test_the_style_messages_of_the_top_level_window_still_pass_through(case: MessageCase):
    probe = RecordingMessageProbe(identifier=case.identifier)

    assert route(probe) is PASS_THROUGH


def test_a_window_seen_before_either_handle_is_tracked_counts_as_a_popup():
    probe = RecordingMessageProbe(handle=POPUP, identifier=WM_NCCREATE)

    assert route(probe, top_level=None, embedded_player=None) == PreventResize(hwnd=POPUP)


class WindowCase(NamedTuple):
    name: str
    handle: int | None


@pytest.mark.parametrize(
    "case",
    [
        WindowCase(name="no_window", handle=None),
        WindowCase(name="top_level", handle=TOP_LEVEL),
        WindowCase(name="embedded_player", handle=EMBEDDED_PLAYER),
        WindowCase(name="popup", handle=POPUP),
    ],
    ids=lambda case: case.name,
)
def test_every_system_message_outside_the_answered_set_passes_through(case: WindowCase):
    # The word parameter is raised so that a gate on it cannot hide a message
    # the set forgot.
    outside = [identifier for identifier in range(WM_USER) if identifier not in ANSWERED_MESSAGE_IDS]
    assert outside, "the set covers every system message; the sweep has nothing to check"

    answered = [
        identifier
        for identifier in outside
        if route(RecordingMessageProbe(handle=case.handle, identifier=identifier, word_param=1)) is not PASS_THROUGH
    ]

    assert answered == []


def test_every_message_in_the_answered_set_is_answered_by_some_window():
    assert ANSWERED_MESSAGE_IDS, "an empty set would pass this test without asking the routing anything"

    unanswered = [
        identifier
        for identifier in sorted(ANSWERED_MESSAGE_IDS)
        if all(
            route(RecordingMessageProbe(handle=handle, identifier=identifier, word_param=1)) is PASS_THROUGH
            for handle in (TOP_LEVEL, POPUP)
        )
    ]

    assert unanswered == []
