# SPDX-FileCopyrightText: zhiyiYo
# SPDX-FileCopyrightText: Virace
# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Inspired and based on:
#  - https://github.com/zhiyiYo/PyQt-Frameless-Window
#  - https://gitee.com/Virace/pyside6-qml-frameless-window/tree/main

from __future__ import annotations

from typing import override

import PySide6.QtCore

from mpvqc.window.services.windows_decisions import handle_non_client_calculate_size, handle_non_client_hit_test

from .native import prevent_window_resize_for, read_window_message, write_nccalcsize_client_rect
from .probes import WindowsCalcSizeProbe, WindowsHitTestProbe

_WM_STYLECHANGING = 0x007C
_WM_STYLECHANGED = 0x007D
_WM_NCCALCSIZE = 0x0083
_WM_NCHITTEST = 0x0084


class WindowsEventFilter(PySide6.QtCore.QAbstractNativeEventFilter):
    def __init__(self) -> None:
        super().__init__()
        self._top_lvl_hwnd: int | None = None
        self._embedded_player_hwnd: int | None = None

    def set_top_lvl_hwnd(self, hwnd: int) -> None:
        self._top_lvl_hwnd = hwnd

    def set_embedded_player_hwnd(self, hwnd: int) -> None:
        self._embedded_player_hwnd = hwnd

    @override
    def nativeEventFilter(
        self, _: PySide6.QtCore.QByteArray | bytes | bytearray | memoryview, message: int
    ) -> tuple[bool, int]:
        msg = read_window_message(message)

        hwnd = msg.hwnd

        match hwnd:
            case None:
                return False, 0
            case self._embedded_player_hwnd:
                return False, 0
            case self._top_lvl_hwnd:
                pass
            case _:
                # Every other window is a popup, and popups must not be
                # resizable. The style is checked per message because Windows
                # reuses handle values and Qt can add the frame back at any
                # time.
                #
                # The style messages are skipped: SetWindowLong sends them back
                # into this filter synchronously, so handling them would call
                # SetWindowLong again, recursing until win32k's nested-message
                # limit.
                if msg.message not in {_WM_STYLECHANGING, _WM_STYLECHANGED}:
                    prevent_window_resize_for(hwnd)
                return False, 0

        if msg.message == _WM_NCHITTEST:
            return handle_non_client_hit_test(WindowsHitTestProbe(hwnd, msg.l_param))
        # Only with wParam TRUE does lParam point at NCCALCSIZE_PARAMS and may
        # the reply carry WVR_ flags; with it FALSE lParam is a plain rect and
        # the reply has to be zero.
        if msg.message == _WM_NCCALCSIZE and msg.w_param:
            handled, result, client_rect = handle_non_client_calculate_size(WindowsCalcSizeProbe(hwnd, msg.l_param))
            if client_rect is not None:
                write_nccalcsize_client_rect(msg.l_param, client_rect)
            return handled, result
        return False, 0
