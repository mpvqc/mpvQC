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
import unittest
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import inject
from PySide6.QtCore import QStandardPaths
from jinja2 import TemplateSyntaxError, TemplateError
from parameterized import parameterized

from mpvqc.services import (
    PlayerService,
    SettingsService,
    DocumentExportService,
    DocumentRenderService,
    DocumentBackupService,
    ApplicationPathsService,
    ResourceService,
)

_mock_app = MagicMock()


def _mock_test_data(
    video: Path or str or None = None,
    nickname: str or None = None,
    comments: list or None = None,
    write_header_date: str or None = None,
    write_header_generator: str or None = None,
    write_header_video_path: str or None = None,
    write_header_nickname: str or None = None,
):
    _mock_app.find_object.return_value.comments.return_value = comments or []

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

    # fmt: off
    inject.clear_and_configure(lambda binder: binder
                               .bind(SettingsService, settings_mock)
                               .bind(PlayerService, player_mock))
    # fmt: on


class DocumentRenderServiceTest(unittest.TestCase):
    _resources: ResourceService = inject.attr(ResourceService)

    @patch("mpvqc.services.document_exporter.QCoreApplication.instance", return_value=_mock_app)
    def test_video_path_video_name(
        self,
        *_,
    ):
        _mock_test_data(video=Path.home() / "video.mkv")
        service = DocumentRenderService()

        template = textwrap.dedent(
            """\
            video_path: {{ video_path }}
            video_name: {{ video_name }}
            """
        )
        expected = textwrap.dedent(
            f"""\
            video_path: {Path.home() / 'video.mkv'}
            video_name: video.mkv
            """
        )
        actual = service.render(template)
        self.assertEqual(expected, actual)

        _mock_test_data(video=None)
        expected = textwrap.dedent(
            """\
            video_path: 
            video_name: 
            """
        )
        actual = service.render(template)
        self.assertEqual(expected, actual)

    @patch("mpvqc.services.document_exporter.QCoreApplication.instance", return_value=_mock_app)
    def test_ends_with_line_break(self, *_):
        _mock_test_data()
        actual = DocumentRenderService().render(self._resources.default_export_template)
        self.assertEqual("\n", actual[-1])

    @patch("mpvqc.services.document_exporter.QCoreApplication.instance", return_value=_mock_app)
    def test_render_no_header(self, *_):
        _mock_test_data()

        expected = textwrap.dedent(
            """\
            [FILE]
    
            [DATA]
            # total lines: 0
            """
        )
        actual = DocumentRenderService().render(self._resources.default_export_template)

        self.assertEqual(expected, actual)

    @patch("mpvqc.services.document_exporter.QCoreApplication.instance", return_value=_mock_app)
    def test_render_partial_header(self, *_):
        _mock_test_data(
            write_header_video_path=True, video="/path/to/video", write_header_nickname=True, nickname="ಠ_ಠ"
        )

        expected = textwrap.dedent(
            f"""\
            [FILE]
            nick      : ಠ_ಠ
            path      : {Path('/path/to/video')}
    
            [DATA]
            # total lines: 0
            """
        )
        actual = DocumentRenderService().render(self._resources.default_export_template)

        self.assertEqual(expected, actual)

    @patch("mpvqc.services.document_exporter.QCoreApplication.instance", return_value=_mock_app)
    def test_render_comments(self, *_):
        _mock_test_data(
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
        actual = DocumentRenderService().render(self._resources.default_export_template)

        self.assertEqual(expected, actual)

    @patch("mpvqc.services.document_exporter.QCoreApplication.instance", return_value=_mock_app)
    def test_render_backup(self, *_):
        _mock_test_data(
            write_header_video_path=False,
            video="/path/to/video/ignore/user/setting",
            comments=[
                {"time": 0, "commentType": "Translation", "comment": "My first comment"},
                {"time": 50, "commentType": "Spelling", "comment": "My second comment"},
                {"time": 100, "commentType": "Phrasing", "comment": "My third comment"},
            ],
        )

        rendered = DocumentRenderService().render(self._resources.backup_template)

        self.assertIn(f'path      : {Path("/path/to/video/ignore/user/setting")}', rendered)
        self.assertIn("[00:00:00] [Translation] My first comment", rendered)
        self.assertIn("[00:00:50] [Spelling] My second comment", rendered)
        self.assertIn("[00:01:40] [Phrasing] My third comment", rendered)
        self.assertIn("# total lines: 3", rendered)


class DocumentBackupServiceTest(unittest.TestCase):
    MODULE = "mpvqc.services.document_exporter"

    any_directory = Path("any-directory")

    def setUp(self):
        paths_mock = MagicMock()
        paths_mock.is_portable = True
        paths_mock.dir_backup = self.any_directory

        player_mock = MagicMock()
        player_mock.has_video = True

        # fmt: off
        inject.clear_and_configure(lambda binder: binder
                                   .bind(ApplicationPathsService, paths_mock)
                                   .bind(PlayerService, player_mock))
        # fmt: on

    def tearDown(self):
        inject.clear()

    @patch(f"{MODULE}.ZipFile")
    @patch("mpvqc.services.document_exporter.QCoreApplication.instance", return_value=_mock_app)
    def test_zip_name(self, q_app, zip_file_mock: MagicMock):
        _mock_test_data()

        service = DocumentBackupService()
        service.backup()

        zip_file_mock.assert_called()

        zip_name = zip_file_mock.call_args.args[0]
        self.assertEqual(f"{datetime.now():%Y-%m}.zip", zip_name.name)

    @patch(f"{MODULE}.ZipFile")
    @patch("mpvqc.services.document_exporter.QCoreApplication.instance", return_value=_mock_app)
    def test_zip_content(self, q_app, zip_file_mock: MagicMock):
        _mock_test_data(
            video="/path/to/nice/video",
            comments=[
                {"time": 0, "commentType": "Frrrranky", "comment": "Suuuuuuuper"},
            ],
        )

        service = DocumentBackupService()
        service.backup()

        writestr_mock = zip_file_mock.return_value.__enter__.return_value.writestr
        writestr_mock.assert_called()

        filename, content = writestr_mock.call_args.args
        self.assertIn(f"{datetime.now():%Y-%m-%d}", filename)
        self.assertIn(f'{Path("/path/to/nice/video")}', content)
        self.assertIn("[00:00:00] [Frrrranky] Suuuuuuuper", content)


class DocumentExportServiceTest(unittest.TestCase):
    """"""

    _movies = Path(QStandardPaths.writableLocation(QStandardPaths.MoviesLocation))
    _home = Path.home()

    @dataclass
    class FilePathProposalTestSet:
        video: Path or None
        nickname: str or None
        expected: Path

    def setUp(self):
        self._resources_mock = MagicMock()
        self._resources_mock.default_export_template = "template"
        self._file_mock = MagicMock()
        self._template_mock = MagicMock()

        self._renderer_mock = MagicMock()
        # fmt: off
        inject.clear_and_configure(lambda binder: binder
                                   .bind(DocumentRenderService, self._renderer_mock))
        # fmt: on

    def tearDown(self):
        inject.clear()

    @parameterized.expand(
        [
            FilePathProposalTestSet(
                video=_home / "Documents" / "my-movie.mp4",
                nickname="some-nickname",
                expected=_home / "Documents" / "[QC]_my-movie_some-nickname.txt",
            ),
            FilePathProposalTestSet(
                video=_home / "Documents" / "my-movie.mp4",
                nickname=None,
                expected=_home / "Documents" / "[QC]_my-movie.txt",
            ),
            FilePathProposalTestSet(
                video=None,
                nickname="some-nickname",
                expected=_movies / "[QC]_untitled_some-nickname.txt",
            ),
            FilePathProposalTestSet(
                video=None,
                nickname=None,
                expected=_movies / "[QC]_untitled.txt",
            ),
        ]
    )
    def test_generate_file_path_proposal_2(self, case: "FilePathProposalTestSet"):
        _mock_test_data(video=case.video, nickname=case.nickname)
        actual = DocumentExportService().generate_file_path_proposal()
        self.assertEqual(case.expected, actual)

    def test_export(self):
        service = DocumentExportService()
        error = service.export(self._file_mock, self._template_mock)

        self._template_mock.read_text.assert_called_once()
        self._renderer_mock.render.assert_called_once()
        self._file_mock.write_text.assert_called_once()
        self.assertIsNone(error)

        self._renderer_mock.render.side_effect = TemplateSyntaxError(message="error", lineno=42)
        error = service.export(self._file_mock, self._template_mock)
        self.assertIsNotNone(error)
        self.assertEqual("error", error.message)
        self.assertEqual(42, error.line_nr)

        self._renderer_mock.render.side_effect = TemplateError(message="error #2")
        error = service.export(self._file_mock, self._template_mock)
        self.assertIsNotNone(error)
        self.assertEqual("error #2", error.message)
        self.assertIsNone(error.line_nr)

    def test_save(self):
        service = DocumentExportService()
        service.save(self._file_mock)

        self._renderer_mock.render.assert_called_once()
        self._file_mock.write_text.assert_called_once()
