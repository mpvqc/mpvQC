# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
from PySide6.QtCore import QSettings, QStandardPaths, QUrl

from mpvqc.importing.domain import LoadFoundVideo
from mpvqc.importing.services import ImportSettingsService

ELSEWHERE = QUrl.fromLocalFile("/elsewhere")


def movies_location() -> QUrl:
    return QUrl.fromLocalFile(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.MoviesLocation))


def documents_location() -> QUrl:
    return QUrl.fromLocalFile(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation))


def import_section(tmp_path) -> str:
    ini = (tmp_path / "test_settings.ini").read_text()
    return ini.split("[Import]", 1)[1].split("[", 1)[0]


def test_import_found_video_defaults_to_ask_every_time(import_settings_service):
    assert import_settings_service.import_found_video == LoadFoundVideo.ASK_EVERY_TIME


@pytest.mark.parametrize("setting", list(LoadFoundVideo))
def test_import_found_video_set_and_get(import_settings_service, setting):
    import_settings_service.import_found_video = setting

    assert import_settings_service.import_found_video == setting


@pytest.mark.parametrize("stored", [42, -1, "banana", ""], ids=["out-of-range", "negative", "text", "empty"])
def test_unreadable_import_found_video_falls_back_to_ask_every_time(import_settings_service, settings_file, stored):
    settings_file.qsettings.setValue("Import/importFoundVideo", stored)

    assert import_settings_service.import_found_video == LoadFoundVideo.ASK_EVERY_TIME


def test_import_found_video_write_emits_once(import_settings_service, make_spy):
    spy = make_spy(import_settings_service.import_found_video_changed)

    import_settings_service.import_found_video = LoadFoundVideo.ALWAYS

    assert spy.count() == 1
    assert spy.at(0, 0) is LoadFoundVideo.ALWAYS

    import_settings_service.import_found_video = LoadFoundVideo.ALWAYS
    assert spy.count() == 1


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


def test_last_directory_video_write_emits_once(import_settings_service, make_spy):
    spy = make_spy(import_settings_service.last_directory_video_changed)

    import_settings_service.last_directory_video = ELSEWHERE

    assert spy.count() == 1
    assert spy.at(0, 0) == ELSEWHERE

    import_settings_service.last_directory_video = ELSEWHERE
    assert spy.count() == 1


def test_last_directory_documents_write_emits_once(import_settings_service, make_spy):
    spy = make_spy(import_settings_service.last_directory_documents_changed)

    import_settings_service.last_directory_documents = ELSEWHERE

    assert spy.count() == 1
    assert spy.at(0, 0) == ELSEWHERE

    import_settings_service.last_directory_documents = ELSEWHERE
    assert spy.count() == 1


def test_last_directory_subtitles_write_emits_once(import_settings_service, make_spy):
    spy = make_spy(import_settings_service.last_directory_subtitles_changed)

    import_settings_service.last_directory_subtitles = ELSEWHERE

    assert spy.count() == 1
    assert spy.at(0, 0) == ELSEWHERE

    import_settings_service.last_directory_subtitles = ELSEWHERE
    assert spy.count() == 1


def test_every_write_lands_under_its_stored_key_in_the_import_ini_section(
    import_settings_service, settings_file, tmp_path
):
    import_settings_service.import_found_video = LoadFoundVideo.NEVER
    import_settings_service.last_directory_video = ELSEWHERE
    import_settings_service.last_directory_documents = ELSEWHERE
    import_settings_service.last_directory_subtitles = ELSEWHERE
    settings_file.qsettings.sync()

    section = import_section(tmp_path)
    assert "importFoundVideo=2" in section
    # QSettings serializes a QUrl into an opaque variant, so only the key name is readable for the directories
    assert "lastDirectoryVideo=" in section
    assert "lastDirectoryDocuments=" in section
    assert "lastDirectorySubtitles=" in section


def test_a_settings_file_from_the_previous_build_reads_back_unchanged(settings_file, tmp_path):
    settings_file.qsettings.setValue("Import/importFoundVideo", 0)
    settings_file.qsettings.setValue("Import/lastDirectoryVideo", QUrl.fromLocalFile("/videos"))
    settings_file.qsettings.setValue("Import/lastDirectoryDocuments", QUrl.fromLocalFile("/documents"))
    settings_file.qsettings.setValue("Import/lastDirectorySubtitles", QUrl.fromLocalFile("/subtitles"))
    settings_file.qsettings.sync()

    # a fresh handle on the same file, so the values come off disk rather than out of the write cache
    reopened = QSettings(str(tmp_path / "test_settings.ini"), QSettings.Format.IniFormat)
    service = ImportSettingsService(reopened)

    assert service.import_found_video == LoadFoundVideo.ALWAYS
    assert service.last_directory_video == QUrl.fromLocalFile("/videos")
    assert service.last_directory_documents == QUrl.fromLocalFile("/documents")
    assert service.last_directory_subtitles == QUrl.fromLocalFile("/subtitles")
