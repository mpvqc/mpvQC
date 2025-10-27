# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later


from mpvqc.services.host_integration.types import DEFAULT_WINDOW_BUTTON_PREFERENCE, OsBackend, WindowButtonPreference

from .utility import read_display_zoom_factor


class GenericDesktop(OsBackend):
    def get_display_zoom_factor(self) -> float:
        return read_display_zoom_factor()

    def get_window_button_preference(self) -> WindowButtonPreference:
        return DEFAULT_WINDOW_BUTTON_PREFERENCE
