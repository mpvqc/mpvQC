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

from mpvqc.services import OsService, SupportedSystems


class TestOsService(unittest.TestCase):

    def test_is_linux(self):
        platform = SupportedSystems.LINUX
        os = OsService(platform.value)

        self.assertTrue(os.is_linux)
        self.assertFalse(os.is_not_linux)

    def test_is_not_linux(self):
        platform = SupportedSystems.LINUX
        os = OsService(platform.value)

        self.assertFalse(os.is_windows)
        self.assertFalse(os.is_mac)

    def test_is_windows(self):
        platform = SupportedSystems.WINDOWS
        os = OsService(platform.value)

        self.assertTrue(os.is_windows)
        self.assertFalse(os.is_not_windows)

    def test_is_not_windows(self):
        platform = SupportedSystems.WINDOWS
        os = OsService(platform.value)

        self.assertFalse(os.is_linux)
        self.assertFalse(os.is_mac)

    def test_is_mac(self):
        platform = SupportedSystems.MAC
        os = OsService(platform.value)

        self.assertTrue(os.is_mac)
        self.assertFalse(os.is_not_mac)

    def test_is_not_mac(self):
        platform = SupportedSystems.MAC
        os = OsService(platform.value)

        self.assertFalse(os.is_linux)
        self.assertFalse(os.is_windows)
