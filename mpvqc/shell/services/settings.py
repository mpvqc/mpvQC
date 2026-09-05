# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from contextlib import suppress
from enum import IntEnum
from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Qt, Signal

from .vocabulary import TimeDisplayMode, WindowTitleFormat

if TYPE_CHECKING:
    from PySide6.QtCore import QSettings

_SHOW_PERCENTAGE_KEY = "StatusBar/statusbarPercentage"
_TIME_DISPLAY_MODE_KEY = "StatusBar/timeFormat"
_LAYOUT_ORIENTATION_KEY = "SplitView/layoutOrientation"
_WINDOW_TITLE_FORMAT_KEY = "Window/titleFormat"


# Until something writes the key this run, an untyped read hands back the ini text, never the type that was stored
def _read_bool(stored: object, default: bool) -> bool:
    if isinstance(stored, bool):
        return stored
    if isinstance(stored, str) and stored.lower() in {"true", "false"}:
        return stored.lower() == "true"
    return default


def _read_int(stored: object, default: int) -> int:
    if isinstance(stored, bool):
        return default
    if isinstance(stored, int):
        return stored
    if isinstance(stored, str):
        with suppress(ValueError):
            return int(stored)
    return default


def _read_member[M: IntEnum](stored: object, of: type[M], default: M) -> M:
    # Reading with type=int would coerce a corrupted value to 0, which both enums name
    if isinstance(stored, bool):
        return default
    if isinstance(stored, str | int):
        with suppress(ValueError):
            return of(int(stored))
    return default


class ShellSettingsService(QObject):
    show_percentage_changed = Signal(bool)
    time_display_mode_changed = Signal(int)
    layout_orientation_changed = Signal(int)
    window_title_format_changed = Signal(int)

    def __init__(self, qsettings: QSettings, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._qsettings = qsettings

    @property
    def show_percentage(self) -> bool:
        return _read_bool(self._qsettings.value(_SHOW_PERCENTAGE_KEY), default=True)

    @show_percentage.setter
    def show_percentage(self, show: bool) -> None:
        if self.show_percentage == show:
            return
        self._qsettings.setValue(_SHOW_PERCENTAGE_KEY, show)
        self.show_percentage_changed.emit(show)

    @property
    def time_display_mode(self) -> TimeDisplayMode:
        stored = self._qsettings.value(_TIME_DISPLAY_MODE_KEY)
        return _read_member(stored, TimeDisplayMode, default=TimeDisplayMode.CURRENT_TOTAL_TIME)

    @time_display_mode.setter
    def time_display_mode(self, mode: TimeDisplayMode) -> None:
        if self.time_display_mode == mode:
            return
        self._qsettings.setValue(_TIME_DISPLAY_MODE_KEY, mode.value)
        self.time_display_mode_changed.emit(mode)

    @property
    def layout_orientation(self) -> int:
        return _read_int(self._qsettings.value(_LAYOUT_ORIENTATION_KEY), default=Qt.Orientation.Vertical.value)

    @layout_orientation.setter
    def layout_orientation(self, orientation: int) -> None:
        if self.layout_orientation == orientation:
            return
        self._qsettings.setValue(_LAYOUT_ORIENTATION_KEY, orientation)
        self.layout_orientation_changed.emit(orientation)

    @property
    def window_title_format(self) -> WindowTitleFormat:
        stored = self._qsettings.value(_WINDOW_TITLE_FORMAT_KEY)
        return _read_member(stored, WindowTitleFormat, default=WindowTitleFormat.DEFAULT)

    @window_title_format.setter
    def window_title_format(self, title_format: WindowTitleFormat) -> None:
        if self.window_title_format == title_format:
            return
        self._qsettings.setValue(_WINDOW_TITLE_FORMAT_KEY, title_format.value)
        self.window_title_format_changed.emit(title_format)
