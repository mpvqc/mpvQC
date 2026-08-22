# SPDX-FileCopyrightText: zhiyiYo
# SPDX-FileCopyrightText: Virace
# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Inspired and based on:
#  - https://github.com/zhiyiYo/PyQt-Frameless-Window
#  - https://gitee.com/Virace/pyside6-qml-frameless-window/tree/main

from __future__ import annotations

from typing import SupportsInt, override

import PySide6.QtCore

from mpvqc.window.services.windows_decisions import (
    CalculateFrameSize,
    HitTestFrame,
    PassThrough,
    PreventResize,
    handle_non_client_calculate_size,
    handle_non_client_hit_test,
    route_window_message,
)

from .native import WindowsMessageProbe, prevent_window_resize_for, write_nccalcsize_client_rect
from .probes import WindowsCalcSizeProbe, WindowsHitTestProbe


class WindowsEventFilter(PySide6.QtCore.QAbstractNativeEventFilter):
    def __init__(self) -> None:
        super().__init__()
        self._top_level_hwnd: int | None = None
        self._embedded_player_hwnd: int | None = None

    def set_top_level_hwnd(self, hwnd: int) -> None:
        self._top_level_hwnd = hwnd

    def set_embedded_player_hwnd(self, hwnd: int) -> None:
        self._embedded_player_hwnd = hwnd

    @override
    def nativeEventFilter(
        self, _: PySide6.QtCore.QByteArray | bytes | bytearray | memoryview, message: SupportsInt
    ) -> tuple[bool, int]:
        route = route_window_message(
            WindowsMessageProbe.from_address(int(message)),
            top_level_hwnd=self._top_level_hwnd,
            embedded_player_hwnd=self._embedded_player_hwnd,
        )

        match route:
            case PassThrough():
                return False, 0
            case PreventResize(hwnd=hwnd):
                prevent_window_resize_for(hwnd)
                return False, 0
            case HitTestFrame(hwnd=hwnd, l_param=l_param):
                return handle_non_client_hit_test(WindowsHitTestProbe(hwnd, l_param))
            case CalculateFrameSize(hwnd=hwnd, l_param=l_param):
                handled, result, client_rect = handle_non_client_calculate_size(WindowsCalcSizeProbe(hwnd, l_param))
                if client_rect is not None:
                    write_nccalcsize_client_rect(l_param, client_rect)
                return handled, result
