# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
import pytest

from mpvqc.services import LabelWidthCalculatorService, PlayerService, SettingsService, TimeFormatterService
from mpvqc.viewmodels.footer import MpvqcFooterViewModel


@pytest.fixture
def controller():
    # noinspection PyCallingNonCallable
    return MpvqcFooterViewModel()


@pytest.fixture(autouse=True)
def configure_inject(player_service_mock, settings_service):
    def config(binder: inject.Binder):
        binder.bind(PlayerService, player_service_mock)
        binder.bind(SettingsService, settings_service)
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


def test_video_percent_display(controller, player_service_mock, make_spy):
    visibility_spy = make_spy(controller.isVideoPercentVisibleChanged)
    text_spy = make_spy(controller.videoPercentTextChanged)

    assert not controller.isVideoPercentVisible

    player_service_mock.update(video_loaded=True)
    assert controller.isVideoPercentVisible
    assert visibility_spy.count() == 1

    controller.toggleVideoPercentDisplay()
    assert not controller.isVideoPercentVisible
    assert visibility_spy.count() == 2

    player_service_mock.update(percent_pos=42)
    assert controller.videoPercentText == "42%"
    assert text_spy.count() > 0

    controller.toggleVideoPercentDisplay()
    assert controller.isVideoPercentVisible
    assert visibility_spy.count() == 3

    controller.toggleVideoPercentDisplay()
    assert not controller.isVideoPercentVisible
    assert visibility_spy.count() == 4

    player_service_mock.update(percent_pos=99)
    assert controller.videoPercentText == "99%"
    assert text_spy.at(invocation=text_spy.count() - 1, argument=0) == "99%"


def test_time_format_display(controller, player_service_mock, make_spy):
    text_spy = make_spy(controller.timeTextChanged)
    visibility_spy = make_spy(controller.isTimeTextVisibleChanged)

    assert not controller.isTimeTextVisible

    player_service_mock.update(video_loaded=True, duration=125, time_pos=65, time_remaining=60)
    assert controller.isTimeTextVisible
    assert controller.timeText == "01:05/02:05"
    assert text_spy.count() == 2
    assert visibility_spy.count() == 1

    controller.timeFormat = controller.TimeFormat.CURRENT_TIME.value
    assert controller.isTimeTextVisible
    assert controller.timeText == "01:05"
    assert text_spy.count() == 3

    controller.timeFormat = controller.TimeFormat.REMAINING_TIME.value
    assert controller.timeText == "-01:00"
    assert text_spy.count() == 4

    controller.timeFormat = controller.TimeFormat.EMPTY.value
    assert not controller.isTimeTextVisible
    assert text_spy.count() == 5
    assert visibility_spy.count() == 2

    controller.timeFormat = controller.TimeFormat.CURRENT_TOTAL_TIME.value
    assert controller.isTimeTextVisible
    assert controller.timeText == "01:05/02:05"
    assert text_spy.count() == 6
    assert visibility_spy.count() == 3


def test_time_width_calculation(controller, player_service_mock, make_spy):
    width_spy = make_spy(controller.timeWidthChanged)

    assert controller.timeWidth == 0

    player_service_mock.update(video_loaded=True, duration=125, time_pos=65, time_remaining=60)
    assert controller.timeWidth > 0
    initial_width = controller.timeWidth
    assert width_spy.count() == 1

    player_service_mock.update(duration=7200, time_pos=3661, time_remaining=3539)
    assert controller.timeWidth > initial_width
    long_format_width = controller.timeWidth
    assert width_spy.count() == 2

    controller.timeFormat = controller.TimeFormat.CURRENT_TIME.value
    assert controller.timeWidth < long_format_width
    assert width_spy.count() == 3

    controller.timeFormat = controller.TimeFormat.EMPTY.value
    assert controller.timeWidth == 0
    assert width_spy.count() == 4

    controller.timeFormat = controller.TimeFormat.CURRENT_TOTAL_TIME.value
    assert controller.timeWidth == long_format_width
    assert width_spy.count() == 5
