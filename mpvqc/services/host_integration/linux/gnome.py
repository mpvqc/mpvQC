# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later


from mpvqc.services.host_integration.types import DEFAULT_WINDOW_BUTTON_PREFERENCE, OsBackend, WindowButtonPreference

from .portals import SettingsPortal
from .utility import read_display_zoom_factor


class GnomeDesktop(OsBackend):
    def get_display_zoom_factor(self) -> float:
        return read_display_zoom_factor()

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
