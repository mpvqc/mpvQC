# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass, field
from typing import NamedTuple

import pytest

from mpvqc.window.services import (
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
WM_NCCALCSIZE = 0x0083
WM_NCHITTEST = 0x0084

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


def test_a_popup_gets_its_resize_style_stripped():
    probe = RecordingMessageProbe(handle=POPUP, identifier=WM_PAINT)

    assert route(probe) == PreventResize(hwnd=POPUP)
    assert probe.asked == ["hwnd", "message_id"]


class StyleMessageCase(NamedTuple):
    name: str
    identifier: int


@pytest.mark.parametrize(
    "case",
    [
        StyleMessageCase(name="style_changing", identifier=WM_STYLECHANGING),
        StyleMessageCase(name="style_changed", identifier=WM_STYLECHANGED),
    ],
    ids=lambda case: case.name,
)
def test_a_popup_style_message_is_left_alone(case: StyleMessageCase):
    probe = RecordingMessageProbe(handle=POPUP, identifier=case.identifier)

    assert route(probe) is PASS_THROUGH


def test_the_style_messages_of_the_top_level_window_still_pass_through():
    probe = RecordingMessageProbe(identifier=WM_STYLECHANGING)

    assert route(probe) is PASS_THROUGH


def test_a_window_seen_before_either_handle_is_tracked_counts_as_a_popup():
    probe = RecordingMessageProbe(handle=POPUP, identifier=WM_NCHITTEST)

    assert route(probe, top_level=None, embedded_player=None) == PreventResize(hwnd=POPUP)
