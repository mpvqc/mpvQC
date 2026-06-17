# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)


def is_tiling_window_manager() -> bool:
    tiling_wms = {
        "awesome",
        "bspwm",
        "dwm",
        "herbstluftwm",
        "hyprland",
        "i3",
        "niri",
        "qtile",
        "river",
        "sway",
        "wlroots",
        "xmonad",
    }

    xdg_current_desktop = os.environ.get("XDG_CURRENT_DESKTOP", "")
    desktops = {d.lower() for d in xdg_current_desktop.split(":")}
    is_tiling_wm = bool(desktops & tiling_wms)

    if is_tiling_wm:
        logger.info("Running on tiling window manager")

    return is_tiling_wm
