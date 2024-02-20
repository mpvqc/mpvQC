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

import unittest
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import MagicMock

import inject
from PySide6.QtCore import QStandardPaths
from parameterized import parameterized

from mpvqc.services import PlayerService, SettingsService, DocumentExporterService


class TestDocumentExporterService(unittest.TestCase):
    """Comment to enforce space"""

    _movies = Path(QStandardPaths.writableLocation(QStandardPaths.MoviesLocation))
    _home = Path('/')

    @dataclass
    class FilePathProposalTestSet:
        video: Path or None
        nickname: str or None
        expected: Path

    @staticmethod
    def _mock_generate_file_path_proposal_with(video: Path or None, nickname: str or None):
        settings_mock = MagicMock()
        settings_mock.nickname = nickname

        player_mock = MagicMock()
        player_mock.path = str(video) if video else None

        inject.clear_and_configure(lambda binder: binder
                                   .bind(SettingsService, settings_mock)
                                   .bind(PlayerService, player_mock))

    def tearDown(self):
        inject.clear()

    @parameterized.expand([
        FilePathProposalTestSet(
            video=_home / 'Documents' / 'my-movie.mp4',
            nickname='some-nickname',
            expected=_home / 'Documents' / '[QC]_my-movie_some-nickname.txt',
        ),
        FilePathProposalTestSet(
            video=_home / 'Documents' / 'my-movie.mp4',
            nickname=None,
            expected=_home / 'Documents' / '[QC]_my-movie.txt',
        ),
        FilePathProposalTestSet(
            video=None,
            nickname='some-nickname',
            expected=_movies / '[QC]_untitled_some-nickname.txt',
        ),
        FilePathProposalTestSet(
            video=None,
            nickname=None,
            expected=_movies / '[QC]_untitled.txt',
        ),
    ])
    def test_generate_file_path_proposal_2(self, case: 'FilePathProposalTestSet'):
        self._mock_generate_file_path_proposal_with(
            video=case.video,
            nickname=case.nickname,
        )
        actual = DocumentExporterService().generate_file_path_proposal()
        self.assertEqual(case.expected, actual)
