# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os

from mpvqc.services.host_integration.types import DEFAULT_WINDOW_BUTTON_PREFERENCE, OsBackend, WindowButtonPreference

from .portals import SettingsPortal


class LinuxBackend(OsBackend):
    def get_display_zoom_factor(self) -> float:
        # Assume that people who use linux are fine with setting it this way
        # until there's an official way of figuring this out

        default_factor = 1.0

        try:
            factor = os.getenv("MPVQC_VIDEO_SCALING_FACTOR", default_factor)
            return float(factor)
        except ValueError:
            return default_factor

    def get_window_button_preference(self) -> WindowButtonPreference:
        with SettingsPortal() as portal:
            layout = portal.read_one("org.gnome.desktop.wm.preferences", "button-layout")

        if layout is None:
            return DEFAULT_WINDOW_BUTTON_PREFERENCE

        buttons = layout.lower()
        return WindowButtonPreference(
            minimize="minimize" in buttons,
            maximize="maximize" in buttons,
            close="close" in buttons,
        )


__all__ = [
    "LinuxBackend",
]
