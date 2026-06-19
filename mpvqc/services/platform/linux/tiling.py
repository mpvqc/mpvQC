# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import os

_TILING_WINDOW_MANAGERS = frozenset(
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
        "mangowc",
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


def is_tiling_window_manager() -> bool:
    xdg_current_desktop = os.environ.get("XDG_CURRENT_DESKTOP", "")
    desktops = {d.lower() for d in xdg_current_desktop.split(":")}
    return bool(desktops & _TILING_WINDOW_MANAGERS)
