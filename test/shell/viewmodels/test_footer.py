# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import replace
from typing import TYPE_CHECKING, NamedTuple

import pytest

from mpvqc.player.services import PlayerService
from mpvqc.shell.services import ShellSettingsService, TimeDisplayMode
from mpvqc.shell.viewmodels import FooterInputs, FooterProps, MpvqcShellFooterViewModel, derive_footer_props

if TYPE_CHECKING:
    import inject


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, player_service, shell_settings_service):
    def custom_bindings(binder: inject.Binder):
        binder.bind(PlayerService, player_service)
        binder.bind(ShellSettingsService, shell_settings_service)

    common_bindings_with(custom_bindings)


@pytest.fixture(autouse=True)
def qt_app_must_be_running(qt_app):
    pass


@pytest.fixture
def make_view_model():
    def _make() -> MpvqcShellFooterViewModel:
        # noinspection PyCallingNonCallable
        return MpvqcShellFooterViewModel()

    return _make


def measure_stub(text: str) -> int:
    return 10 + len(text)


BASE_INPUTS = FooterInputs(
    video_loaded=True,
    percent_pos=42,
    time_pos=65,
    time_remaining=60,
    duration=125.0,
    show_percentage=True,
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
                show_percentage=True,
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
                show_percentage=True,
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
                show_percentage=True,
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
                show_percentage=True,
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
                show_percentage=True,
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
                show_percentage=True,
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
                show_percentage=True,
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
                show_percentage=True,
                time_display_mode=TimeDisplayMode.CURRENT_TOTAL_TIME,
                is_percent_visible=False,
                percent_text="42%",
                is_time_visible=False,
                time_text="",
                time_width=0,
            ),
        ),
        DerivationCase(
            name="percentage setting off hides percent despite video",
            inputs=replace(BASE_INPUTS, show_percentage=False),
            expected=FooterProps(
                show_percentage=False,
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


def test_video_loaded_fold(make_view_model, player_handle, record_emissions):
    view_model = make_view_model()
    emissions = record_emissions(view_model)

    player_handle.load_video("/videos/movie.mkv")

    emissions.assert_exactly(isPercentVisibleChanged=1, isTimeVisibleChanged=1, timeTextChanged=1, timeWidthChanged=1)
    assert emissions["timeTextChanged"].at(0, 0) == "00:00/00:00"
    assert view_model.timeWidth > 0


def test_percent_pos_fold(make_view_model, player_handle, record_emissions):
    view_model = make_view_model()
    emissions = record_emissions(view_model)

    player_handle.update(percent_pos=42.0)

    emissions.assert_exactly(percentTextChanged=1)
    assert emissions["percentTextChanged"].at(0, 0) == "42%"


def test_time_pos_fold(make_view_model, player_handle, shell_settings_service, record_emissions):
    player_handle.load_video("/videos/movie.mkv")
    player_handle.update(time_pos=1.0)
    shell_settings_service.time_display_mode = TimeDisplayMode.CURRENT_TIME
    view_model = make_view_model()
    assert view_model.timeText == "00:01"
    emissions = record_emissions(view_model)

    # 1 -> 10 permutes the same glyphs, so the width stays put on every font engine
    player_handle.update(time_pos=10.0)

    emissions.assert_exactly(timeTextChanged=1)
    assert emissions["timeTextChanged"].at(0, 0) == "00:10"


def test_time_remaining_fold(make_view_model, player_handle, shell_settings_service, record_emissions):
    player_handle.load_video("/videos/movie.mkv")
    player_handle.update(time_remaining=1.0)
    shell_settings_service.time_display_mode = TimeDisplayMode.REMAINING_TIME
    view_model = make_view_model()
    assert view_model.timeText == "-00:01"
    emissions = record_emissions(view_model)

    # 1 -> 10 permutes the same glyphs, so the width stays put on every font engine
    player_handle.update(time_remaining=10.0)

    emissions.assert_exactly(timeTextChanged=1)
    assert emissions["timeTextChanged"].at(0, 0) == "-00:10"


def test_duration_fold(make_view_model, player_handle, record_emissions):
    player_handle.load_video("/videos/movie.mkv")
    view_model = make_view_model()
    assert view_model.timeText == "00:00/00:00"
    emissions = record_emissions(view_model)

    player_handle.update(duration=3600.0)

    emissions.assert_exactly(timeTextChanged=1, timeWidthChanged=1)
    assert emissions["timeTextChanged"].at(0, 0) == "00:00:00/01:00:00"
    assert emissions["timeWidthChanged"].at(0, 0) == view_model.timeWidth


def test_show_percentage_fold(make_view_model, player_handle, shell_settings_service, record_emissions):
    player_handle.load_video("/videos/movie.mkv")
    view_model = make_view_model()
    assert view_model.isPercentVisible
    emissions = record_emissions(view_model)

    shell_settings_service.show_percentage = False

    emissions.assert_exactly(showPercentageChanged=1, isPercentVisibleChanged=1)
    assert emissions["isPercentVisibleChanged"].at(0, 0) is False


def test_time_display_mode_fold(make_view_model, player_handle, shell_settings_service, record_emissions):
    player_handle.load_video("/videos/movie.mkv")
    player_handle.update(duration=125.0, time_pos=65.0, time_remaining=60.0)
    view_model = make_view_model()
    assert view_model.timeText == "01:05/02:05"
    emissions = record_emissions(view_model)

    shell_settings_service.time_display_mode = TimeDisplayMode.NONE

    emissions.assert_exactly(timeDisplayModeChanged=1, isTimeVisibleChanged=1, timeTextChanged=1, timeWidthChanged=1)
    assert not emissions["timeTextChanged"].at(0, 0)
    assert emissions["timeWidthChanged"].at(0, 0) == 0


def test_time_display_mode_property_writes_through_to_settings(make_view_model, shell_settings_service, make_spy):
    view_model = make_view_model()
    spy = make_spy(view_model.timeDisplayModeChanged)

    view_model.timeDisplayMode = TimeDisplayMode.REMAINING_TIME.value

    assert shell_settings_service.time_display_mode is TimeDisplayMode.REMAINING_TIME
    assert view_model.timeDisplayMode == TimeDisplayMode.REMAINING_TIME.value
    assert spy.count() == 1


def test_toggle_percentage_writes_through_to_settings(make_view_model, shell_settings_service):
    view_model = make_view_model()
    initial = view_model.showPercentage

    view_model.togglePercentage()

    assert view_model.showPercentage is not initial
    assert shell_settings_service.show_percentage is not initial
