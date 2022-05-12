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

from mpvqc.impl import BuildInfoExtractor
from mpvqc.services import ResourceService, BuildInfoService


class TestBuildInfoService(unittest.TestCase):

    def setUp(self):
        inject.clear_and_configure(lambda binder: binder
                                   .bind(ResourceService, ResourceService())
                                   .bind(BuildInfoExtractor, BuildInfoExtractor()))

    def tearDown(self):
        inject.clear()

    def test_tag(self):
        service = BuildInfoService()
        self.assertTrue(service.tag)

    def test_commit(self):
        service = BuildInfoService()
        self.assertTrue(service.commit)
