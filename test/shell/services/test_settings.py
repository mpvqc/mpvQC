# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable
from typing import NamedTuple

import pytest
from PySide6.QtCore import QSettings, Qt

from mpvqc.shell.services import (
    ShellSettingsService,
    TimeDisplayMode,
    WindowTitleFormat,
)

VERTICAL = Qt.Orientation.Vertical.value
HORIZONTAL = Qt.Orientation.Horizontal.value


@pytest.fixture
def existing_settings_service(read_existing_settings) -> Callable[[str], ShellSettingsService]:
    def read(content: str) -> ShellSettingsService:
        return ShellSettingsService(read_existing_settings(content))

    return read


@pytest.fixture
def shell_settings_spies(shell_settings_service, make_spy):
    return (
        make_spy(shell_settings_service.show_percentage_changed),
        make_spy(shell_settings_service.time_display_mode_changed),
        make_spy(shell_settings_service.layout_orientation_changed),
        make_spy(shell_settings_service.window_title_format_changed),
    )


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


@pytest.mark.parametrize(
    "orientation",
    [
        HORIZONTAL,
        42,
        -1,
    ],
)
def test_layout_orientation_set_and_get(shell_settings_service, orientation):
    shell_settings_service.layout_orientation = orientation

    assert shell_settings_service.layout_orientation == orientation
    assert type(shell_settings_service.layout_orientation) is int


@pytest.mark.parametrize("title_format", list(WindowTitleFormat))
def test_window_title_format_set_and_get(shell_settings_service, title_format):
    shell_settings_service.window_title_format = title_format

    assert shell_settings_service.window_title_format is title_format


def test_each_change_is_stored_before_its_one_signal(shell_settings_service, settings_file):
    service = shell_settings_service
    store = settings_file.qsettings
    remaining = TimeDisplayMode.REMAINING_TIME
    file_path = WindowTitleFormat.FILE_PATH
    deliveries: list[tuple[str, object, object, object]] = []
    service.show_percentage_changed.connect(
        lambda payload: deliveries.append(
            ("show_percentage", payload, store.value("StatusBar/statusbarPercentage"), service.show_percentage)
        )
    )
    service.time_display_mode_changed.connect(
        lambda payload: deliveries.append(
            ("time_display_mode", payload, store.value("StatusBar/timeFormat"), service.time_display_mode)
        )
    )
    service.layout_orientation_changed.connect(
        lambda payload: deliveries.append(
            ("layout_orientation", payload, store.value("SplitView/layoutOrientation"), service.layout_orientation)
        )
    )
    service.window_title_format_changed.connect(
        lambda payload: deliveries.append(
            ("window_title_format", payload, store.value("Window/titleFormat"), service.window_title_format)
        )
    )

    for _ in range(2):
        service.show_percentage = False
        service.time_display_mode = remaining
        service.layout_orientation = HORIZONTAL
        service.window_title_format = file_path

    assert deliveries == [
        ("show_percentage", False, False, False),
        ("time_display_mode", remaining.value, remaining.value, remaining),
        ("layout_orientation", HORIZONTAL, HORIZONTAL, HORIZONTAL),
        ("window_title_format", file_path.value, file_path.value, file_path),
    ]
    assert [type(payload) for _, payload, _, _ in deliveries] == [bool, int, int, int]


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
    [
        pytest.param(42, id="out-of-range"),
        pytest.param("42", id="text-out-of-range"),
        pytest.param("banana", id="text"),
        pytest.param("", id="empty"),
        pytest.param("1.0", id="decimal"),
        pytest.param(True, id="bool"),
        pytest.param(1.5, id="float"),
    ],
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
def test_an_unreadable_member_falls_back_to_its_default(
    shell_settings_service, settings_file, case: FallbackCase, stored
):
    settings_file.qsettings.setValue(case.key, stored)

    assert case.read(shell_settings_service) is case.default


@pytest.mark.parametrize(
    "stored",
    [
        pytest.param("banana", id="text"),
        pytest.param("", id="empty"),
        pytest.param("1.0", id="decimal"),
        pytest.param(True, id="true"),
        pytest.param(False, id="false"),
        pytest.param(1.5, id="float"),
    ],
)
def test_an_unreadable_layout_orientation_falls_back_to_vertical(shell_settings_service, settings_file, stored):
    settings_file.qsettings.setValue("SplitView/layoutOrientation", stored)

    assert shell_settings_service.layout_orientation == VERTICAL
    assert type(shell_settings_service.layout_orientation) is int


@pytest.mark.parametrize(
    ("stored", "expected"),
    [
        (True, True),
        (False, False),
        ("true", True),
        ("false", False),
        ("TrUe", True),
        ("FaLsE", False),
    ],
)
def test_show_percentage_reads_native_and_text_booleans(shell_settings_service, settings_file, stored, expected):
    settings_file.qsettings.setValue("StatusBar/statusbarPercentage", stored)

    assert shell_settings_service.show_percentage is expected


@pytest.mark.parametrize(
    "stored",
    [
        pytest.param(1, id="number"),
        pytest.param(0.0, id="float"),
        pytest.param("1", id="text-number"),
        pytest.param("yes", id="yes"),
        pytest.param("", id="empty"),
        pytest.param(" true ", id="padded"),
        pytest.param("banana", id="text"),
    ],
)
def test_an_unreadable_percentage_falls_back_to_on(shell_settings_service, settings_file, stored):
    settings_file.qsettings.setValue("StatusBar/statusbarPercentage", stored)

    assert shell_settings_service.show_percentage is True


@pytest.mark.parametrize(
    ("stored", "expected"),
    [
        (0, 0),
        (42, 42),
        (-1, -1),
        ("0", 0),
        ("42", 42),
        ("-1", -1),
        (" +42 ", 42),
    ],
)
def test_layout_orientation_reads_native_and_text_integers(shell_settings_service, settings_file, stored, expected):
    settings_file.qsettings.setValue("SplitView/layoutOrientation", stored)

    assert shell_settings_service.layout_orientation == expected
    assert type(shell_settings_service.layout_orientation) is int


@pytest.mark.parametrize(
    "storage",
    [
        "missing",
        "malformed",
        "text-defaults",
    ],
)
def test_reads_and_no_op_assignments_leave_storage_untouched(
    shell_settings_service, settings_file, shell_settings_spies, storage
):
    qsettings = settings_file.qsettings
    defaults = {
        "StatusBar/statusbarPercentage": "true",
        "StatusBar/timeFormat": "3",
        "SplitView/layoutOrientation": "2",
        "Window/titleFormat": "0",
    }
    if storage != "missing":
        for key, value in defaults.items():
            qsettings.setValue(key, "banana" if storage == "malformed" else value)
    before = {key: qsettings.value(key) for key in qsettings.allKeys()}

    assert shell_settings_service.show_percentage is True
    assert shell_settings_service.time_display_mode is TimeDisplayMode.CURRENT_TOTAL_TIME
    assert shell_settings_service.layout_orientation == VERTICAL
    assert shell_settings_service.window_title_format is WindowTitleFormat.DEFAULT
    assert {key: qsettings.value(key) for key in qsettings.allKeys()} == before
    assert [spy.count() for spy in shell_settings_spies] == [0, 0, 0, 0]

    shell_settings_service.show_percentage = True
    shell_settings_service.time_display_mode = TimeDisplayMode.CURRENT_TOTAL_TIME
    shell_settings_service.layout_orientation = VERTICAL
    shell_settings_service.window_title_format = WindowTitleFormat.DEFAULT

    assert {key: qsettings.value(key) for key in qsettings.allKeys()} == before
    assert [spy.count() for spy in shell_settings_spies] == [0, 0, 0, 0]


def test_instances_share_a_file_but_never_a_value(shell_settings_service, settings_file, tmp_path):
    same_file = ShellSettingsService(QSettings(settings_file.qsettings.fileName(), QSettings.Format.IniFormat))
    other_file = ShellSettingsService(QSettings(str(tmp_path / "other.ini"), QSettings.Format.IniFormat))

    shell_settings_service.show_percentage = False
    shell_settings_service.time_display_mode = TimeDisplayMode.REMAINING_TIME
    other_file.layout_orientation = 42
    other_file.window_title_format = WindowTitleFormat.FILE_NAME

    assert (same_file.show_percentage, same_file.time_display_mode) == (False, TimeDisplayMode.REMAINING_TIME)
    assert (same_file.layout_orientation, same_file.window_title_format) == (VERTICAL, WindowTitleFormat.DEFAULT)
    assert (other_file.show_percentage, other_file.time_display_mode) == (True, TimeDisplayMode.CURRENT_TOTAL_TIME)
    assert (other_file.layout_orientation, other_file.window_title_format) == (42, WindowTitleFormat.FILE_NAME)
