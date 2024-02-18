# mpvQC
#
# Copyright (C) 2024 mpvQC developers
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

from mpvqc.pyobjects import MpvqcExportTemplateModelPyObject
from mpvqc.services import ApplicationPathsService


class TestExportTemplatesModel(unittest.TestCase):

    @staticmethod
    def _mock(paths: tuple[Path, ...]):
        # noinspection PyCallingNonCallable
        mock = MagicMock()
        mock.files_export_templates = paths
        inject.clear_and_configure(lambda binder: binder
                                   .bind(ApplicationPathsService, mock))

    def tearDown(self):
        inject.clear()

    def test_templates(self):
        self._mock(paths=(Path.home(), Path.cwd()))

        # noinspection PyCallingNonCallable
        model = MpvqcExportTemplateModelPyObject()

        expected = 2
        actual = model.rowCount()
        self.assertEqual(expected, actual)

    def test_no_templates(self):
        self._mock(paths=())

        # noinspection PyCallingNonCallable
        model = MpvqcExportTemplateModelPyObject()

        expected = 0
        actual = model.rowCount()
        self.assertEqual(expected, actual)
