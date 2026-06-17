# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
import os
import sys

logger = logging.getLogger(__name__)

_IS_WINDOWS = sys.platform == "win32"

_WINDOWS_ROOT = "qrc:/qt/qml/MpvqcApplicationWindows.qml"
_LINUX_ROOT = "qrc:/qt/qml/MpvqcApplicationLinux.qml"


def is_tiling_window_manager() -> bool:
    if sys.platform != "linux":
        return False

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


def window_root_qml_url() -> str:
    return _WINDOWS_ROOT if _IS_WINDOWS else _LINUX_ROOT


def should_draw_own_shadow(*, is_tiling_wm: bool) -> bool:
    # Windows keeps the native DWM frame and its shadow. Generic Linux is
    # frameless and draws its own, except on tiling WMs where windows sit flush.
    return not _IS_WINDOWS and not is_tiling_wm


def should_draw_window_border() -> bool:
    # Windows draws a thin border to delineate the window from the desktop.
    # Linux draws its own shadow (or sits flush on tiling WMs) and needs none.
    return _IS_WINDOWS
