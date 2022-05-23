#  mpvQC
#
#  Copyright (C) 2022 mpvQC developers
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


import unittest
from pathlib import Path
from unittest.mock import MagicMock

import inject
from PySide6.QtCore import QStandardPaths, QCoreApplication

from mpvqc.services import AppEnvironmentService, FilePathService


class TestPortableFileService(unittest.TestCase):
    executing_dir = Path.home()

    def setUp(self):
        mock = MagicMock()
        mock.is_portable = True
        mock.executing_directory = self.executing_dir
        inject.clear_and_configure(lambda binder: binder
                                   .bind(AppEnvironmentService, mock))

    def tearDown(self):
        inject.clear()

    def test_directory_backup(self):
        service = FilePathService()
        expected = self.executing_dir / 'appdata' / 'backups'
        actual = service.dir_backup
        self.assertEqual(expected, actual)

    def test_directory_config(self):
        service = FilePathService()
        expected = self.executing_dir / 'appdata'
        actual = service.dir_config
        self.assertEqual(expected, actual)

    def test_directory_screenshots(self):
        service = FilePathService()
        expected = self.executing_dir / 'appdata' / 'screenshots'
        actual = service.dir_screenshots
        self.assertEqual(expected, actual)

    def test_file_input_conf(self):
        service = FilePathService()
        expected = self.executing_dir / 'appdata' / 'input.conf'
        actual = service.file_input_conf
        self.assertEqual(expected, actual)

    def test_file_mpv_conf(self):
        service = FilePathService()
        expected = self.executing_dir / 'appdata' / 'mpv.conf'
        actual = service.file_mpv_conf
        self.assertEqual(expected, actual)

    def test_file_settings(self):
        service = FilePathService()
        expected = self.executing_dir / 'appdata' / 'settings.ini'
        actual = service.file_settings
        self.assertEqual(expected, actual)


class TestNonPortableFileService(unittest.TestCase):
    MODULE = 'mpvqc.impl.file_service_non_portable'
    executing_dir = Path.home()

    def setUp(self):
        QCoreApplication.setApplicationName('mpvQC')
        mock = MagicMock()
        mock.is_portable = False
        inject.clear_and_configure(lambda binder: binder
                                   .bind(AppEnvironmentService, mock))

    def tearDown(self):
        inject.clear()

    def test_directory_backup(self, *_):
        service = FilePathService()
        expected = Path(QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)) / 'mpvQC' / 'backups'
        actual = service.dir_backup
        self.assertEqual(expected, actual)

    def test_directory_config(self, *_):
        service = FilePathService()
        expected = Path(QStandardPaths.writableLocation(QStandardPaths.AppConfigLocation))
        actual = service.dir_config
        self.assertEqual(expected, actual)

    def test_directory_screenshots(self, *_):
        service = FilePathService()
        expected = Path(QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)) / 'mpvQC'
        actual = service.dir_screenshots
        self.assertEqual(expected, actual)

    def test_file_input_conf(self, *_):
        service = FilePathService()
        expected = Path.home() / '.config' / 'mpvQC' / 'input.conf'
        actual = service.file_input_conf
        self.assertEqual(expected, actual)

    def test_file_mpv_conf(self, *_):
        service = FilePathService()
        expected = Path.home() / '.config' / 'mpvQC' / 'mpv.conf'
        actual = service.file_mpv_conf
        self.assertEqual(expected, actual)

    def test_file_settings(self, *_):
        service = FilePathService()
        expected = Path.home() / '.config' / 'mpvQC' / 'settings.ini'
        actual = service.file_settings
        self.assertEqual(expected, actual)
