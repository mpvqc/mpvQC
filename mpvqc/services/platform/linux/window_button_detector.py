# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal

from mpvqc.jobs import Err, Ok, SerialJobRunner
from mpvqc.services.platform.window_buttons import DEFAULT_WINDOW_BUTTON_PREFERENCE, WindowButtonPreference

from .portals import SettingsPortal

if TYPE_CHECKING:
    from mpvqc.jobs import JobExecutor, Result

logger = logging.getLogger(__name__)


class WindowButtonDetector(QObject):
    preference_changed = Signal(WindowButtonPreference)

    def __init__(self, executor: JobExecutor | None = None) -> None:
        super().__init__()
        self._preference = DEFAULT_WINDOW_BUTTON_PREFERENCE
        self._jobs = SerialJobRunner(executor)

    def detect(self) -> None:
        self._jobs.run(work=self._read_preference, on_result=self._apply_preference)

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

    def _apply_preference(self, result: Result[WindowButtonPreference]) -> None:
        match result:
            case Ok(preference):
                if preference != self._preference:
                    self._preference = preference
                    self.preference_changed.emit(preference)
            case Err(error):
                logger.error("Window button detection failed", exc_info=error)

    @property
    def preference(self) -> WindowButtonPreference:
        return self._preference
