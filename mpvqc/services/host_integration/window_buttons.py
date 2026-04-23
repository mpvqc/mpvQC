# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Final


@dataclass(frozen=True)
class WindowButtonPreference:
    minimize: bool
    maximize: bool
    close: bool


DEFAULT_WINDOW_BUTTON_PREFERENCE: Final = WindowButtonPreference(minimize=True, maximize=True, close=True)


def read_window_button_preference() -> WindowButtonPreference:
    if sys.platform == "linux":
        return read_linux_window_button_preference()
    return DEFAULT_WINDOW_BUTTON_PREFERENCE


def read_linux_window_button_preference() -> WindowButtonPreference:
    from mpvqc.services.host_integration.portals import SettingsPortal

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
