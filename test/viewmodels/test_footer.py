# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import replace
from typing import NamedTuple

import inject
import pytest

from mpvqc.player.services import PlayerService
from mpvqc.services import FontLoaderService, LabelWidthCalculatorService
from mpvqc.shell.services import ShellSettingsService, TimeDisplayMode
from mpvqc.viewmodels import MpvqcFooterViewModel
from mpvqc.viewmodels.views.footer import FooterInputs, FooterProps, derive_footer_props


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, player_service, shell_settings_service):
    def custom_bindings(binder: inject.Binder):
        binder.bind(PlayerService, player_service)
        binder.bind(ShellSettingsService, shell_settings_service)
        binder.bind_to_constructor(FontLoaderService, FontLoaderService)
        binder.bind(LabelWidthCalculatorService, LabelWidthCalculatorService())

    common_bindings_with(custom_bindings)


@pytest.fixture(autouse=True)
def qt_app_must_be_running(qt_app):
    pass


@pytest.fixture
def make_view_model():
    def _make() -> MpvqcFooterViewModel:
        # noinspection PyCallingNonCallable
        return MpvqcFooterViewModel()

    return _make


@pytest.fixture
def spy_notifies(make_spy):
    def _spy(view_model: MpvqcFooterViewModel) -> dict:
        return {
            "statusbarPercentage": make_spy(view_model.statusbarPercentageChanged),
            "timeDisplayMode": make_spy(view_model.timeDisplayModeChanged),
            "isPercentVisible": make_spy(view_model.isPercentVisibleChanged),
            "percentText": make_spy(view_model.percentTextChanged),
            "isTimeVisible": make_spy(view_model.isTimeVisibleChanged),
            "timeText": make_spy(view_model.timeTextChanged),
            "timeWidth": make_spy(view_model.timeWidthChanged),
        }

    return _spy


def emissions(spies: dict) -> dict[str, int]:
    return {name: spy.count() for name, spy in spies.items() if spy.count()}


def measure_stub(text: str) -> int:
    return 10 + len(text)


BASE_INPUTS = FooterInputs(
    video_loaded=True,
    percent_pos=42,
    time_pos=65,
    time_remaining=60,
    duration=125.0,
    statusbar_percentage=True,
    time_display_mode=TimeDisplayMode.CURRENT_TOTAL_TIME,
)


class DerivationCase(NamedTuple):
    name: str
    inputs: FooterInputs
    expected: FooterProps


@pytest.mark.parametrize(
    "case",
    [
        DerivationCase(
            name="current over total joins both times",
            inputs=BASE_INPUTS,
            expected=FooterProps(
                statusbar_percentage=True,
                time_display_mode=TimeDisplayMode.CURRENT_TOTAL_TIME,
                is_percent_visible=True,
                percent_text="42%",
                is_time_visible=True,
                time_text="01:05/02:05",
                time_width=21,
            ),
        ),
        DerivationCase(
            name="current time",
            inputs=replace(BASE_INPUTS, time_display_mode=TimeDisplayMode.CURRENT_TIME),
            expected=FooterProps(
                statusbar_percentage=True,
                time_display_mode=TimeDisplayMode.CURRENT_TIME,
                is_percent_visible=True,
                percent_text="42%",
                is_time_visible=True,
                time_text="01:05",
                time_width=15,
            ),
        ),
        DerivationCase(
            name="remaining time carries a minus prefix",
            inputs=replace(BASE_INPUTS, time_display_mode=TimeDisplayMode.REMAINING_TIME),
            expected=FooterProps(
                statusbar_percentage=True,
                time_display_mode=TimeDisplayMode.REMAINING_TIME,
                is_percent_visible=True,
                percent_text="42%",
                is_time_visible=True,
                time_text="-01:00",
                time_width=16,
            ),
        ),
        DerivationCase(
            name="none mode hides the time and zeroes the width",
            inputs=replace(BASE_INPUTS, time_display_mode=TimeDisplayMode.NONE),
            expected=FooterProps(
                statusbar_percentage=True,
                time_display_mode=TimeDisplayMode.NONE,
                is_percent_visible=True,
                percent_text="42%",
                is_time_visible=False,
                time_text="",
                time_width=0,
            ),
        ),
        DerivationCase(
            name="one hour flips to the long format",
            inputs=replace(BASE_INPUTS, time_display_mode=TimeDisplayMode.CURRENT_TIME, duration=3600.0),
            expected=FooterProps(
                statusbar_percentage=True,
                time_display_mode=TimeDisplayMode.CURRENT_TIME,
                is_percent_visible=True,
                percent_text="42%",
                is_time_visible=True,
                time_text="00:01:05",
                time_width=18,
            ),
        ),
        DerivationCase(
            name="just under one hour stays short",
            inputs=replace(BASE_INPUTS, time_display_mode=TimeDisplayMode.CURRENT_TIME, duration=3599.0),
            expected=FooterProps(
                statusbar_percentage=True,
                time_display_mode=TimeDisplayMode.CURRENT_TIME,
                is_percent_visible=True,
                percent_text="42%",
                is_time_visible=True,
                time_text="01:05",
                time_width=15,
            ),
        ),
        DerivationCase(
            name="long format joins in total mode",
            inputs=replace(BASE_INPUTS, duration=7200.0),
            expected=FooterProps(
                statusbar_percentage=True,
                time_display_mode=TimeDisplayMode.CURRENT_TOTAL_TIME,
                is_percent_visible=True,
                percent_text="42%",
                is_time_visible=True,
                time_text="00:01:05/02:00:00",
                time_width=27,
            ),
        ),
        DerivationCase(
            name="no video blanks the time and hides both labels",
            inputs=replace(BASE_INPUTS, video_loaded=False),
            expected=FooterProps(
                statusbar_percentage=True,
                time_display_mode=TimeDisplayMode.CURRENT_TOTAL_TIME,
                is_percent_visible=False,
                percent_text="42%",
                is_time_visible=False,
                time_text="",
                time_width=0,
            ),
        ),
        DerivationCase(
            name="statusbar setting off hides percent despite video",
            inputs=replace(BASE_INPUTS, statusbar_percentage=False),
            expected=FooterProps(
                statusbar_percentage=False,
                time_display_mode=TimeDisplayMode.CURRENT_TOTAL_TIME,
                is_percent_visible=False,
                percent_text="42%",
                is_time_visible=True,
                time_text="01:05/02:05",
                time_width=21,
            ),
        ),
    ],
    ids=lambda case: case.name,
)
def test_derivation(case: DerivationCase):
    assert derive_footer_props(case.inputs, measure_stub) == case.expected


def test_video_loaded_fold(make_view_model, player_handle, spy_notifies):
    view_model = make_view_model()
    spies = spy_notifies(view_model)

    player_handle.load_video("/videos/movie.mkv")

    assert emissions(spies) == {"isPercentVisible": 1, "isTimeVisible": 1, "timeText": 1, "timeWidth": 1}
    assert spies["timeText"].at(0, 0) == "00:00/00:00"
    assert view_model.timeWidth > 0


def test_percent_pos_fold(make_view_model, player_handle, spy_notifies):
    view_model = make_view_model()
    spies = spy_notifies(view_model)

    player_handle.update(percent_pos=42.0)

    assert emissions(spies) == {"percentText": 1}
    assert spies["percentText"].at(0, 0) == "42%"


def test_time_pos_fold(make_view_model, player_handle, shell_settings_service, spy_notifies):
    player_handle.load_video("/videos/movie.mkv")
    player_handle.update(time_pos=1.0)
    shell_settings_service.time_display_mode = TimeDisplayMode.CURRENT_TIME
    view_model = make_view_model()
    assert view_model.timeText == "00:01"
    spies = spy_notifies(view_model)

    # 1 -> 10 permutes the same glyphs, so the width stays put on every font engine
    player_handle.update(time_pos=10.0)

    assert emissions(spies) == {"timeText": 1}
    assert spies["timeText"].at(0, 0) == "00:10"


def test_time_remaining_fold(make_view_model, player_handle, shell_settings_service, spy_notifies):
    player_handle.load_video("/videos/movie.mkv")
    player_handle.update(time_remaining=1.0)
    shell_settings_service.time_display_mode = TimeDisplayMode.REMAINING_TIME
    view_model = make_view_model()
    assert view_model.timeText == "-00:01"
    spies = spy_notifies(view_model)

    # 1 -> 10 permutes the same glyphs, so the width stays put on every font engine
    player_handle.update(time_remaining=10.0)

    assert emissions(spies) == {"timeText": 1}
    assert spies["timeText"].at(0, 0) == "-00:10"


def test_duration_fold(make_view_model, player_handle, spy_notifies):
    player_handle.load_video("/videos/movie.mkv")
    view_model = make_view_model()
    assert view_model.timeText == "00:00/00:00"
    spies = spy_notifies(view_model)

    player_handle.update(duration=3600.0)

    assert emissions(spies) == {"timeText": 1, "timeWidth": 1}
    assert spies["timeText"].at(0, 0) == "00:00:00/01:00:00"
    assert spies["timeWidth"].at(0, 0) == view_model.timeWidth


def test_statusbar_percentage_fold(make_view_model, player_handle, shell_settings_service, spy_notifies):
    player_handle.load_video("/videos/movie.mkv")
    view_model = make_view_model()
    assert view_model.isPercentVisible
    spies = spy_notifies(view_model)

    shell_settings_service.show_percentage = False

    assert emissions(spies) == {"statusbarPercentage": 1, "isPercentVisible": 1}
    assert spies["isPercentVisible"].at(0, 0) is False


def test_time_display_mode_fold(make_view_model, player_handle, shell_settings_service, spy_notifies):
    player_handle.load_video("/videos/movie.mkv")
    player_handle.update(duration=125.0, time_pos=65.0, time_remaining=60.0)
    view_model = make_view_model()
    assert view_model.timeText == "01:05/02:05"
    spies = spy_notifies(view_model)

    shell_settings_service.time_display_mode = TimeDisplayMode.NONE

    assert emissions(spies) == {"timeDisplayMode": 1, "isTimeVisible": 1, "timeText": 1, "timeWidth": 1}
    assert not spies["timeText"].at(0, 0)
    assert spies["timeWidth"].at(0, 0) == 0


def test_time_display_mode_property_writes_through_to_settings(make_view_model, shell_settings_service, make_spy):
    view_model = make_view_model()
    spy = make_spy(view_model.timeDisplayModeChanged)

    view_model.timeDisplayMode = TimeDisplayMode.REMAINING_TIME.value

    assert shell_settings_service.time_display_mode is TimeDisplayMode.REMAINING_TIME
    assert view_model.timeDisplayMode == TimeDisplayMode.REMAINING_TIME.value
    assert spy.count() == 1


def test_toggle_statusbar_percentage_writes_through_to_settings(make_view_model, shell_settings_service):
    view_model = make_view_model()
    initial = view_model.statusbarPercentage

    view_model.toggleStatusbarPercentage()

    assert view_model.statusbarPercentage is not initial
    assert shell_settings_service.show_percentage is not initial
