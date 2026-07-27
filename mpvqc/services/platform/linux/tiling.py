# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import os
import re

_SEPARATORS = re.compile(r"[:;]")

_TILING_DESKTOPS = frozenset(
    {
        "awesome",
        "bspwm",
        "cwc",
        "dwl",
        "dwm",
        "herbstluftwm",
        "hyprland",
        "i3",
        "japokwm",
        "leftwm",
        "mango",
        "miracle-wm",
        "niri",
        "notion",
        "qtile",
        "ratpoison",
        "river",
        "spectrwm",
        "stumpwm",
        "sway",
        "waymonad",
        "wlroots",
        "xmonad",
    }
)


def is_tiling_desktop() -> bool:
    xdg_current_desktop = os.environ.get("XDG_CURRENT_DESKTOP", "")
    desktops = {name.strip().lower() for name in _SEPARATORS.split(xdg_current_desktop)}
    return bool(desktops & _TILING_DESKTOPS)
