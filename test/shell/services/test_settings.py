# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable
from typing import NamedTuple

import pytest
from PySide6.QtCore import Qt

from mpvqc.shell.services import ShellSettingsService, TimeDisplayMode, WindowTitleFormat

VERTICAL = Qt.Orientation.Vertical.value
HORIZONTAL = Qt.Orientation.Horizontal.value


@pytest.fixture
def existing_settings_service(read_existing_settings) -> Callable[[str], ShellSettingsService]:
    def read(content: str) -> ShellSettingsService:
        return ShellSettingsService(read_existing_settings(content))

    return read


def test_show_percentage_defaults_to_on(shell_settings_service):
    assert shell_settings_service.show_percentage is True


def test_time_display_mode_defaults_to_current_over_total(shell_settings_service):
    assert shell_settings_service.time_display_mode is TimeDisplayMode.CURRENT_TOTAL_TIME


def test_layout_orientation_defaults_to_vertical(shell_settings_service):
    assert shell_settings_service.layout_orientation == VERTICAL


def test_window_title_format_defaults_to_the_app_name(shell_settings_service):
    assert shell_settings_service.window_title_format is WindowTitleFormat.DEFAULT


def test_show_percentage_set_and_get(shell_settings_service):
    shell_settings_service.show_percentage = False

    assert not shell_settings_service.show_percentage


@pytest.mark.parametrize("mode", list(TimeDisplayMode))
def test_time_display_mode_set_and_get(shell_settings_service, mode):
    shell_settings_service.time_display_mode = mode

    assert shell_settings_service.time_display_mode is mode


def test_layout_orientation_set_and_get(shell_settings_service):
    shell_settings_service.layout_orientation = HORIZONTAL

    assert shell_settings_service.layout_orientation == HORIZONTAL


@pytest.mark.parametrize("title_format", list(WindowTitleFormat))
def test_window_title_format_set_and_get(shell_settings_service, title_format):
    shell_settings_service.window_title_format = title_format

    assert shell_settings_service.window_title_format is title_format


def test_show_percentage_signals_a_change(shell_settings_service, make_spy):
    spy = make_spy(shell_settings_service.show_percentage_changed)

    shell_settings_service.show_percentage = False
    assert spy.count() == 1
    assert spy.at(0, 0) is False

    shell_settings_service.show_percentage = False
    assert spy.count() == 1


def test_time_display_mode_signals_a_change(shell_settings_service, make_spy):
    spy = make_spy(shell_settings_service.time_display_mode_changed)

    shell_settings_service.time_display_mode = TimeDisplayMode.REMAINING_TIME
    assert spy.count() == 1
    assert spy.at(0, 0) == TimeDisplayMode.REMAINING_TIME

    shell_settings_service.time_display_mode = TimeDisplayMode.REMAINING_TIME
    assert spy.count() == 1


def test_layout_orientation_signals_a_change(shell_settings_service, make_spy):
    spy = make_spy(shell_settings_service.layout_orientation_changed)

    shell_settings_service.layout_orientation = HORIZONTAL
    assert spy.count() == 1
    assert spy.at(0, 0) == HORIZONTAL

    shell_settings_service.layout_orientation = HORIZONTAL
    assert spy.count() == 1


def test_window_title_format_signals_a_change(shell_settings_service, make_spy):
    spy = make_spy(shell_settings_service.window_title_format_changed)

    shell_settings_service.window_title_format = WindowTitleFormat.FILE_NAME
    assert spy.count() == 1
    assert spy.at(0, 0) == WindowTitleFormat.FILE_NAME

    shell_settings_service.window_title_format = WindowTitleFormat.FILE_NAME
    assert spy.count() == 1


def test_every_write_lands_under_its_stored_key(shell_settings_service, ini_section):
    shell_settings_service.show_percentage = False
    shell_settings_service.time_display_mode = TimeDisplayMode.REMAINING_TIME
    shell_settings_service.layout_orientation = HORIZONTAL
    shell_settings_service.window_title_format = WindowTitleFormat.FILE_PATH

    assert ini_section("StatusBar")["statusbarPercentage"] == "false"
    assert ini_section("StatusBar")["timeFormat"] == "2"
    assert ini_section("SplitView")["layoutOrientation"] == "1"
    assert ini_section("Window")["titleFormat"] == "2"


def test_a_settings_file_from_an_earlier_run_reads_back_unchanged(existing_settings_service):
    service = existing_settings_service("""
        [StatusBar]
        statusbarPercentage=false
        timeFormat=1

        [SplitView]
        layoutOrientation=1

        [Window]
        titleFormat=2
    """)

    assert service.show_percentage is False
    assert service.time_display_mode is TimeDisplayMode.CURRENT_TIME
    assert service.layout_orientation == HORIZONTAL
    assert service.window_title_format is WindowTitleFormat.FILE_PATH


class FallbackCase(NamedTuple):
    name: str
    key: str
    read: Callable[[ShellSettingsService], object]
    default: object


@pytest.mark.parametrize(
    "stored",
    [42, -1, "banana", "", True],
    ids=["out-of-range", "negative", "text", "empty", "bool"],
)
@pytest.mark.parametrize(
    "case",
    [
        FallbackCase(
            name="time display mode",
            key="StatusBar/timeFormat",
            read=lambda service: service.time_display_mode,
            default=TimeDisplayMode.CURRENT_TOTAL_TIME,
        ),
        FallbackCase(
            name="window title format",
            key="Window/titleFormat",
            read=lambda service: service.window_title_format,
            default=WindowTitleFormat.DEFAULT,
        ),
    ],
    ids=lambda case: case.name,
)
def test_an_unreadable_member_falls_back_to_its_default(shell_settings_service, settings_file, case, stored):
    settings_file.qsettings.setValue(case.key, stored)

    assert case.read(shell_settings_service) is case.default


@pytest.mark.parametrize("stored", ["banana", "", True], ids=["text", "empty", "bool"])
def test_an_unreadable_layout_orientation_falls_back_to_vertical(shell_settings_service, settings_file, stored):
    settings_file.qsettings.setValue("SplitView/layoutOrientation", stored)

    assert shell_settings_service.layout_orientation == VERTICAL
