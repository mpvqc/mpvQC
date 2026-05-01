# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
import pytest

from mpvqc.enums import MpvqcTimeFormat
from mpvqc.services import LabelWidthCalculatorService, PlayerService, SettingsService
from mpvqc.viewmodels import MpvqcFooterViewModel

TimeFormat = MpvqcTimeFormat.TimeFormat


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, player_service_mock, settings_service):
    def custom_bindings(binder: inject.Binder):
        binder.bind(PlayerService, player_service_mock)
        binder.bind(SettingsService, settings_service)
        binder.bind(LabelWidthCalculatorService, LabelWidthCalculatorService())

    common_bindings_with(custom_bindings)


@pytest.fixture(autouse=True)
def qt_app_must_be_running(qt_app):
    pass


@pytest.fixture
def view_model():
    # noinspection PyCallingNonCallable
    return MpvqcFooterViewModel()


def test_statusbarPercentage(view_model, settings_service):
    settings_service.statusbar_percentage = False
    assert not view_model.statusbarPercentage

    settings_service.statusbar_percentage = True
    assert view_model.statusbarPercentage


def test_timeFormat(view_model, settings_service):
    settings_service.time_format = TimeFormat.REMAINING_TIME.value
    assert view_model.timeFormat == TimeFormat.REMAINING_TIME.value

    view_model.timeFormat = TimeFormat.CURRENT_TIME.value
    assert settings_service.time_format == TimeFormat.CURRENT_TIME.value


@pytest.mark.parametrize(
    ("setting", "video_loaded", "visible"),
    [
        (False, False, False),
        (False, True, False),
        (True, False, False),
        (True, True, True),
    ],
)
def test_isPercentVisible(view_model, setting, video_loaded, visible):
    view_model.setStatusbarPercentage(setting)
    view_model.setVideoLoaded(video_loaded)

    assert view_model.isPercentVisible is visible


def test_percentText(view_model):
    view_model.setPercentPos(42)
    assert view_model.percentText == "42%"


@pytest.mark.parametrize(
    ("video_loaded", "time_format", "duration", "time_pos", "time_remaining", "expected"),
    [
        (False, TimeFormat.CURRENT_TIME.value, 125.0, 65, 60, ""),
        (True, TimeFormat.EMPTY.value, 125.0, 65, 60, ""),
        (True, TimeFormat.CURRENT_TIME.value, 125.0, 65, 60, "01:05"),
        (True, TimeFormat.CURRENT_TIME.value, 7200.0, 3661, 3539, "01:01:01"),
        (True, TimeFormat.REMAINING_TIME.value, 125.0, 65, 60, "-01:00"),
        (True, TimeFormat.REMAINING_TIME.value, 7200.0, 3661, 3539, "-00:58:59"),
        (True, TimeFormat.CURRENT_TOTAL_TIME.value, 125.0, 65, 60, "01:05/02:05"),
        (True, TimeFormat.CURRENT_TOTAL_TIME.value, 7200.0, 3661, 3539, "01:01:01/02:00:00"),
    ],
)
def test_timeText(view_model, video_loaded, time_format, duration, time_pos, time_remaining, expected):
    view_model.setVideoLoaded(video_loaded)
    view_model.setDuration(duration)
    view_model.setTimePos(time_pos)
    view_model.setTimeRemaining(time_remaining)
    view_model.setTimeFormat(time_format)

    assert view_model.timeText == expected
    assert view_model.isTimeVisible is bool(expected)


def test_timeWidth(view_model):
    view_model.setTimeFormat(TimeFormat.CURRENT_TIME.value)
    view_model.setDuration(125.0)
    assert view_model.timeWidth == 0

    view_model.setVideoLoaded(True)
    view_model.setTimeFormat(TimeFormat.EMPTY.value)
    assert view_model.timeWidth == 0

    view_model.setTimeFormat(TimeFormat.CURRENT_TIME.value)
    short_width = view_model.timeWidth
    assert short_width > 0

    view_model.setDuration(7200.0)
    assert view_model.timeWidth > short_width


def test_timeWidth_recomputes_when_video_loaded_toggles_after_duration_and_format(view_model):
    view_model.setTimeFormat(TimeFormat.CURRENT_TIME.value)
    view_model.setDuration(125.0)
    assert view_model.timeWidth == 0

    view_model.setVideoLoaded(True)
    assert view_model.timeWidth > 0

    view_model.setVideoLoaded(False)
    assert view_model.timeWidth == 0


def test_toggleStatusbarPercentage(view_model, settings_service):
    initial = view_model.statusbarPercentage

    view_model.toggleStatusbarPercentage()

    assert view_model.statusbarPercentage is not initial
    assert settings_service.statusbar_percentage is not initial
