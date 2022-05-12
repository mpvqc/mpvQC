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

import inject

from mpvqc.impl import ResourceFileReader
from mpvqc.services import ResourceService


class TestResourceService(unittest.TestCase):

    def setUp(self):
        inject.clear_and_configure(lambda binder: binder
                                   .bind(ResourceFileReader, ResourceFileReader()))

    def tearDown(self):
        inject.clear()

    def test_version_conf_content_contains_tag(self):
        text = ResourceService().build_info_conf_content
        self.assertIn('tag=', text)

    def test_version_conf_content_contains_commit(self):
        text = ResourceService().build_info_conf_content
        self.assertIn('commit=', text)

    def test_input_conf_exists(self):
        text = ResourceService().input_conf_content
        self.assertTrue(text)

    def test_mpv_conf_exists(self):
        text = ResourceService().mpv_conf_content
        self.assertTrue(text)
