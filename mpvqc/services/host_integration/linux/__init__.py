# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os

from mpvqc.services.host_integration.types import OsBackend, WindowButtonPreference


class LinuxBackend(OsBackend):
    def __init__(self):
        self._desktop_environment: OsBackend = get_desktop_environment()

    def get_display_zoom_factor(self) -> float:
        return self._desktop_environment.get_display_zoom_factor()

    def get_window_button_preference(self) -> WindowButtonPreference:
        return self._desktop_environment.get_window_button_preference()


def get_desktop_environment() -> OsBackend:
    desktop = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
    # fmt: off
    match desktop:
        case "gnome":
            from .gnome import GnomeDesktop
            return GnomeDesktop()
        case _:
            from .generic import GenericDesktop
            return GenericDesktop()
    # fmt: on


__all__ = [
    "LinuxBackend",
]
