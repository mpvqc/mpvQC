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


import textwrap
import unittest

from mpvqc.impl import BuildInfoExtractor


class TestBuildVersionExtractor(unittest.TestCase):

    @staticmethod
    def _read(content: str) -> BuildInfoExtractor:
        extractor = BuildInfoExtractor()
        extractor.extract_from(textwrap.dedent(content))
        return extractor

    def test_extract_tag(self):
        expected_tag = 'v1.0.0'

        text = f'''\
                [build_info]
                tag={expected_tag}
                '''

        extractor = self._read(text)

        self.assertEqual(expected_tag, extractor.tag)

    def test_extract_commit(self):
        expected_commit = 'abcdefgh'

        text = f'''\
                [build_info]
                commit={expected_commit}
                '''

        extractor = self._read(text)

        self.assertEqual(expected_commit, extractor.commit_id)

    def test_extract_all(self):
        expected_tag = 'v1.0.0'
        expected_commit = 'abcdefgh'

        text = f'''\
                [build_info]
                tag={expected_tag}
                commit={expected_commit}
                '''

        extractor = self._read(text)

        self.assertEqual(expected_tag, extractor.tag)
        self.assertEqual(expected_commit, extractor.commit_id)
