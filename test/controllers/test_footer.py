# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
import pytest
from PySide6.QtCore import QObject, Signal

from mpvqc.controllers.footer import MpvqcFooterViewController
from mpvqc.services import LabelWidthCalculatorService, PlayerService, SettingsService, TimeFormatterService


class PlayerMock(QObject):
    time_pos_changed = Signal(int)
    duration_changed = Signal(float)
    percent_pos_changed = Signal(int)
    video_loaded_changed = Signal(bool)
    time_remaining_changed = Signal(int)

    def __init__(self):
        super().__init__()
        self.video_loaded = False
        self.duration = 0.0
        self.time_pos = 0
        self.time_remaining = 0
        self.percent_pos = 0

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

        self.video_loaded_changed.emit(self.video_loaded)
        self.duration_changed.emit(self.duration)
        self.time_pos_changed.emit(self.time_pos)
        self.time_remaining_changed.emit(self.time_remaining)
        self.percent_pos_changed.emit(self.percent_pos)


class SettingsMock(QObject):
    statusbarPercentageChanged = Signal(bool)
    timeFormatChanged = Signal(int)

    def __init__(self):
        super().__init__()
        from mpvqc.controllers.footer import MpvqcFooterViewController

        self._statusbar_percentage = False
        self._time_format = MpvqcFooterViewController.TimeFormat.CURRENT_TOTAL_TIME

    @property
    def statusbar_percentage(self):
        return self._statusbar_percentage

    @statusbar_percentage.setter
    def statusbar_percentage(self, value):
        if self._statusbar_percentage != value:
            self._statusbar_percentage = value
            self.statusbarPercentageChanged.emit(value)

    @property
    def time_format(self):
        return self._time_format

    @time_format.setter
    def time_format(self, value):
        if self._time_format != value:
            self._time_format = value
            self.timeFormatChanged.emit(value)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


@pytest.fixture
def controller():
    # noinspection PyCallingNonCallable
    return MpvqcFooterViewController()


@pytest.fixture
def player():
    return PlayerMock()


@pytest.fixture
def settings():
    return SettingsMock()


@pytest.fixture(autouse=True)
def configure_inject(player, settings):
    def config(binder: inject.Binder):
        binder.bind(PlayerService, player)
        binder.bind(SettingsService, settings)
        binder.bind(TimeFormatterService, TimeFormatterService())
        binder.bind(LabelWidthCalculatorService, LabelWidthCalculatorService())

    inject.configure(config, clear=True)


def test_initial_state(controller):
    assert controller.selectedCommentIndex == 0
    assert controller.totalCommentCount == 0
    assert not controller.isCommentCountVisible
    assert not controller.isVideoPercentVisible
    assert not controller.isTimeTextVisible


def test_comment_count_display(controller, make_spy):
    text_spy = make_spy(controller.commentCountTextChanged)
    visibility_spy = make_spy(controller.isCommentCountVisibleChanged)

    controller.totalCommentCount = 2
    controller.selectedCommentIndex = 1

    assert controller.commentCountText == "2/2"
    assert controller.isCommentCountVisible
    assert text_spy.count() > 0
    assert visibility_spy.count() > 0

    controller.totalCommentCount = 0

    assert not controller.isCommentCountVisible
    assert text_spy.count() == 3
    assert visibility_spy.count() == 2


def test_video_percent_display(controller, player, make_spy):
    visibility_spy = make_spy(controller.isVideoPercentVisibleChanged)
    text_spy = make_spy(controller.videoPercentTextChanged)

    assert not controller.isVideoPercentVisible

    controller.toggleVideoPercentDisplay()
    assert not controller.isVideoPercentVisible
    assert visibility_spy.count() == 0

    player.update(video_loaded=True)
    assert controller.isVideoPercentVisible
    assert visibility_spy.count() > 0

    player.update(percent_pos=42)
    assert controller.videoPercentText == "42%"
    assert text_spy.count() > 0

    controller.toggleVideoPercentDisplay()
    assert not controller.isVideoPercentVisible
    assert visibility_spy.count() == 2

    controller.toggleVideoPercentDisplay()
    assert controller.isVideoPercentVisible
    assert visibility_spy.count() == 3

    player.update(percent_pos=99)
    assert controller.videoPercentText == "99%"
    assert text_spy.at(invocation=text_spy.count() - 1, argument=0) == "99%"


def test_time_format_display(controller, player, make_spy):
    text_spy = make_spy(controller.timeTextChanged)
    visibility_spy = make_spy(controller.isTimeTextVisibleChanged)

    assert not controller.isTimeTextVisible

    player.update(video_loaded=True, duration=125, time_pos=65, time_remaining=60)
    assert controller.isTimeTextVisible
    assert controller.timeText == "01:05/02:05"
    assert text_spy.count() == 1
    assert visibility_spy.count() == 1

    controller.timeFormat = controller.TimeFormat.CURRENT_TIME
    assert controller.isTimeTextVisible
    assert controller.timeText == "01:05"
    assert text_spy.count() == 2

    controller.timeFormat = controller.TimeFormat.REMAINING_TIME
    assert controller.timeText == "-01:00"
    assert text_spy.count() == 3

    controller.timeFormat = controller.TimeFormat.EMPTY
    assert not controller.isTimeTextVisible
    assert text_spy.count() == 4
    assert visibility_spy.count() == 2

    controller.timeFormat = controller.TimeFormat.CURRENT_TOTAL_TIME
    assert controller.isTimeTextVisible
    assert controller.timeText == "01:05/02:05"
    assert text_spy.count() == 5
    assert visibility_spy.count() == 3


def test_time_width_calculation(controller, player, make_spy):
    width_spy = make_spy(controller.timeWidthChanged)

    assert controller.timeWidth == 0

    player.update(video_loaded=True, duration=125, time_pos=65, time_remaining=60)
    assert controller.timeWidth > 0
    initial_width = controller.timeWidth
    assert width_spy.count() == 1

    player.update(duration=7200, time_pos=3661, time_remaining=3539)
    assert controller.timeWidth > initial_width
    long_format_width = controller.timeWidth
    assert width_spy.count() == 2

    controller.timeFormat = controller.TimeFormat.CURRENT_TIME
    assert controller.timeWidth < long_format_width
    assert width_spy.count() == 3

    controller.timeFormat = controller.TimeFormat.EMPTY
    assert controller.timeWidth == 0
    assert width_spy.count() == 4

    controller.timeFormat = controller.TimeFormat.CURRENT_TOTAL_TIME
    assert controller.timeWidth == long_format_width
    assert width_spy.count() == 5
