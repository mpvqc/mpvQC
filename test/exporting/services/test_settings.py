# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable

import pytest

from mpvqc.exporting.services import ExportSettingsService


@pytest.fixture
def existing_settings_service(read_existing_settings) -> Callable[[str], ExportSettingsService]:
    def read(content: str) -> ExportSettingsService:
        return ExportSettingsService(read_existing_settings(content))

    return read


def test_backup_enabled_defaults_to_on(export_settings_service):
    assert export_settings_service.backup_enabled


def test_backup_enabled_set_and_get(export_settings_service):
    export_settings_service.backup_enabled = False
    assert not export_settings_service.backup_enabled

    export_settings_service.backup_enabled = True
    assert export_settings_service.backup_enabled


def test_backup_enabled_signals_a_change(export_settings_service, make_spy):
    spy = make_spy(export_settings_service.backup_enabled_changed)

    export_settings_service.backup_enabled = False
    assert spy.count() == 1
    assert spy.at(0, 0) is False

    export_settings_service.backup_enabled = False
    assert spy.count() == 1


def test_backup_interval_defaults_to_one_minute(export_settings_service):
    assert export_settings_service.backup_interval == 60


def test_backup_interval_set_and_get(export_settings_service):
    export_settings_service.backup_interval = 120
    assert export_settings_service.backup_interval == 120


def test_backup_interval_signals_a_change(export_settings_service, make_spy):
    spy = make_spy(export_settings_service.backup_interval_changed)

    export_settings_service.backup_interval = 90
    assert spy.count() == 1
    assert spy.at(0, 0) == 90

    export_settings_service.backup_interval = 90
    assert spy.count() == 1


@pytest.mark.parametrize(
    "stored",
    [42, "banana", "", ["a", "b"]],
    ids=["number", "text", "empty", "comma-separated"],
)
def test_unreadable_backup_enabled_falls_back_to_on(export_settings_service, settings_file, stored):
    settings_file.qsettings.setValue("Backup/enabled", stored)

    assert export_settings_service.backup_enabled


@pytest.mark.parametrize(
    "stored",
    ["banana", "", ["a", "b"], 4.5],
    ids=["text", "empty", "comma-separated", "fractional"],
)
def test_unreadable_backup_interval_falls_back_to_one_minute(export_settings_service, settings_file, stored):
    settings_file.qsettings.setValue("Backup/interval", stored)

    assert export_settings_service.backup_interval == 60


def test_nickname_defaults_to_the_os_username(export_settings_service, monkeypatch):
    monkeypatch.setenv("USERNAME", "os-user")
    assert export_settings_service.nickname == "os-user"


def test_nickname_set_and_get(export_settings_service):
    export_settings_service.nickname = "lorem"
    assert export_settings_service.nickname == "lorem"


def test_a_nickname_cleared_to_none_reads_back_as_empty(export_settings_service):
    export_settings_service.nickname = None
    assert not export_settings_service.nickname


def test_write_header_date_defaults_to_on(export_settings_service):
    assert export_settings_service.write_header_date


def test_write_header_date_set_and_get(export_settings_service):
    export_settings_service.write_header_date = False
    assert not export_settings_service.write_header_date


def test_write_header_generator_defaults_to_on(export_settings_service):
    assert export_settings_service.write_header_generator


def test_write_header_generator_set_and_get(export_settings_service):
    export_settings_service.write_header_generator = False
    assert not export_settings_service.write_header_generator


def test_write_header_nickname_defaults_to_off(export_settings_service):
    assert not export_settings_service.write_header_nickname


def test_write_header_nickname_set_and_get(export_settings_service):
    export_settings_service.write_header_nickname = True
    assert export_settings_service.write_header_nickname


def test_write_header_video_path_defaults_to_on(export_settings_service):
    assert export_settings_service.write_header_video_path


def test_write_header_video_path_set_and_get(export_settings_service):
    export_settings_service.write_header_video_path = False
    assert not export_settings_service.write_header_video_path


def test_write_header_subtitles_defaults_to_off(export_settings_service):
    assert not export_settings_service.write_header_subtitles


def test_write_header_subtitles_set_and_get(export_settings_service):
    export_settings_service.write_header_subtitles = True
    assert export_settings_service.write_header_subtitles


def test_every_write_lands_under_its_stored_key_in_the_backup_and_export_ini_sections(
    export_settings_service, ini_section
):
    export_settings_service.backup_enabled = False
    export_settings_service.backup_interval = 90
    export_settings_service.nickname = "lorem"
    export_settings_service.write_header_date = False
    export_settings_service.write_header_generator = False
    export_settings_service.write_header_nickname = True
    export_settings_service.write_header_video_path = False
    export_settings_service.write_header_subtitles = True

    backup = ini_section("Backup")
    assert backup["enabled"] == "false"
    assert backup["interval"] == "90"

    export = ini_section("Export")
    assert export["nickname"] == "lorem"
    assert export["writeHeaderDate"] == "false"
    assert export["writeHeaderGenerator"] == "false"
    assert export["writeHeaderNickname"] == "true"
    assert export["writeHeaderVideoPath"] == "false"
    assert export["writeHeaderSubtitles"] == "true"


def test_a_settings_file_from_an_earlier_run_reads_back_unchanged(existing_settings_service):
    service = existing_settings_service(
        """
        [Backup]
        enabled=false
        interval=90

        [Export]
        nickname=lorem
        writeHeaderDate=false
        writeHeaderGenerator=false
        writeHeaderNickname=true
        writeHeaderVideoPath=false
        writeHeaderSubtitles=true
        """
    )

    assert not service.backup_enabled
    assert service.backup_interval == 90
    assert service.nickname == "lorem"
    assert not service.write_header_date
    assert not service.write_header_generator
    assert service.write_header_nickname
    assert not service.write_header_video_path
    assert service.write_header_subtitles


@pytest.mark.parametrize(
    "stored",
    ["banana", "", "2", "1.0"],
    ids=["text", "empty", "number", "fractional"],
)
def test_an_earlier_run_storing_an_unreadable_backup_enabled_falls_back_to_on(existing_settings_service, stored):
    assert existing_settings_service(f"[Backup]\nenabled={stored}\n").backup_enabled


@pytest.mark.parametrize(
    "stored",
    ["banana", "", "true", "4.5"],
    ids=["text", "empty", "boolean", "fractional"],
)
def test_an_earlier_run_storing_an_unreadable_backup_interval_falls_back_to_one_minute(
    existing_settings_service, stored
):
    assert existing_settings_service(f"[Backup]\ninterval={stored}\n").backup_interval == 60
