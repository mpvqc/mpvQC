# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import sys
from pathlib import Path
from textwrap import dedent
from typing import NamedTuple
from unittest.mock import call, patch

import pytest
from PySide6.QtCore import QObject, QProcess, QSettings, QStandardPaths, QUrl

from mpvqc.importing.services import ImportSettingsService, LoadFoundVideo

ELSEWHERE = QUrl.fromLocalFile("/elsewhere")


def movies_location() -> QUrl:
    return QUrl.fromLocalFile(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.MoviesLocation))


def documents_location() -> QUrl:
    return QUrl.fromLocalFile(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation))


def test_import_found_video_defaults_to_ask_every_time(import_settings_service):
    assert import_settings_service.import_found_video == LoadFoundVideo.ASK_EVERY_TIME


@pytest.mark.parametrize("setting", list(LoadFoundVideo))
def test_import_found_video_set_and_get(import_settings_service, setting):
    import_settings_service.import_found_video = setting

    assert import_settings_service.import_found_video == setting


@pytest.mark.parametrize(
    ("stored", "expected"),
    [
        (0, LoadFoundVideo.ALWAYS),
        (1, LoadFoundVideo.ASK_EVERY_TIME),
        (2, LoadFoundVideo.NEVER),
        ("0", LoadFoundVideo.ALWAYS),
        ("1", LoadFoundVideo.ASK_EVERY_TIME),
        ("2", LoadFoundVideo.NEVER),
        (" +2 ", LoadFoundVideo.NEVER),
    ],
)
def test_native_and_text_members_read_without_rewriting(import_settings_service, qsettings, stored, expected):
    qsettings.setValue("Import/loadFoundVideo", stored)

    assert import_settings_service.import_found_video is expected
    assert qsettings.value("Import/loadFoundVideo") == stored


class UnreadableVideoSettingCase(NamedTuple):
    name: str
    stored: int | str | list[str] | bool | float | None


@pytest.mark.parametrize(
    "case",
    [
        UnreadableVideoSettingCase(name="out-of-range", stored=42),
        UnreadableVideoSettingCase(name="text-out-of-range", stored="42"),
        UnreadableVideoSettingCase(name="text", stored="banana"),
        UnreadableVideoSettingCase(name="empty", stored=""),
        UnreadableVideoSettingCase(name="comma-separated", stored=["a", "b"]),
        UnreadableVideoSettingCase(name="native-bool", stored=True),
        UnreadableVideoSettingCase(name="text-bool", stored="true"),
        UnreadableVideoSettingCase(name="native-float", stored=0.0),
        UnreadableVideoSettingCase(name="text-float", stored="0.0"),
        UnreadableVideoSettingCase(name="none", stored=None),
    ],
    ids=lambda case: case.name,
)
def test_unreadable_import_found_video_falls_back_to_ask_every_time(
    import_settings_service, qsettings, case: UnreadableVideoSettingCase
):
    qsettings.setValue("Import/loadFoundVideo", case.stored)

    assert import_settings_service.import_found_video is LoadFoundVideo.ASK_EVERY_TIME
    assert qsettings.contains("Import/loadFoundVideo")
    assert qsettings.value("Import/loadFoundVideo") == case.stored


def test_last_directory_video_defaults_to_the_movies_location(import_settings_service):
    assert import_settings_service.last_directory_video == movies_location()


def test_last_directory_documents_defaults_to_the_documents_location(import_settings_service):
    assert import_settings_service.last_directory_documents == documents_location()


def test_last_directory_subtitles_defaults_to_the_documents_location(import_settings_service):
    assert import_settings_service.last_directory_subtitles == documents_location()


def test_last_directory_video_set_and_get(import_settings_service):
    import_settings_service.last_directory_video = ELSEWHERE

    assert import_settings_service.last_directory_video == ELSEWHERE


def test_last_directory_documents_set_and_get(import_settings_service):
    import_settings_service.last_directory_documents = ELSEWHERE

    assert import_settings_service.last_directory_documents == ELSEWHERE


def test_last_directory_subtitles_set_and_get(import_settings_service):
    import_settings_service.last_directory_subtitles = ELSEWHERE

    assert import_settings_service.last_directory_subtitles == ELSEWHERE


def test_every_write_lands_under_its_stored_key_in_the_import_ini_section(import_settings_service, ini_section):
    import_settings_service.import_found_video = LoadFoundVideo.NEVER
    import_settings_service.last_directory_video = ELSEWHERE
    import_settings_service.last_directory_documents = ELSEWHERE
    import_settings_service.last_directory_subtitles = ELSEWHERE

    section = ini_section("Import")
    assert section["loadFoundVideo"] == "2"
    assert section["lastDirectoryVideo"].startswith("@Variant(")
    assert section["lastDirectoryDocuments"].startswith("@Variant(")
    assert section["lastDirectorySubtitles"].startswith("@Variant(")


def test_synced_writes_read_back_in_a_fresh_process(import_settings_service, qsettings):
    import_settings_service.import_found_video = LoadFoundVideo.ALWAYS
    import_settings_service.last_directory_video = QUrl("file:///videos")
    import_settings_service.last_directory_documents = QUrl("file:///documents")
    import_settings_service.last_directory_subtitles = QUrl("file:///subtitles")
    qsettings.sync()
    assert qsettings.status() == QSettings.Status.NoError

    reader = dedent("""
        import json
        import sys
        from PySide6.QtCore import QSettings, QUrl
        from mpvqc.importing.services import ImportSettingsService

        qsettings = QSettings(sys.argv[1], QSettings.Format.IniFormat)
        service = ImportSettingsService(qsettings)
        print(json.dumps({
            "stored": {
                key: [type(value).__name__, value.toString() if isinstance(value, QUrl) else value]
                for key in qsettings.allKeys()
                for value in [qsettings.value(key)]
            },
            "effective": [
                service.import_found_video.value,
                service.last_directory_video.toString(),
                service.last_directory_documents.toString(),
                service.last_directory_subtitles.toString(),
            ],
        }))
    """)
    process = QProcess()
    process.setWorkingDirectory(str(Path(__file__).resolve().parents[3]))
    process.start(sys.executable, ["-c", reader, qsettings.fileName()])
    finished = process.waitForFinished(30_000)
    if not finished:
        process.kill()
        process.waitForFinished()
    assert finished, process.errorString()
    assert process.exitStatus() == QProcess.ExitStatus.NormalExit
    assert process.exitCode() == 0, bytes(process.readAllStandardError().data()).decode("utf-8")
    assert json.loads(bytes(process.readAllStandardOutput().data())) == {
        "stored": {
            "Import/loadFoundVideo": ["str", "0"],
            "Import/lastDirectoryVideo": ["QUrl", "file:///videos"],
            "Import/lastDirectoryDocuments": ["QUrl", "file:///documents"],
            "Import/lastDirectorySubtitles": ["QUrl", "file:///subtitles"],
        },
        "effective": [0, "file:///videos", "file:///documents", "file:///subtitles"],
    }


def test_the_previous_builds_found_video_key_is_ignored(import_settings_service, qsettings):
    qsettings.setValue("Import/importFoundVideo", LoadFoundVideo.ALWAYS.value)

    assert import_settings_service.import_found_video == LoadFoundVideo.ASK_EVERY_TIME
    assert qsettings.value("Import/importFoundVideo") == 0
    assert not qsettings.contains("Import/loadFoundVideo")


class MalformedDirectoryCase(NamedTuple):
    name: str
    stored: str | int | None


@pytest.mark.parametrize(
    "case",
    [
        MalformedDirectoryCase(name="path", stored="/directory"),
        MalformedDirectoryCase(name="url-text", stored="file:///directory"),
        MalformedDirectoryCase(name="number", stored=42),
        MalformedDirectoryCase(name="none", stored=None),
    ],
    ids=lambda case: case.name,
)
def test_malformed_directories_use_lazy_fallback_without_repair(qsettings, case: MalformedDirectoryCase):
    store = qsettings
    keys = ("Import/lastDirectoryVideo", "Import/lastDirectoryDocuments", "Import/lastDirectorySubtitles")
    with patch.object(QStandardPaths, "writableLocation", side_effect=["/first"] * 3 + ["/second"] * 3) as location:
        service = ImportSettingsService(store)
        location.assert_not_called()
        assert (service.last_directory_video, service.last_directory_documents, service.last_directory_subtitles) == (
            QUrl.fromLocalFile("/first"),
            QUrl.fromLocalFile("/first"),
            QUrl.fromLocalFile("/first"),
        )
        assert store.allKeys() == []
        for key in keys:
            store.setValue(key, case.stored)
        assert (service.last_directory_video, service.last_directory_documents, service.last_directory_subtitles) == (
            QUrl.fromLocalFile("/second"),
            QUrl.fromLocalFile("/second"),
            QUrl.fromLocalFile("/second"),
        )
        assert (
            location.call_args_list
            == [
                call(QStandardPaths.StandardLocation.MoviesLocation),
                call(QStandardPaths.StandardLocation.DocumentsLocation),
                call(QStandardPaths.StandardLocation.DocumentsLocation),
            ]
            * 2
        )
    assert [store.value(key) for key in keys] == [case.stored] * 3
    assert all(store.contains(key) for key in keys)


def test_plain_owner_writes_defaults_and_equal_values_unconditionally(import_settings_service, qsettings):
    service = import_settings_service
    store = qsettings
    assert not isinstance(service, QObject)
    video, documents, subtitles = (
        service.last_directory_video,
        service.last_directory_documents,
        service.last_directory_subtitles,
    )
    assert store.allKeys() == []

    with patch.object(store, "setValue", wraps=store.setValue) as write:
        for _ in range(2):
            service.import_found_video = LoadFoundVideo.ASK_EVERY_TIME
            service.last_directory_video = video
            service.last_directory_documents = documents
            service.last_directory_subtitles = subtitles
        assert (
            write.call_args_list
            == [
                call("Import/loadFoundVideo", 1),
                call("Import/lastDirectoryVideo", video),
                call("Import/lastDirectoryDocuments", documents),
                call("Import/lastDirectorySubtitles", subtitles),
            ]
            * 2
        )
    assert type(store.value("Import/loadFoundVideo")) is int
    assert isinstance(store.value("Import/lastDirectoryVideo"), QUrl)
    assert isinstance(store.value("Import/lastDirectoryDocuments"), QUrl)
    assert isinstance(store.value("Import/lastDirectorySubtitles"), QUrl)
