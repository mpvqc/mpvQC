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
from PySide6.QtCore import QSettings

from mpvqc.services import FilePathService, SettingsService


class TestSettingsServiceInitializer(unittest.TestCase):

    def test_backing_object(self):
        file_service = MagicMock()
        file_service.file_settings = str(Path.home())
        inject.clear_and_configure(lambda binder: binder
                                   .bind(FilePathService, file_service))

        try:
            service = SettingsService()
            settings = service.backing_object
            self.assertIsInstance(settings, QSettings)
        finally:
            inject.clear()
