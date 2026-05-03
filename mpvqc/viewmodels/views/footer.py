# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.enums import MpvqcTimeFormat
from mpvqc.services import LabelWidthCalculatorService, PlayerService, SettingsService, TimeFormatterService

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1

TimeFormat = MpvqcTimeFormat.TimeFormat
SECONDS_PER_HOUR = 3600


@QmlElement
class MpvqcFooterViewModel(QObject):
    _player = inject.attr(PlayerService)
    _settings = inject.attr(SettingsService)
    _formatter = inject.attr(TimeFormatterService)
    _label_calculator = inject.attr(LabelWidthCalculatorService)

    statusbarPercentageChanged = Signal(bool)
    timeFormatChanged = Signal(int)
    isPercentVisibleChanged = Signal(bool)
    percentTextChanged = Signal(str)
    isTimeVisibleChanged = Signal(bool)
    timeTextChanged = Signal(str)
    timeWidthChanged = Signal(int)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self._statusbar_percentage = self._settings.statusbar_percentage
        self._time_format = self._settings.time_format
        self._video_loaded = self._player.video_loaded
        self._percent_pos = self._player.percent_pos or 0
        self._time_pos = self._player.time_pos or 0
        self._time_remaining = self._player.time_remaining or 0
        self._duration = self._player.duration

        self._is_percent_visible = self._video_loaded and self._statusbar_percentage
        self._percent_text = f"{self._percent_pos}%"
        self._is_time_visible = self._video_loaded and self._time_format != TimeFormat.EMPTY
        self._time_text = self._derive_time_text()
        self._time_width = self._derive_time_width()

        self._settings.statusbarPercentageChanged.connect(self.setStatusbarPercentage)
        self._settings.timeFormatChanged.connect(self.setTimeFormat)
        self._player.video_loaded_changed.connect(self.setVideoLoaded)
        self._player.percent_pos_changed.connect(self.setPercentPos)
        self._player.time_pos_changed.connect(self.setTimePos)
        self._player.time_remaining_changed.connect(self.setTimeRemaining)
        self._player.duration_changed.connect(self.setDuration)

    @Property(bool, notify=statusbarPercentageChanged)
    def statusbarPercentage(self) -> bool:
        return self._statusbar_percentage

    @Property(int, notify=timeFormatChanged)
    def timeFormat(self) -> int:
        return self._time_format

    @timeFormat.setter
    def timeFormat(self, value: int) -> None:
        self._settings.time_format = value

    @Property(bool, notify=isPercentVisibleChanged)
    def isPercentVisible(self) -> bool:
        return self._is_percent_visible

    @Property(str, notify=percentTextChanged)
    def percentText(self) -> str:
        return self._percent_text

    @Property(bool, notify=isTimeVisibleChanged)
    def isTimeVisible(self) -> bool:
        return self._is_time_visible

    @Property(str, notify=timeTextChanged)
    def timeText(self) -> str:
        return self._time_text

    @Property(int, notify=timeWidthChanged)
    def timeWidth(self) -> int:
        return self._time_width

    @Slot(bool)
    def setStatusbarPercentage(self, value: bool) -> None:
        if self._statusbar_percentage == value:
            return
        self._statusbar_percentage = value
        self.statusbarPercentageChanged.emit(value)
        self._update_is_percent_visible()

    @Slot(int)
    def setTimeFormat(self, value: int) -> None:
        if self._time_format == value:
            return
        self._time_format = value
        self.timeFormatChanged.emit(value)
        self._update_is_time_visible()
        self._update_time_text()
        self._update_time_width()

    @Slot(bool)
    def setVideoLoaded(self, value: bool) -> None:
        if self._video_loaded == value:
            return
        self._video_loaded = value
        self._update_is_percent_visible()
        self._update_is_time_visible()
        self._update_time_text()
        self._update_time_width()

    @Slot(int)
    def setPercentPos(self, value: int) -> None:
        if self._percent_pos == value:
            return
        self._percent_pos = value
        self._update_percent_text()

    @Slot(int)
    def setTimePos(self, value: int) -> None:
        if self._time_pos == value:
            return
        self._time_pos = value
        self._update_time_text()

    @Slot(int)
    def setTimeRemaining(self, value: int) -> None:
        if self._time_remaining == value:
            return
        self._time_remaining = value
        self._update_time_text()

    @Slot(float)
    def setDuration(self, value: float) -> None:
        if self._duration == value:
            return
        self._duration = value
        self._update_time_text()
        self._update_time_width()

    @Slot()
    def toggleStatusbarPercentage(self) -> None:
        self._settings.statusbar_percentage = not self._statusbar_percentage

    def _update_is_percent_visible(self) -> None:
        new_value = self._video_loaded and self._statusbar_percentage
        if self._is_percent_visible == new_value:
            return
        self._is_percent_visible = new_value
        self.isPercentVisibleChanged.emit(new_value)

    def _update_percent_text(self) -> None:
        new_value = f"{self._percent_pos}%"
        if self._percent_text == new_value:
            return
        self._percent_text = new_value
        self.percentTextChanged.emit(new_value)

    def _update_is_time_visible(self) -> None:
        new_value = self._video_loaded and self._time_format != TimeFormat.EMPTY
        if self._is_time_visible == new_value:
            return
        self._is_time_visible = new_value
        self.isTimeVisibleChanged.emit(new_value)

    def _update_time_text(self) -> None:
        new_value = self._derive_time_text()
        if self._time_text == new_value:
            return
        self._time_text = new_value
        self.timeTextChanged.emit(new_value)

    def _update_time_width(self) -> None:
        new_value = self._derive_time_width()
        if self._time_width == new_value:
            return
        self._time_width = new_value
        self.timeWidthChanged.emit(new_value)

    def _derive_time_text(self) -> str:
        if not self._video_loaded:
            return ""
        long_format = self._duration >= SECONDS_PER_HOUR
        match self._time_format:
            case TimeFormat.CURRENT_TIME:
                return self._formatter.format_time_to_string(self._time_pos, long_format=long_format)
            case TimeFormat.REMAINING_TIME:
                return f"-{self._formatter.format_time_to_string(self._time_remaining, long_format=long_format)}"
            case TimeFormat.CURRENT_TOTAL_TIME:
                current = self._formatter.format_time_to_string(self._time_pos, long_format=long_format)
                total = self._formatter.format_time_to_string(self._duration, long_format=long_format)
                return f"{current}/{total}"
            case _:
                return ""

    def _derive_time_width(self) -> int:
        if not self._time_text:
            return 0
        return self._label_calculator.calculate_width_for([self._time_text])
