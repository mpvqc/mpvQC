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
from pathlib import Path
from unittest.mock import MagicMock

import inject
from PySide6.QtCore import QStandardPaths

from mpvqc.services import PlayerService, SettingsService, DocumentExporterService


class TestDocumentExporterService(unittest.TestCase):
    _service = DocumentExporterService()

    def _mock_generate_file_path_proposal_with(self, video: Path or None, nickname: str or None):
        settings_mock = MagicMock()
        settings_mock.nickname = nickname

        player_mock = MagicMock()
        player_mock.mpv.path = str(video) if video else None

        inject.clear_and_configure(lambda binder: binder
                                   .bind(SettingsService, settings_mock)
                                   .bind(PlayerService, player_mock))

    def tearDown(self):
        inject.clear()

    def test_generate_file_path_proposal(self):
        home = Path('/')
        movies = Path(QStandardPaths.writableLocation(QStandardPaths.MoviesLocation))

        # --
        self._mock_generate_file_path_proposal_with(
            video=home / 'Documents' / 'my-movie.mp4',
            nickname='some-nickname'
        )
        expected = home / 'Documents' / '[QC]_my-movie_some-nickname.txt'
        actual = self._service.generate_file_path_proposal()
        self.assertEqual(expected, actual)

        # --
        self._mock_generate_file_path_proposal_with(
            video=home / 'Documents' / 'my-movie.mp4',
            nickname=None
        )
        expected = home / 'Documents' / '[QC]_my-movie.txt'
        actual = self._service.generate_file_path_proposal()
        self.assertEqual(expected, actual)

        # --
        self._mock_generate_file_path_proposal_with(
            video=None,
            nickname='some-nickname'
        )
        expected = movies / '[QC]_untitled_some-nickname.txt'
        actual = self._service.generate_file_path_proposal()
        self.assertEqual(expected, actual)

        # --
        self._mock_generate_file_path_proposal_with(
            video=None,
            nickname=None
        )
        expected = movies / '[QC]_untitled.txt'
        actual = self._service.generate_file_path_proposal()
        self.assertEqual(expected, actual)
