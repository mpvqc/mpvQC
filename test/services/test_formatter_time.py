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

from parameterized import parameterized

from mpvqc.services import TimeFormatterService


class TimeFormatterServiceTest(unittest.TestCase):
    _service = TimeFormatterService()

    @parameterized.expand([
        ('00:00:00', 0),
        ('00:01:08', 68),
        ('00:16:39', 999),
        ('02:46:40', 10000),
    ])
    def test_format_time_to_string_long(self, expected, input_seconds):
        actual = self._service.format_time_to_string(input_seconds, long_format=True)
        self.assertEqual(expected, actual)

    @parameterized.expand([
        ('00:00', 0),
        ('01:08', 68),
        ('16:39', 999),
    ])
    def test_format_time_to_string_short(self, expected, input_seconds):
        actual = self._service.format_time_to_string(input_seconds, long_format=False)
        self.assertEqual(expected, actual)
