# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from .frame_geometry import Rect

SW_MAXIMIZE = 3
WPF_RESTORETOMAXIMIZED = 0x0002


class WindowPlacement(NamedTuple):
    flags: int
    show_cmd: int
    min_position: tuple[int, int]
    max_position: tuple[int, int]
    normal_rect: Rect

    @property
    def shows_maximized(self) -> bool:
        return self.show_cmd == SW_MAXIMIZE

    @property
    def restores_to_maximized(self) -> bool:
        return bool(self.flags & WPF_RESTORETOMAXIMIZED)
