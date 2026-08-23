# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class MessageProbe(Protocol):
    def hwnd(self) -> int | None: ...

    def message_id(self) -> int: ...

    def w_param(self) -> int: ...

    def l_param(self) -> int: ...


@dataclass(frozen=True)
class PassThrough:
    pass


@dataclass(frozen=True)
class PreventResize:
    hwnd: int


@dataclass(frozen=True)
class HitTestFrame:
    hwnd: int
    l_param: int


@dataclass(frozen=True)
class CalculateFrameSize:
    hwnd: int
    l_param: int


type MessageRoute = PassThrough | PreventResize | HitTestFrame | CalculateFrameSize

PASS_THROUGH = PassThrough()

_WM_STYLECHANGED = 0x007D
_WM_NCCREATE = 0x0081
_WM_NCCALCSIZE = 0x0083
_WM_NCHITTEST = 0x0084

_FRESH_STYLE_MESSAGE_IDS = frozenset({_WM_NCCREATE, _WM_STYLECHANGED})
ANSWERED_MESSAGE_IDS = frozenset({_WM_NCHITTEST, _WM_NCCALCSIZE, *_FRESH_STYLE_MESSAGE_IDS})


def route_window_message(
    probe: MessageProbe,
    *,
    top_level_hwnd: int | None,
    embedded_player_hwnd: int | None,
) -> MessageRoute:
    hwnd = probe.hwnd()
    if hwnd is None or hwnd == embedded_player_hwnd:
        return PASS_THROUGH
    if hwnd == top_level_hwnd:
        return _route_top_level(probe, hwnd)
    return _route_popup(probe, hwnd)


def _route_top_level(probe: MessageProbe, hwnd: int) -> MessageRoute:
    message_id = probe.message_id()
    if message_id == _WM_NCHITTEST:
        return HitTestFrame(hwnd=hwnd, l_param=probe.l_param())
    # Only with wParam TRUE does lParam point at NCCALCSIZE_PARAMS and may the
    # reply carry WVR_ flags; with it FALSE lParam is a plain rect and the reply
    # has to be zero.
    if message_id == _WM_NCCALCSIZE and probe.w_param():
        return CalculateFrameSize(hwnd=hwnd, l_param=probe.l_param())
    return PASS_THROUGH


def _route_popup(probe: MessageProbe, hwnd: int) -> MessageRoute:
    if probe.message_id() in _FRESH_STYLE_MESSAGE_IDS:
        return PreventResize(hwnd=hwnd)
    return PASS_THROUGH


def read_hit_test_point(l_param: int) -> tuple[int, int]:
    return _signed_16(l_param & 0xFFFF), _signed_16((l_param >> 16) & 0xFFFF)


def _signed_16(value: int) -> int:
    return value - 0x10000 if value & 0x8000 else value
