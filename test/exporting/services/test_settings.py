# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable
from unittest.mock import call, patch

import pytest

from mpvqc.exporting.services import ExportSettingsService


@pytest.fixture
def existing_settings_service(read_existing_settings) -> Callable[[str], ExportSettingsService]:
    def read(content: str) -> ExportSettingsService:
        return ExportSettingsService(read_existing_settings(content))

    return read


@pytest.fixture
def backup_spies(export_settings_service, make_spy):
    return (
        make_spy(export_settings_service.backup_enabled_changed),
        make_spy(export_settings_service.backup_interval_changed),
    )


def test_backup_enabled_defaults_to_on(export_settings_service):
    assert export_settings_service.backup_enabled


def test_backup_enabled_set_and_get(export_settings_service):
    export_settings_service.backup_enabled = False
    assert not export_settings_service.backup_enabled

    export_settings_service.backup_enabled = True
    assert export_settings_service.backup_enabled


def test_backup_interval_defaults_to_one_minute(export_settings_service):
    assert export_settings_service.backup_interval == 60


def test_backup_interval_set_and_get(export_settings_service):
    export_settings_service.backup_interval = 120
    assert export_settings_service.backup_interval == 120


def test_each_backup_change_is_stored_before_its_one_signal(export_settings_service, settings_file):
    service = export_settings_service
    store = settings_file.qsettings
    deliveries: list[tuple[str, object, object, object]] = []
    service.backup_enabled_changed.connect(
        lambda payload: deliveries.append(("enabled", payload, store.value("Backup/enabled"), service.backup_enabled))
    )
    service.backup_interval_changed.connect(
        lambda payload: deliveries.append(
            ("interval", payload, store.value("Backup/interval"), service.backup_interval)
        )
    )

    for _ in range(2):
        service.backup_enabled = False
        service.backup_interval = 90

    assert deliveries == [
        ("enabled", False, False, False),
        ("interval", 90, 90, 90),
    ]
    assert [type(payload) for _, payload, _, _ in deliveries] == [bool, int]


@pytest.mark.parametrize(
    "stored",
    [
        pytest.param(42, id="number"),
        pytest.param("banana", id="text"),
        pytest.param("", id="empty"),
        pytest.param(["a", "b"], id="comma-separated"),
    ],
)
def test_unreadable_backup_enabled_falls_back_to_on(export_settings_service, settings_file, stored):
    settings_file.qsettings.setValue("Backup/enabled", stored)

    assert export_settings_service.backup_enabled


@pytest.mark.parametrize(
    "stored",
    [
        pytest.param("banana", id="text"),
        pytest.param("", id="empty"),
        pytest.param(["a", "b"], id="comma-separated"),
        pytest.param(4.5, id="fractional"),
        pytest.param(True, id="true"),
        pytest.param(False, id="false"),
    ],
)
def test_unreadable_backup_interval_falls_back_to_one_minute(export_settings_service, settings_file, stored):
    settings_file.qsettings.setValue("Backup/interval", stored)

    assert export_settings_service.backup_interval == 60
    assert type(export_settings_service.backup_interval) is int


def test_nickname_defaults_to_the_current_os_username(export_settings_service, settings_file, monkeypatch):
    monkeypatch.setenv("USERNAME", "os-user")
    assert export_settings_service.nickname == "os-user"

    monkeypatch.setenv("USERNAME", "new-user")
    assert export_settings_service.nickname == "new-user"
    assert not settings_file.qsettings.contains("Export/nickname")


def test_nickname_set_and_get(export_settings_service):
    export_settings_service.nickname = "lorem"
    assert export_settings_service.nickname == "lorem"


def test_a_cleared_nickname_stays_empty(export_settings_service, ini_section, monkeypatch):
    monkeypatch.setenv("USERNAME", "os-user")
    export_settings_service.nickname = "previous-user"
    export_settings_service.nickname = ""

    assert isinstance(export_settings_service.nickname, str)
    assert not export_settings_service.nickname
    assert not ini_section("Export")["nickname"]


@pytest.mark.parametrize(
    "encoded",
    [
        pytest.param("", id="empty"),
        pytest.param("@Invalid()", id="invalid"),
    ],
)
def test_an_earlier_run_with_a_cleared_nickname_stays_empty(existing_settings_service, monkeypatch, encoded):
    monkeypatch.setenv("USERNAME", "os-user")

    nickname = existing_settings_service(f"[Export]\nnickname={encoded}\n").nickname
    assert isinstance(nickname, str)
    assert not nickname


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


@pytest.mark.parametrize(
    "storage",
    [
        "missing",
        "malformed",
        "text-defaults",
    ],
)
def test_header_defaults_are_written_unconditionally_without_signals(
    export_settings_service, settings_file, ini_section, backup_spies, storage
):
    qsettings = settings_file.qsettings
    expected = {
        "writeHeaderDate": "true",
        "writeHeaderGenerator": "true",
        "writeHeaderNickname": "false",
        "writeHeaderVideoPath": "true",
        "writeHeaderSubtitles": "false",
    }
    if storage != "missing":
        for key, value in expected.items():
            qsettings.setValue(f"Export/{key}", "banana" if storage == "malformed" else value)

    with patch.object(qsettings, "setValue", wraps=qsettings.setValue) as writes:
        for _ in range(2):
            export_settings_service.write_header_date = True
            export_settings_service.write_header_generator = True
            export_settings_service.write_header_nickname = False
            export_settings_service.write_header_video_path = True
            export_settings_service.write_header_subtitles = False

    assert (
        writes.call_args_list
        == [
            call("Export/writeHeaderDate", True),
            call("Export/writeHeaderGenerator", True),
            call("Export/writeHeaderNickname", False),
            call("Export/writeHeaderVideoPath", True),
            call("Export/writeHeaderSubtitles", False),
        ]
        * 2
    )
    assert dict(ini_section("Export")) == expected
    assert [spy.count() for spy in backup_spies] == [0, 0]


def test_every_write_lands_under_its_stored_key_in_the_backup_and_export_ini_sections(
    export_settings_service, ini_section, backup_spies
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
    assert [spy.count() for spy in backup_spies] == [1, 1]


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
    [
        pytest.param("banana", id="text"),
        pytest.param("", id="empty"),
        pytest.param("1", id="number"),
        pytest.param("@Invalid()", id="invalid"),
    ],
)
def test_an_earlier_run_with_unreadable_headers_keeps_defaults(existing_settings_service, stored):
    service = existing_settings_service(f"""
        [Export]
        writeHeaderDate={stored}
        writeHeaderGenerator={stored}
        writeHeaderNickname={stored}
        writeHeaderVideoPath={stored}
        writeHeaderSubtitles={stored}
    """)

    assert service.write_header_date is True
    assert service.write_header_generator is True
    assert service.write_header_nickname is False
    assert service.write_header_video_path is True
    assert service.write_header_subtitles is False


@pytest.mark.parametrize(
    "stored",
    [
        pytest.param("banana", id="text"),
        pytest.param("", id="empty"),
        pytest.param("2", id="number"),
        pytest.param("1.0", id="fractional"),
    ],
)
def test_an_earlier_run_storing_an_unreadable_backup_enabled_falls_back_to_on(existing_settings_service, stored):
    assert existing_settings_service(f"[Backup]\nenabled={stored}\n").backup_enabled


@pytest.mark.parametrize(
    "stored",
    [
        pytest.param("banana", id="text"),
        pytest.param("", id="empty"),
        pytest.param("true", id="boolean"),
        pytest.param("4.5", id="fractional"),
    ],
)
def test_an_earlier_run_storing_an_unreadable_backup_interval_falls_back_to_one_minute(
    existing_settings_service, stored
):
    assert existing_settings_service(f"[Backup]\ninterval={stored}\n").backup_interval == 60
