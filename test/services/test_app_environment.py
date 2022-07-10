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


import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from mpvqc.services import AppEnvironmentService


class TestAppEnvironmentService(unittest.TestCase):
    MODULE = 'mpvqc.services.app_environment'

    def test_executing_directory_as_distributable(self):
        try:
            setattr(sys, 'frozen', True)
            setattr(sys, '_MEIPASS', Path(__file__))
            service = AppEnvironmentService()
            self.assertTrue(service.executing_directory.exists())
        finally:
            delattr(sys, 'frozen')
            delattr(sys, '_MEIPASS')

    def test_executing_directory_non_distributable(self, *_):
        try:
            setattr(sys, 'frozen', False)
            service = AppEnvironmentService()
            self.assertTrue(service.executing_directory.exists())
        finally:
            delattr(sys, 'frozen')

    @patch(f'{MODULE}.Path.is_file', return_value=True)
    def test_portable(self, *_):
        service = AppEnvironmentService()
        self.assertTrue(service.is_portable)

    @patch(f'{MODULE}.Path.is_file', return_value=False)
    def test_non_portable(self, *_):
        service = AppEnvironmentService()
        self.assertFalse(service.is_portable)