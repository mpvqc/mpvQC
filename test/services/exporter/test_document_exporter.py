# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QStandardPaths, QThreadPool

from mpvqc.services import ExportService


@pytest.fixture
def service(qt_app) -> ExportService:
    return ExportService()


@pytest.fixture
def configure_mocks(qt_app, comments_service_mock, settings_service, player_service_mock):
    def _make_mock(
        video: Path | str | None = None,
        nickname: str | None = None,
        comments: list | None = None,
        subtitles: list | None = None,
        write_header_date: bool = False,
        write_header_generator: bool = False,
        write_header_nickname: bool = False,
        write_header_video_path: bool = False,
        write_header_subtitles: bool = False,
    ):
        comments_service_mock.comments.return_value = comments or []

        settings_service.nickname = nickname
        settings_service.write_header_date = write_header_date
        settings_service.write_header_generator = write_header_generator
        settings_service.write_header_nickname = write_header_nickname
        settings_service.write_header_video_path = write_header_video_path
        settings_service.write_header_subtitles = write_header_subtitles
        settings_service.language = "en-US"

        player_service_mock.path = str(video) if video else None
        player_service_mock.external_subtitles = tuple(str(s) for s in subtitles or ())

    return _make_mock


def wait_for_jobs() -> None:
    QThreadPool.globalInstance().waitForDone()


@dataclass
class FilePathProposalTestSet:
    video: Path | None
    nickname: str | None
    suffix: str
    expected: Path


HOME = Path.home()
MOVIES = Path(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.MoviesLocation))


@pytest.mark.parametrize(
    "case",
    [
        FilePathProposalTestSet(
            video=HOME / "Documents" / "my-movie.mp4",
            nickname="some-nickname",
            suffix="json",
            expected=HOME / "Documents" / "[QC]_my-movie_some-nickname.json",
        ),
        FilePathProposalTestSet(
            video=HOME / "Documents" / "my-movie.mp4",
            nickname=None,
            suffix="txt",
            expected=HOME / "Documents" / "[QC]_my-movie.txt",
        ),
        FilePathProposalTestSet(
            video=None,
            nickname="some-nickname",
            suffix="txt",
            expected=MOVIES / "[QC]_untitled_some-nickname.txt",
        ),
        FilePathProposalTestSet(
            video=None,
            nickname=None,
            suffix="json",
            expected=MOVIES / "[QC]_untitled.json",
        ),
    ],
)
def test_generates_file_path_proposals(case, configure_mocks, service):
    configure_mocks(video=case.video, nickname=case.nickname)
    actual = service.generate_file_path_proposal(case.suffix)
    assert actual == case.expected


def test_save_writes_v1_document(configure_mocks, service, tmp_path, make_spy):
    configure_mocks()
    error_spy = make_spy(service.export_error_occurred)
    file = tmp_path / "saved.json"

    service.save(file)
    wait_for_jobs()

    assert json.loads(file.read_text(encoding="utf-8"))["version"] == 1
    assert error_spy.count() == 0


def test_save_signals_on_write_failure(configure_mocks, service, make_spy):
    configure_mocks()
    error_spy = make_spy(service.export_error_occurred)
    file_mock = MagicMock()
    file_mock.write_text.side_effect = PermissionError("read-only target")

    service.save(file_mock)
    wait_for_jobs()

    assert error_spy.count() == 1
    assert error_spy.at(invocation=0, argument=1) == -1


def test_save_records_save(configure_mocks, service, tmp_path, state_service_mock):
    configure_mocks()
    file = tmp_path / "saved.txt"

    service.save(file)
    wait_for_jobs()

    state_service_mock.record_save.assert_called_once_with(file)


def test_save_failure_does_not_record_save(configure_mocks, service, state_service_mock):
    configure_mocks()
    file_mock = MagicMock()
    file_mock.write_text.side_effect = PermissionError("read-only target")

    service.save(file_mock)
    wait_for_jobs()

    state_service_mock.record_save.assert_not_called()


def test_export_classic_writes_classic_document_without_recording(
    configure_mocks, service, tmp_path, state_service_mock
):
    configure_mocks()
    file = tmp_path / "export.txt"

    service.export_classic(file)
    wait_for_jobs()

    assert file.read_text(encoding="utf-8").startswith("[FILE]")
    state_service_mock.record_save.assert_not_called()


def test_export_classic_signals_on_write_failure(configure_mocks, service, make_spy):
    configure_mocks()
    error_spy = make_spy(service.export_error_occurred)
    file_mock = MagicMock()
    file_mock.write_text.side_effect = PermissionError("read-only target")

    service.export_classic(file_mock)
    wait_for_jobs()

    assert error_spy.count() == 1
    assert error_spy.at(invocation=0, argument=1) == -1


def test_export_custom_succeeds(configure_mocks, service, tmp_path, make_spy):
    configure_mocks(nickname="lorem")
    error_spy = make_spy(service.export_error_occurred)
    template = tmp_path / "template.jinja"
    template.write_text("nick: {{ nickname }}", encoding="utf-8")
    file = tmp_path / "export.txt"

    service.export_custom(file, template)
    wait_for_jobs()

    assert error_spy.count() == 0
    assert file.read_text(encoding="utf-8") == "nick: lorem"


@pytest.mark.parametrize(
    ("template_content", "expected_lineno"),
    [
        ("{% if %}", 1),
        ("{{ undefined_thing() }}", -1),
    ],
)
def test_export_custom_signals_on_render_failure(
    configure_mocks, service, tmp_path, make_spy, template_content, expected_lineno
):
    configure_mocks()
    error_spy = make_spy(service.export_error_occurred)
    template = tmp_path / "template.jinja"
    template.write_text(template_content, encoding="utf-8")

    service.export_custom(tmp_path / "export.txt", template)
    wait_for_jobs()

    assert error_spy.count() == 1
    assert error_spy.at(invocation=0, argument=0)
    assert error_spy.at(invocation=0, argument=1) == expected_lineno


@pytest.mark.parametrize(
    "read_error",
    [
        UnicodeDecodeError("utf-8", b"\xff", 0, 1, "invalid"),
        FileNotFoundError("template gone"),
    ],
)
def test_export_custom_signals_on_template_read_failure(configure_mocks, service, make_spy, read_error):
    configure_mocks()
    error_spy = make_spy(service.export_error_occurred)
    template_mock = MagicMock()
    template_mock.read_text.side_effect = read_error

    service.export_custom(MagicMock(), template_mock)
    wait_for_jobs()

    assert error_spy.count() == 1
    assert error_spy.at(invocation=0, argument=1) == -1


def test_export_custom_signals_on_write_failure(configure_mocks, service, tmp_path, make_spy):
    configure_mocks()
    error_spy = make_spy(service.export_error_occurred)
    template = tmp_path / "template.jinja"
    template.write_text("static", encoding="utf-8")
    file_mock = MagicMock()
    file_mock.write_text.side_effect = PermissionError("read-only target")

    service.export_custom(file_mock, template)
    wait_for_jobs()

    assert error_spy.count() == 1
    assert error_spy.at(invocation=0, argument=1) == -1


def test_backup_writes_archive(configure_mocks, service, application_paths_service_mock, tmp_path):
    application_paths_service_mock.dir_backup = tmp_path
    configure_mocks(comments=[{"time": 50 * 1000, "commentType": "Spelling", "comment": "My comment"}])

    service.backup()
    wait_for_jobs()

    assert len(list(tmp_path.glob("*.zip"))) == 1


def test_backup_failure_is_logged(configure_mocks, service, application_paths_service_mock, tmp_path, caplog):
    application_paths_service_mock.dir_backup = tmp_path / "does-not-exist"
    configure_mocks()

    service.backup()
    wait_for_jobs()

    assert "Failed to create backup" in caplog.text
    assert not (tmp_path / "does-not-exist").exists()
