# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, Self

from PySide6.QtCore import QObject, Qt, Signal

from mpvqc.settings import Setting, read_bool, read_int, read_member

from .vocabulary import TimeDisplayMode, WindowTitleFormat

if TYPE_CHECKING:
    from PySide6.QtCore import QSettings


class ShellSettingsService(QObject):
    show_percentage_changed = Signal(bool)
    time_display_mode_changed = Signal(int)
    layout_orientation_changed = Signal(int)
    window_title_format_changed = Signal(int)

    def __init__(self, qsettings: QSettings, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.qsettings = qsettings

    def _notify_show_percentage(self, show: bool) -> None:
        self.show_percentage_changed.emit(show)

    def _notify_time_display_mode(self, mode: TimeDisplayMode) -> None:
        self.time_display_mode_changed.emit(mode.value)

    def _notify_layout_orientation(self, orientation: int) -> None:
        self.layout_orientation_changed.emit(orientation)

    def _notify_window_title_format(self, title_format: WindowTitleFormat) -> None:
        self.window_title_format_changed.emit(title_format.value)

    # PySide's metadata scanner cannot parse generic calls in unannotated class assignments.
    show_percentage: Setting[Self, bool] = Setting[Self, bool](
        "StatusBar/statusbarPercentage",
        default=lambda: True,
        decode=read_bool,
        notify=_notify_show_percentage,
    )

    time_display_mode: Setting[Self, TimeDisplayMode] = Setting[Self, TimeDisplayMode](
        "StatusBar/timeFormat",
        default=lambda: TimeDisplayMode.CURRENT_TOTAL_TIME,
        decode=lambda stored, default: read_member(stored, TimeDisplayMode, default),
        encode=lambda mode: mode.value,
        notify=_notify_time_display_mode,
    )

    layout_orientation: Setting[Self, int] = Setting[Self, int](
        "SplitView/layoutOrientation",
        default=lambda: Qt.Orientation.Vertical.value,
        decode=read_int,
        notify=_notify_layout_orientation,
    )

    window_title_format: Setting[Self, WindowTitleFormat] = Setting[Self, WindowTitleFormat](
        "Window/titleFormat",
        default=lambda: WindowTitleFormat.DEFAULT,
        decode=lambda stored, default: read_member(stored, WindowTitleFormat, default),
        encode=lambda title_format: title_format.value,
        notify=_notify_window_title_format,
    )
