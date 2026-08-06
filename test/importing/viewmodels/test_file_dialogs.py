# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest
from PySide6.QtCore import QUrl

from mpvqc.importing.domain import DOCUMENT_EXTENSIONS, SUBTITLE_EXTENSIONS
from mpvqc.importing.services import ImporterService, ImportSettingsService
from mpvqc.importing.viewmodels import MpvqcImportFileDialogViewModel


@pytest.fixture
def importer_service_mock() -> MagicMock:
    return MagicMock(spec_set=ImporterService)


@pytest.fixture
def import_settings_service_mock() -> MagicMock:
    return MagicMock(spec_set=ImportSettingsService)


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, importer_service_mock, import_settings_service_mock):
    def custom_bindings(binder: inject.Binder):
        binder.bind(ImporterService, importer_service_mock)
        binder.bind(ImportSettingsService, import_settings_service_mock)

    common_bindings_with(custom_bindings)


@pytest.fixture
def view_model() -> MpvqcImportFileDialogViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcImportFileDialogViewModel()


def test_video_file_glob_pattern_includes_fixed_fallback_patterns(view_model):
    pattern = view_model.videoFileGlobPattern

    assert "*.avi" in pattern
    assert "*.mkv" in pattern
    assert "*.mp4" in pattern


def test_document_file_glob_pattern_wraps_sorted_extensions(view_model):
    expected = f" ({' '.join(sorted(f'*{ext}' for ext in DOCUMENT_EXTENSIONS))})"

    assert view_model.documentFileGlobPattern == expected


def test_subtitle_file_glob_pattern_wraps_sorted_extensions(view_model):
    expected = f" ({' '.join(sorted(f'*{ext}' for ext in SUBTITLE_EXTENSIONS))})"

    assert view_model.subtitleFileGlobPattern == expected


def test_last_directory_properties_read_through_to_settings(view_model, import_settings_service_mock):
    import_settings_service_mock.last_directory_video = QUrl.fromLocalFile("/videos")
    import_settings_service_mock.last_directory_documents = QUrl.fromLocalFile("/documents")
    import_settings_service_mock.last_directory_subtitles = QUrl.fromLocalFile("/subtitles")

    assert view_model.lastDirectoryVideo == QUrl.fromLocalFile("/videos")
    assert view_model.lastDirectoryDocuments == QUrl.fromLocalFile("/documents")
    assert view_model.lastDirectorySubtitles == QUrl.fromLocalFile("/subtitles")


def test_open_video_forwards_the_selected_file_to_the_importer(view_model, importer_service_mock, tmp_path):
    file = tmp_path / "movie.mkv"

    view_model.openVideo(QUrl.fromLocalFile(str(file)))

    documents, videos, subtitles = importer_service_mock.open.call_args.args
    assert documents == []
    assert [path.name for path in videos] == ["movie.mkv"]
    assert subtitles == []


def test_open_documents_forwards_the_selected_files_to_the_importer(view_model, importer_service_mock, tmp_path):
    urls = [QUrl.fromLocalFile(str(tmp_path / "a.txt")), QUrl.fromLocalFile(str(tmp_path / "b.json"))]

    view_model.openDocuments(urls)

    documents, videos, subtitles = importer_service_mock.open.call_args.args
    assert [path.name for path in documents] == ["a.txt", "b.json"]
    assert videos == []
    assert subtitles == []


def test_open_subtitles_forwards_the_selected_files_to_the_importer(view_model, importer_service_mock, tmp_path):
    urls = [QUrl.fromLocalFile(str(tmp_path / "a.srt")), QUrl.fromLocalFile(str(tmp_path / "b.ass"))]

    view_model.openSubtitles(urls)

    documents, videos, subtitles = importer_service_mock.open.call_args.args
    assert documents == []
    assert videos == []
    assert [path.name for path in subtitles] == ["a.srt", "b.ass"]


def test_open_video_saves_the_selected_files_parent_directory(view_model, import_settings_service_mock, tmp_path):
    folder = tmp_path / "videos"
    folder.mkdir()

    view_model.openVideo(QUrl.fromLocalFile(str(folder / "movie.mkv")))

    assert import_settings_service_mock.last_directory_video == QUrl.fromLocalFile(str(folder))


def test_open_documents_saves_the_first_selected_files_parent_directory(
    view_model, import_settings_service_mock, tmp_path
):
    first_folder = tmp_path / "first"
    first_folder.mkdir()
    second_folder = tmp_path / "second"
    second_folder.mkdir()

    view_model.openDocuments(
        [QUrl.fromLocalFile(str(first_folder / "a.txt")), QUrl.fromLocalFile(str(second_folder / "b.json"))]
    )

    assert import_settings_service_mock.last_directory_documents == QUrl.fromLocalFile(str(first_folder))


def test_open_subtitles_saves_the_first_selected_files_parent_directory(
    view_model, import_settings_service_mock, tmp_path
):
    first_folder = tmp_path / "first"
    first_folder.mkdir()
    second_folder = tmp_path / "second"
    second_folder.mkdir()

    view_model.openSubtitles(
        [QUrl.fromLocalFile(str(first_folder / "a.srt")), QUrl.fromLocalFile(str(second_folder / "b.ass"))]
    )

    assert import_settings_service_mock.last_directory_subtitles == QUrl.fromLocalFile(str(first_folder))


def test_the_next_video_dialog_opens_in_the_directory_the_last_one_saved(
    view_model, import_settings_service_mock, tmp_path
):
    folder = tmp_path / "videos"
    folder.mkdir()

    view_model.openVideo(QUrl.fromLocalFile(str(folder / "movie.mkv")))
    next_view_model = MpvqcImportFileDialogViewModel()

    assert next_view_model.lastDirectoryVideo == QUrl.fromLocalFile(str(folder))
