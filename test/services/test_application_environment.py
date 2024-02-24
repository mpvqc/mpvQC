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

import os
import sys
import unittest
from pathlib import Path

from mpvqc.services import ApplicationEnvironmentService


class ApplicationEnvironmentServiceTest(unittest.TestCase):
    MODULE = 'mpvqc.services.application_environment'

    def test_built_by_pyinstaller(self):
        try:
            setattr(sys, 'frozen', True)
            setattr(sys, '_MEIPASS', Path(__file__))
            service = ApplicationEnvironmentService()
            self.assertTrue(service.executing_directory.exists())
        finally:
            delattr(sys, 'frozen')
            delattr(sys, '_MEIPASS')

        try:
            setattr(sys, 'frozen', False)
            service = ApplicationEnvironmentService()
            self.assertTrue(service.executing_directory.exists())
        finally:
            delattr(sys, 'frozen')

    def test_run_as_flatpak(self, *_):
        service = ApplicationEnvironmentService()
        self.assertFalse(service.runs_as_flatpak)

        os.environ['FLATPAK_ID'] = "MPVQC_ID"
        service = ApplicationEnvironmentService()
        self.assertTrue(service.runs_as_flatpak)
