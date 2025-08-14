# mpvQC
#
# Copyright (C) 2024
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import textwrap
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import inject
import pytest
from jinja2 import TemplateError, TemplateSyntaxError
from PySide6.QtCore import QStandardPaths

from mpvqc.services import (
    DocumentBackupService,
    DocumentExportService,
    DocumentRenderService,
    PlayerService,
    ResourceReaderService,
    ResourceService,
    SettingsService,
)

MODULE = "mpvqc.services.document_exporter"


@pytest.fixture
def qt_app():
    with patch(f"{MODULE}.QCoreApplication.instance", return_value=MagicMock()) as mock:
        yield mock.return_value


@pytest.fixture
def zip_file():
    with patch(f"{MODULE}.ZipFile", return_value=MagicMock()) as mock:
        yield mock


@pytest.fixture
def resource_service() -> ResourceService:
    return ResourceService()


@pytest.fixture
def make_mock(qt_app):
    def _make_mock(
        video: Path | str | None = None,
        nickname: str | None = None,
        comments: list | None = None,
        write_header_date: bool | None = None,
        write_header_generator: bool | None = None,
        write_header_video_path: bool | None = None,
        write_header_nickname: bool | None = None,
    ):
        qt_app.find_object.return_value.comments.return_value = comments or []

        player_mock = MagicMock()
        player_mock.path = str(video) if video else None
        player_mock.has_video = bool(video)

        settings_mock = MagicMock()
        settings_mock.nickname = nickname
        settings_mock.writeHeaderDate = write_header_date
        settings_mock.writeHeaderGenerator = write_header_generator
        settings_mock.writeHeaderVideoPath = write_header_video_path
        settings_mock.writeHeaderNickname = write_header_nickname
        settings_mock.language = "en-US"

        def config(binder: inject.Binder):
            binder.bind(PlayerService, player_mock)
            binder.bind(SettingsService, settings_mock)
            binder.bind(ResourceReaderService, ResourceReaderService())
            binder.bind(ResourceService, ResourceService())

        inject.configure(config, clear=True)

    return _make_mock


@pytest.fixture
def document_renderer_service_mock() -> MagicMock:
    mock = MagicMock()

    def config(binder: inject.Binder):
        binder.bind(DocumentRenderService, mock)

    inject.configure(config, clear=True)
    return mock


@pytest.fixture
def document_render_service() -> DocumentRenderService:
    return DocumentRenderService()


@pytest.fixture
def document_backup_service() -> DocumentBackupService:
    return DocumentBackupService()


@pytest.fixture
def document_exporter_service() -> DocumentExportService:
    return DocumentExportService()


def test_render_service_video_path_video_name(make_mock, document_render_service):
    template = textwrap.dedent(
        """\
        video_path: {{ video_path }}
        video_name: {{ video_name }}
        """
    )

    make_mock(video=Path.home() / "video.mkv")
    expected = textwrap.dedent(f"""\
        video_path: {Path.home() / "video.mkv"}
        video_name: video.mkv
        """)
    actual = document_render_service.render(template)
    assert actual == expected

    make_mock(video=None)
    expected = textwrap.dedent("""video_path: \nvideo_name: \n""")
    actual = document_render_service.render(template)
    assert actual == expected


def test_render_service_renders_text_that_ends_with_newline(make_mock, document_render_service, resource_service):
    make_mock()
    actual = document_render_service.render(resource_service.default_export_template)
    assert actual[-1] == "\n"


def test_render_service_renders_no_headers(make_mock, document_render_service, resource_service):
    make_mock()

    expected = textwrap.dedent(
        """\
        [FILE]

        [DATA]
        # total lines: 0
        """
    )
    actual = document_render_service.render(resource_service.default_export_template)
    assert expected == actual


def test_render_service_renders_partial_headers(make_mock, document_render_service, resource_service):
    make_mock(
        write_header_video_path=True,
        video="/path/to/video",
        write_header_nickname=True,
        nickname="ಠ_ಠ",
    )

    expected = textwrap.dedent(
        f"""\
        [FILE]
        nick      : ಠ_ಠ
        path      : {Path("/path/to/video")}

        [DATA]
        # total lines: 0
        """
    )
    actual = document_render_service.render(resource_service.default_export_template)
    assert expected == actual


def test_render_service_renders_comments(make_mock, document_render_service, resource_service):
    make_mock(
        comments=[
            {"time": 0, "commentType": "Translation", "comment": "My first comment"},
            {"time": 50, "commentType": "Spelling", "comment": "My second comment"},
            {"time": 100, "commentType": "Phrasing", "comment": "My third comment"},
        ]
    )

    expected = textwrap.dedent(
        """\
        [FILE]

        [DATA]
        [00:00:00] [Translation] My first comment
        [00:00:50] [Spelling] My second comment
        [00:01:40] [Phrasing] My third comment
        # total lines: 3
        """
    )
    actual = document_render_service.render(resource_service.default_export_template)
    assert expected == actual


def test_renderer_service_renders_backup(make_mock, document_render_service, resource_service):
    make_mock(
        write_header_video_path=False,
        video="/path/to/video/ignore/user/setting",
        comments=[
            {"time": 0, "commentType": "Translation", "comment": "My first comment"},
            {"time": 50, "commentType": "Spelling", "comment": "My second comment"},
            {"time": 100, "commentType": "Phrasing", "comment": "My third comment"},
        ],
    )

    rendered = document_render_service.render(resource_service.backup_template)

    assert f"path      : {Path('/path/to/video/ignore/user/setting')}" in rendered
    assert "[00:00:00] [Translation] My first comment" in rendered
    assert "[00:00:50] [Spelling] My second comment" in rendered
    assert "[00:01:40] [Phrasing] My third comment" in rendered
    assert "# total lines: 3" in rendered


def test_backup_service_archive_name(make_mock, zip_file, document_backup_service):
    make_mock()

    document_backup_service.backup()

    assert zip_file.called
    zip_name = zip_file.call_args.args[0]
    assert zip_name.name == f"{datetime.now(UTC):%Y-%m}.zip"


def test_backup_service_performs_backup(make_mock, zip_file, document_backup_service):
    make_mock(
        video="/path/to/nice/video",
        comments=[
            {"time": 0, "commentType": "Frrrranky", "comment": "Suuuuuuuper"},
        ],
    )

    document_backup_service.backup()

    writestr_mock = zip_file.return_value.__enter__.return_value.writestr
    assert writestr_mock.called

    filename, content = writestr_mock.call_args.args
    assert f"{datetime.now(UTC):%Y-%m-%d}" in filename
    assert f"{Path('/path/to/nice/video')}" in content
    assert "[00:00:00] [Frrrranky] Suuuuuuuper" in content


@dataclass
class FilePathProposalTestSet:
    video: Path | None
    nickname: str | None
    expected: Path


HOME = Path.home()
MOVIES = Path(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.MoviesLocation))


@pytest.mark.parametrize(
    "case",
    [
        FilePathProposalTestSet(
            video=HOME / "Documents" / "my-movie.mp4",
            nickname="some-nickname",
            expected=HOME / "Documents" / "[QC]_my-movie_some-nickname.txt",
        ),
        FilePathProposalTestSet(
            video=HOME / "Documents" / "my-movie.mp4",
            nickname=None,
            expected=HOME / "Documents" / "[QC]_my-movie.txt",
        ),
        FilePathProposalTestSet(
            video=None,
            nickname="some-nickname",
            expected=MOVIES / "[QC]_untitled_some-nickname.txt",
        ),
        FilePathProposalTestSet(
            video=None,
            nickname=None,
            expected=MOVIES / "[QC]_untitled.txt",
        ),
    ],
)
def test_document_exporter_generates_file_path_proposals(case, make_mock, document_exporter_service):
    make_mock(video=case.video, nickname=case.nickname)
    actual = document_exporter_service.generate_file_path_proposal()
    assert actual == case.expected


def test_document_exporter_exports(document_exporter_service, document_renderer_service_mock):
    template_mock = MagicMock()
    file_mock = MagicMock()

    error = document_exporter_service.export(file_mock, template_mock)
    assert error is None
    assert template_mock.read_text.called
    assert file_mock.write_text.called
    assert document_renderer_service_mock.render.called

    document_renderer_service_mock.render.side_effect = TemplateSyntaxError(message="error", lineno=42)
    error = document_exporter_service.export(file_mock, template_mock)
    assert error is not None
    assert error.message == "error"
    assert error.line_nr == 42

    document_renderer_service_mock.render.side_effect = TemplateError(message="error #2")
    error = document_exporter_service.export(file_mock, template_mock)
    assert error is not None
    assert error.message == "error #2"
    assert error.line_nr is None


def test_document_exporter_saves(document_exporter_service, document_renderer_service_mock):
    file_mock = MagicMock()

    document_exporter_service.save(file_mock)

    assert document_renderer_service_mock.render.called
    assert file_mock.write_text.called
