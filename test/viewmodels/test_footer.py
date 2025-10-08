# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
import pytest

from mpvqc.services import LabelWidthCalculatorService, PlayerService, SettingsService, TimeFormatterService
from mpvqc.viewmodels.footer import MpvqcFooterViewModel


@pytest.fixture
def view_model():
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


def test_initial_state(view_model):
    assert view_model.selectedCommentIndex == 0
    assert view_model.totalCommentCount == 0
    assert not view_model.isCommentCountVisible
    assert not view_model.isVideoPercentVisible
    assert not view_model.isTimeTextVisible


def test_comment_count_display(view_model, make_spy):
    text_spy = make_spy(view_model.commentCountTextChanged)
    visibility_spy = make_spy(view_model.isCommentCountVisibleChanged)

    view_model.totalCommentCount = 2
    view_model.selectedCommentIndex = 1

    assert view_model.commentCountText == "2/2"
    assert view_model.isCommentCountVisible
    assert text_spy.count() > 0
    assert visibility_spy.count() > 0

    view_model.totalCommentCount = 0

    assert not view_model.isCommentCountVisible
    assert text_spy.count() == 3
    assert visibility_spy.count() == 2


def test_video_percent_display(view_model, player_service_mock, make_spy):
    visibility_spy = make_spy(view_model.isVideoPercentVisibleChanged)
    text_spy = make_spy(view_model.videoPercentTextChanged)

    assert not view_model.isVideoPercentVisible

    player_service_mock.update(video_loaded=True)
    assert view_model.isVideoPercentVisible
    assert visibility_spy.count() == 1

    view_model.toggleVideoPercentDisplay()
    assert not view_model.isVideoPercentVisible
    assert visibility_spy.count() == 2

    player_service_mock.update(percent_pos=42)
    assert view_model.videoPercentText == "42%"
    assert text_spy.count() > 0

    view_model.toggleVideoPercentDisplay()
    assert view_model.isVideoPercentVisible
    assert visibility_spy.count() == 3

    view_model.toggleVideoPercentDisplay()
    assert not view_model.isVideoPercentVisible
    assert visibility_spy.count() == 4

    player_service_mock.update(percent_pos=99)
    assert view_model.videoPercentText == "99%"
    assert text_spy.at(invocation=text_spy.count() - 1, argument=0) == "99%"


def test_time_format_display(view_model, player_service_mock, make_spy):
    text_spy = make_spy(view_model.timeTextChanged)
    visibility_spy = make_spy(view_model.isTimeTextVisibleChanged)

    assert not view_model.isTimeTextVisible

    player_service_mock.update(video_loaded=True, duration=125, time_pos=65, time_remaining=60)
    assert view_model.isTimeTextVisible
    assert view_model.timeText == "01:05/02:05"
    assert text_spy.count() == 2
    assert visibility_spy.count() == 1

    view_model.timeFormat = view_model.TimeFormat.CURRENT_TIME.value
    assert view_model.isTimeTextVisible
    assert view_model.timeText == "01:05"
    assert text_spy.count() == 3

    view_model.timeFormat = view_model.TimeFormat.REMAINING_TIME.value
    assert view_model.timeText == "-01:00"
    assert text_spy.count() == 4

    view_model.timeFormat = view_model.TimeFormat.EMPTY.value
    assert not view_model.isTimeTextVisible
    assert text_spy.count() == 5
    assert visibility_spy.count() == 2

    view_model.timeFormat = view_model.TimeFormat.CURRENT_TOTAL_TIME.value
    assert view_model.isTimeTextVisible
    assert view_model.timeText == "01:05/02:05"
    assert text_spy.count() == 6
    assert visibility_spy.count() == 3


def test_time_width_calculation(view_model, player_service_mock, make_spy):
    width_spy = make_spy(view_model.timeWidthChanged)

    assert view_model.timeWidth == 0

    player_service_mock.update(video_loaded=True, duration=125, time_pos=65, time_remaining=60)
    assert view_model.timeWidth > 0
    initial_width = view_model.timeWidth
    assert width_spy.count() == 1

    player_service_mock.update(duration=7200, time_pos=3661, time_remaining=3539)
    assert view_model.timeWidth > initial_width
    long_format_width = view_model.timeWidth
    assert width_spy.count() == 2

    view_model.timeFormat = view_model.TimeFormat.CURRENT_TIME.value
    assert view_model.timeWidth < long_format_width
    assert width_spy.count() == 3

    view_model.timeFormat = view_model.TimeFormat.EMPTY.value
    assert view_model.timeWidth == 0
    assert width_spy.count() == 4

    view_model.timeFormat = view_model.TimeFormat.CURRENT_TOTAL_TIME.value
    assert view_model.timeWidth == long_format_width
    assert width_spy.count() == 5
