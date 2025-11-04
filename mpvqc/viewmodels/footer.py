# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import IntEnum

import inject
from PySide6.QtCore import Property, QEnum, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import LabelWidthCalculatorService, PlayerService, SettingsService, TimeFormatterService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcFooterViewModel(QObject):
    _player: PlayerService = inject.attr(PlayerService)
    _settings: SettingsService = inject.attr(SettingsService)
    _formatter: TimeFormatterService = inject.attr(TimeFormatterService)
    _label_calculator: LabelWidthCalculatorService = inject.attr(LabelWidthCalculatorService)

    SECONDS_PER_HOUR = 3600

    class TimeFormat(IntEnum):
        EMPTY = 0
        CURRENT_TIME = 1
        REMAINING_TIME = 2
        CURRENT_TOTAL_TIME = 3

    QEnum(TimeFormat)

    selectedCommentIndexChanged = Signal(int)
    totalCommentCountChanged = Signal(int)
    commentCountTextChanged = Signal(str)
    isCommentCountVisibleChanged = Signal(bool)
    videoPercentTextChanged = Signal(str)
    isVideoPercentVisibleChanged = Signal(bool)
    timeFormatChanged = Signal(int)
    timeTextChanged = Signal(str)
    isTimeTextVisibleChanged = Signal(bool)
    timeWidthChanged = Signal(int)

    def __init__(self, /, parent=None):
        super().__init__(parent)
        self._selected_comment_index = 0
        self._total_comment_count = 0
        self._comment_count_text = ""
        self._is_comment_count_visible = False
        self._video_percent_text = ""
        self._is_video_percent_visible = self._player.video_loaded and self._settings.statusbar_percentage
        self._time_text = ""
        self._is_time_text_visible = self._player.video_loaded and self._settings.time_format != self.TimeFormat.EMPTY
        self._time_width = 0

        self._settings.statusbarPercentageChanged.connect(self._update_is_video_percent_visible)
        self._settings.timeFormatChanged.connect(self.timeFormatChanged)
        self._settings.timeFormatChanged.connect(self._update_is_time_text_visible)
        self._settings.timeFormatChanged.connect(self._update_time_text)
        self._settings.timeFormatChanged.connect(self._update_time_width)
        self._player.percent_pos_changed.connect(self._update_video_percent_text)
        self._player.video_loaded_changed.connect(self._update_is_time_text_visible)
        self._player.video_loaded_changed.connect(self._update_is_video_percent_visible)
        self._player.time_pos_changed.connect(self._update_time_text)
        self._player.time_remaining_changed.connect(self._update_time_text)
        self._player.duration_changed.connect(self._update_time_text)
        self._player.duration_changed.connect(self._update_time_width)

        self.selectedCommentIndexChanged.connect(self._update_comment_count_text)
        self.totalCommentCountChanged.connect(self._update_comment_count_text)
        self.totalCommentCountChanged.connect(self._update_is_comment_count_visible)

    @Property(int, notify=selectedCommentIndexChanged)
    def selectedCommentIndex(self) -> int:
        return self._selected_comment_index

    @selectedCommentIndex.setter
    def selectedCommentIndex(self, value: int) -> None:
        if self._selected_comment_index != value:
            self._selected_comment_index = value
            self.selectedCommentIndexChanged.emit(value)

    @Property(int, notify=totalCommentCountChanged)
    def totalCommentCount(self) -> int:
        return self._total_comment_count

    @totalCommentCount.setter
    def totalCommentCount(self, value: int) -> None:
        if self._total_comment_count != value:
            self._total_comment_count = value
            self.totalCommentCountChanged.emit(value)

    @Property(str, notify=commentCountTextChanged)
    def commentCountText(self) -> str:
        return self._comment_count_text

    @Slot()
    def _update_comment_count_text(self) -> None:
        new_text = f"{self._selected_comment_index + 1}/{self._total_comment_count}"
        if self._comment_count_text != new_text:
            self._comment_count_text = new_text
            self.commentCountTextChanged.emit(new_text)

    @Property(bool, notify=isCommentCountVisibleChanged)
    def isCommentCountVisible(self) -> bool:
        return self._is_comment_count_visible

    @Slot()
    def _update_is_comment_count_visible(self) -> None:
        new_visibility = self._total_comment_count > 0
        if self._is_comment_count_visible != new_visibility:
            self._is_comment_count_visible = new_visibility
            self.isCommentCountVisibleChanged.emit(new_visibility)

    @Property(str, notify=videoPercentTextChanged)
    def videoPercentText(self) -> str:
        return self._video_percent_text

    @Slot(int)
    def _update_video_percent_text(self, percent: int) -> None:
        new_text = f"{percent}%"
        if self._video_percent_text != new_text:
            self._video_percent_text = new_text
            self.videoPercentTextChanged.emit(new_text)

    @Property(bool, notify=isVideoPercentVisibleChanged)
    def isVideoPercentVisible(self) -> bool:
        return self._is_video_percent_visible

    @Slot()
    def _update_is_video_percent_visible(self) -> None:
        new_visibility = self._settings.statusbar_percentage and self._player.video_loaded
        if self._is_video_percent_visible != new_visibility:
            self._is_video_percent_visible = new_visibility
            self.isVideoPercentVisibleChanged.emit(new_visibility)

    @Property(int, notify=timeFormatChanged)
    def timeFormat(self) -> int:
        return self._settings.time_format

    @timeFormat.setter
    def timeFormat(self, value: int) -> None:
        self._settings.time_format = value

    @Property(str, notify=timeTextChanged)
    def timeText(self) -> str:
        return self._time_text

    @Slot()
    def _update_time_text(self) -> None:
        time_format = self._settings.time_format
        video_loaded = self._player.video_loaded
        long_format = self._player.duration >= self.SECONDS_PER_HOUR
        new_text = ""

        match (video_loaded, time_format):
            case (True, self.TimeFormat.CURRENT_TIME):
                new_text = self._formatter.format_time_to_string(self._player.time_pos or 0, long_format=long_format)
            case (True, self.TimeFormat.REMAINING_TIME):
                new_text = f"-{self._formatter.format_time_to_string(self._player.time_remaining or 0, long_format=long_format)}"
            case (True, self.TimeFormat.CURRENT_TOTAL_TIME):
                current_str = self._formatter.format_time_to_string(self._player.time_pos or 0, long_format=long_format)
                total_str = self._formatter.format_time_to_string(self._player.duration or 0, long_format=long_format)
                new_text = f"{current_str}/{total_str}"

        if self._time_text != new_text:
            self._time_text = new_text
            self.timeTextChanged.emit(new_text)

    @Property(bool, notify=isTimeTextVisibleChanged)
    def isTimeTextVisible(self) -> bool:
        return self._is_time_text_visible

    @Slot()
    def _update_is_time_text_visible(self) -> None:
        new_visibility = self._player.video_loaded and self._settings.time_format != self.TimeFormat.EMPTY
        if self._is_time_text_visible != new_visibility:
            self._is_time_text_visible = new_visibility
            self.isTimeTextVisibleChanged.emit(new_visibility)

    @Property(int, notify=timeWidthChanged)
    def timeWidth(self) -> int:
        return self._time_width

    @Slot()
    def _update_time_width(self) -> None:
        new_width = 0 if not self._time_text else self._label_calculator.calculate_width_for([self._time_text])

        if self._time_width != new_width:
            self._time_width = new_width
            self.timeWidthChanged.emit(new_width)

    @Slot()
    def toggleVideoPercentDisplay(self) -> None:
        self._settings.statusbar_percentage = not self._settings.statusbar_percentage
