# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Qt, QThreadPool, Signal, Slot

if TYPE_CHECKING:
    from typing import Final


@dataclass(frozen=True)
class WindowButtonPreference:
    minimize: bool
    maximize: bool
    close: bool


DEFAULT_WINDOW_BUTTON_PREFERENCE: Final = WindowButtonPreference(minimize=True, maximize=True, close=True)


def read_linux_window_button_preference() -> WindowButtonPreference:
    from mpvqc.services.platform.linux.portals import SettingsPortal

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


class WindowButtonDetector(QObject):
    preference_changed = Signal(object)
    _preference_detected = Signal(object)

    def __init__(self) -> None:
        super().__init__()
        self._preference = DEFAULT_WINDOW_BUTTON_PREFERENCE
        self._preference_detected.connect(self._apply_preference, Qt.ConnectionType.QueuedConnection)

    def detect(self) -> None:
        if sys.platform != "linux":
            return
        QThreadPool.globalInstance().start(self._read_preference)

    def _read_preference(self) -> None:
        self._preference_detected.emit(read_linux_window_button_preference())

    @Slot(object)
    def _apply_preference(self, preference: WindowButtonPreference) -> None:
        if preference != self._preference:
            self._preference = preference
            self.preference_changed.emit(preference)

    @property
    def preference(self) -> WindowButtonPreference:
        return self._preference
