# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable
from dataclasses import dataclass, replace

import inject
from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.player.services import PlayerService
from mpvqc.services import LabelWidthCalculatorService, TimeFormatterService
from mpvqc.shared import needs_long_format
from mpvqc.shell.services import ShellSettingsService, TimeDisplayMode

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@dataclass(frozen=True)
class FooterInputs:
    video_loaded: bool
    percent_pos: int
    time_pos: int
    time_remaining: int
    duration: float
    statusbar_percentage: bool
    time_display_mode: int


@dataclass(frozen=True)
class FooterProps:
    statusbar_percentage: bool
    time_display_mode: int
    is_percent_visible: bool
    percent_text: str
    is_time_visible: bool
    time_text: str
    time_width: int


def derive_footer_props(inputs: FooterInputs, measure_width: Callable[[str], int]) -> FooterProps:
    time_text = _derive_time_text(inputs)
    return FooterProps(
        statusbar_percentage=inputs.statusbar_percentage,
        time_display_mode=inputs.time_display_mode,
        is_percent_visible=inputs.video_loaded and inputs.statusbar_percentage,
        percent_text=f"{inputs.percent_pos}%",
        is_time_visible=inputs.video_loaded and inputs.time_display_mode != TimeDisplayMode.NONE,
        time_text=time_text,
        time_width=measure_width(time_text) if time_text else 0,
    )


def _derive_time_text(inputs: FooterInputs) -> str:
    if not inputs.video_loaded:
        return ""
    long_format = needs_long_format(inputs.duration)
    to_string = TimeFormatterService.format_time_to_string
    match inputs.time_display_mode:
        case TimeDisplayMode.CURRENT_TIME:
            return to_string(inputs.time_pos, long_format=long_format)
        case TimeDisplayMode.REMAINING_TIME:
            return f"-{to_string(inputs.time_remaining, long_format=long_format)}"
        case TimeDisplayMode.CURRENT_TOTAL_TIME:
            current = to_string(inputs.time_pos, long_format=long_format)
            total = to_string(inputs.duration, long_format=long_format)
            return f"{current}/{total}"
        case _:
            return ""


@QmlElement
class MpvqcFooterViewModel(QObject):
    _player = inject.attr(PlayerService)
    _settings = inject.attr(ShellSettingsService)
    _label_calculator = inject.attr(LabelWidthCalculatorService)

    statusbarPercentageChanged = Signal(bool)
    timeDisplayModeChanged = Signal(int)
    isPercentVisibleChanged = Signal(bool)
    percentTextChanged = Signal(str)
    isTimeVisibleChanged = Signal(bool)
    timeTextChanged = Signal(str)
    timeWidthChanged = Signal(int)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self._inputs = FooterInputs(
            video_loaded=self._player.video_loaded,
            percent_pos=self._player.percent_pos,
            time_pos=self._player.time_pos,
            time_remaining=self._player.time_remaining,
            duration=self._player.duration,
            statusbar_percentage=self._settings.show_percentage,
            time_display_mode=self._settings.time_display_mode,
        )
        self._props = self._derive()

        self._settings.show_percentage_changed.connect(self._fold_statusbar_percentage)
        self._settings.time_display_mode_changed.connect(self._fold_time_display_mode)
        self._player.video_loaded_changed.connect(self._fold_video_loaded)
        self._player.percent_pos_changed.connect(self._fold_percent_pos)
        self._player.time_pos_changed.connect(self._fold_time_pos)
        self._player.time_remaining_changed.connect(self._fold_time_remaining)
        self._player.duration_changed.connect(self._fold_duration)

    def _derive(self) -> FooterProps:
        return derive_footer_props(self._inputs, self._measure_width)

    def _measure_width(self, text: str) -> int:
        return self._label_calculator.calculate_width_for((text,))

    @Slot(bool)
    def _fold_statusbar_percentage(self, value: bool) -> None:
        self._update(replace(self._inputs, statusbar_percentage=value))

    @Slot(int)
    def _fold_time_display_mode(self, value: int) -> None:
        self._update(replace(self._inputs, time_display_mode=value))

    @Slot(bool)
    def _fold_video_loaded(self, value: bool) -> None:
        self._update(replace(self._inputs, video_loaded=value))

    @Slot(int)
    def _fold_percent_pos(self, value: int) -> None:
        self._update(replace(self._inputs, percent_pos=value))

    @Slot(int)
    def _fold_time_pos(self, value: int) -> None:
        self._update(replace(self._inputs, time_pos=value))

    @Slot(int)
    def _fold_time_remaining(self, value: int) -> None:
        self._update(replace(self._inputs, time_remaining=value))

    @Slot(float)
    def _fold_duration(self, value: float) -> None:
        self._update(replace(self._inputs, duration=value))

    def _update(self, inputs: FooterInputs) -> None:
        self._inputs = inputs
        new, old = self._derive(), self._props
        if new == old:
            return
        self._props = new
        if new.statusbar_percentage != old.statusbar_percentage:
            self.statusbarPercentageChanged.emit(new.statusbar_percentage)
        if new.time_display_mode != old.time_display_mode:
            self.timeDisplayModeChanged.emit(new.time_display_mode)
        if new.is_percent_visible != old.is_percent_visible:
            self.isPercentVisibleChanged.emit(new.is_percent_visible)
        if new.percent_text != old.percent_text:
            self.percentTextChanged.emit(new.percent_text)
        if new.is_time_visible != old.is_time_visible:
            self.isTimeVisibleChanged.emit(new.is_time_visible)
        if new.time_text != old.time_text:
            self.timeTextChanged.emit(new.time_text)
        if new.time_width != old.time_width:
            self.timeWidthChanged.emit(new.time_width)

    @Property(bool, notify=statusbarPercentageChanged)
    def statusbarPercentage(self) -> bool:
        return self._props.statusbar_percentage

    @Property(int, notify=timeDisplayModeChanged)
    def timeDisplayMode(self) -> int:
        return self._props.time_display_mode

    @timeDisplayMode.setter
    def timeDisplayMode(self, value: int) -> None:
        self._settings.time_display_mode = TimeDisplayMode(value)

    @Property(bool, notify=isPercentVisibleChanged)
    def isPercentVisible(self) -> bool:
        return self._props.is_percent_visible

    @Property(str, notify=percentTextChanged)
    def percentText(self) -> str:
        return self._props.percent_text

    @Property(bool, notify=isTimeVisibleChanged)
    def isTimeVisible(self) -> bool:
        return self._props.is_time_visible

    @Property(str, notify=timeTextChanged)
    def timeText(self) -> str:
        return self._props.time_text

    @Property(int, notify=timeWidthChanged)
    def timeWidth(self) -> int:
        return self._props.time_width

    @Slot()
    def toggleStatusbarPercentage(self) -> None:
        self._settings.show_percentage = not self._props.statusbar_percentage
