# mpvQC
#
# Copyright (C) 2022 mpvQC developers
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
from PySide6.QtCore import QSettings
from parameterized import parameterized

from mpvqc.services import ApplicationPathsService, SettingsService


class SettingsServiceTest(unittest.TestCase):
    _path = Path()

    # https://github.com/wolever/parameterized

    def setUp(self):
        mock = MagicMock()
        mock.file_settings = self._path
        inject.clear_and_configure(lambda binder: binder
                                   .bind(ApplicationPathsService, mock))
        self._settings = SettingsService()

    def tearDown(self):
        inject.clear()

    def _mock_settings(self, values: dict[str, ...]):
        q_settings = QSettings(f'{self._path}', QSettings.Format.IniFormat)
        q_settings.clear()
        for key, value in values.items():
            q_settings.setValue(key, value)
        self._settings._settings = q_settings

    @parameterized.expand([
        ({}, ''),
        ({'Export/nickname': ''}, ''),
        ({'Export/nickname': True}, 'True'),
        ({'Export/nickname': 1}, '1'),
        ({'Export/nickname': 'nick'}, 'nick'),
    ])
    def test_string(self, input, expected):
        self._mock_settings(input)
        self.assertEqual(expected, self._settings.nickname)

    def test_string_with_default(self):
        self._mock_settings({})
        self.assertEqual('en-US', self._settings.language)

    @parameterized.expand([
        ({}, False),
        ({'Export/writeHeaderDate': ''}, False),
        ({'Export/writeHeaderDate': True}, True),
        ({'Export/writeHeaderDate': 1}, False),
        ({'Export/writeHeaderDate': 'true'}, True),
    ])
    def test_bool(self, input, expected):
        self._mock_settings(input)
        self.assertEqual(expected, self._settings.writeHeaderDate)
