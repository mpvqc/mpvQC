# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from PySide6.QtCore import QObject, Qt, QThreadPool, Signal, Slot

from mpvqc.services.platform.window_buttons import DEFAULT_WINDOW_BUTTON_PREFERENCE, WindowButtonPreference

from .portals import SettingsPortal


class WindowButtonDetector(QObject):
    preference_changed = Signal(WindowButtonPreference)
    _preference_detected = Signal(WindowButtonPreference)

    def __init__(self) -> None:
        super().__init__()
        self._preference = DEFAULT_WINDOW_BUTTON_PREFERENCE
        self._preference_detected.connect(self._apply_preference, Qt.ConnectionType.QueuedConnection)

    def detect(self) -> None:
        QThreadPool.globalInstance().start(self._run_detection)

    def _run_detection(self) -> None:
        self._preference_detected.emit(self._read_preference())

    @staticmethod
    def _read_preference() -> WindowButtonPreference:
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

    @Slot(WindowButtonPreference)
    def _apply_preference(self, preference: WindowButtonPreference) -> None:
        if preference != self._preference:
            self._preference = preference
            self.preference_changed.emit(preference)

    @property
    def preference(self) -> WindowButtonPreference:
        return self._preference
