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

from mpvqc.services import ApplicationEnvironmentService, ApplicationPathsService


class ApplicationPathsServiceTest(unittest.TestCase):
    executing_dir = Path.home()

    def _mock(self, portable: bool = False):
        mock = MagicMock()
        mock.is_portable = portable
        mock.executing_directory = self.executing_dir
        # fmt: off
        inject.clear_and_configure(lambda binder: binder
                                   .bind(ApplicationEnvironmentService, mock))
        # fmt: on

    def tearDown(self):
        inject.clear()

    def test_path_distinction(self):
        self._mock(portable=False)
        service = ApplicationPathsService()
        self.assertNotIn("appdata", f"{service.dir_config}")

        self._mock(portable=True)
        service = ApplicationPathsService()
        self.assertIn("appdata", f"{service.dir_config}")

    def test_directory_backup(self):
        self._mock(portable=True)
        service = ApplicationPathsService()
        expected = self.executing_dir / "appdata" / "backups"
        actual = service.dir_backup
        self.assertEqual(expected, actual)

    def test_directory_config(self):
        self._mock(portable=True)
        service = ApplicationPathsService()
        expected = self.executing_dir / "appdata"
        actual = service.dir_config
        self.assertEqual(expected, actual)

    def test_directory_screenshots(self):
        self._mock(portable=True)
        service = ApplicationPathsService()
        expected = self.executing_dir / "appdata" / "screenshots"
        actual = service.dir_screenshots
        self.assertEqual(expected, actual)

    def test_directory_export_templates(self):
        self._mock(portable=True)
        service = ApplicationPathsService()
        expected = self.executing_dir / "appdata" / "export-templates"
        actual = service.dir_export_templates
        self.assertEqual(expected, actual)

    def test_file_input_conf(self):
        self._mock(portable=True)
        service = ApplicationPathsService()
        expected = self.executing_dir / "appdata" / "input.conf"
        actual = service.file_input_conf
        self.assertEqual(expected, actual)

    def test_file_mpv_conf(self):
        self._mock(portable=True)
        service = ApplicationPathsService()
        expected = self.executing_dir / "appdata" / "mpv.conf"
        actual = service.file_mpv_conf
        self.assertEqual(expected, actual)

    def test_file_settings(self):
        self._mock(portable=True)
        service = ApplicationPathsService()
        expected = self.executing_dir / "appdata" / "settings.ini"
        actual = service.file_settings
        self.assertEqual(expected, actual)
