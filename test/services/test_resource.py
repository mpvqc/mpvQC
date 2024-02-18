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

import inject

from mpvqc.services import ResourceService, ResourceReaderService


class TestResourceService(unittest.TestCase):

    def setUp(self):
        inject.clear_and_configure(lambda binder: binder
                                   .bind(ResourceReaderService, ResourceReaderService()))

    def tearDown(self):
        inject.clear()

    def test_input_conf_exists(self):
        text = ResourceService().input_conf_content
        self.assertTrue(text)

    def test_mpv_conf_exists(self):
        text = ResourceService().mpv_conf_content
        self.assertTrue(text)

    def test_mpvqc_export_template_exists(self):
        text = ResourceService().mpvqc_export_template_content
        self.assertTrue(text)
