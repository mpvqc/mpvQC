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


class ResourceServiceTest(unittest.TestCase):

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

    def test_default_export_template(self):
        template = ResourceService().default_export_template
        self.assertTrue(template)

        # contains all mpvQC expressions
        required_arguments = [
            "write_date", "date",
            "write_generator", "generator",
            "write_nickname", "nickname",
            "write_video_path", "video_path",
            "comments",
            "comment['time'] | as_time",
            "comment['commentType'] | as_comment_type",
            "comment['comment'] | trim",
        ]
        for arg in required_arguments:
            self.assertIn(arg, template, f"Expected to find mpvQC expression '{arg}' in export template")

        # ends with '\n'
        self.assertEqual('\n', template[-1])
