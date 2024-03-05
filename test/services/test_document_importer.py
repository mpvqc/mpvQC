# mpvQC
#
# Copyright (C) 2024
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
from unittest.mock import MagicMock, patch

import inject

from mpvqc.services import ReverseTranslatorService, DocumentImporterService

DOCUMENT_1 = '''\
erroneous_document
'''

DOCUMENT_2 = '''\
[FILE]
nick: some-weird-nick
path: /home/luffy/Videos/an existing video with spaces.mp4

[DATA]
[00:00:01][CommentType] Document 2 / Comment 1
[00:02:00][CommentType] Document 2 / Comment 2
[03:00:00][CommentType] Document 2 / Comment 3
'''

DOCUMENT_3 = '''\
[FILE]
nick: some-weird-nick
path       :                 C:\\Videos\\mpvQC\\an existing video with spaces on Windows.mp4

[DATA]
[00:00:11][A SPECIAL Comment-_-Type] Document 3 / Comment 1
[00:22:00][YOOOOO-comment-type] Document 3 / Comment 2
[33:00:00][ניסוח] Document 3 / Comment 3
'''

DOCUMENT_4 = '''\
[FILE]
nick: some-weird-nick
path       :                 /home/luffy/Videos/a not existing video with spaces.mp4

[DATA]
[00:00:11][A SPECIAL Comment-_-Type] Document 3 / Comment 1
[00:22:00][YOOOOO-comment-type] Document 3 / Comment 2
[00:00:00][ניסוח] Document 3 / Comment 3
[33:00:00][ניסוח] Document 3 / Comment 4
'''


class DocumentImporterServiceTest(unittest.TestCase):
    MODULE = 'mpvqc.services.document_importer'

    _service = DocumentImporterService()

    def setUp(self):
        inject.clear_and_configure(lambda binder: binder
                                   .bind(ReverseTranslatorService, ReverseTranslatorService()))

    def tearDown(self):
        inject.clear()

    @staticmethod
    def _mock(name, and_return_content):
        p = MagicMock()
        p.mpvqc_name = name
        p.read_text.return_value = and_return_content
        return p

    @staticmethod
    def _mocked_is_file_function(path: MagicMock):
        file_path = path.call_args[0][0]
        return 'an existing video' in file_path

    def test_import_document_1(self):
        p1 = self._mock('path-1', and_return_content=DOCUMENT_1)
        p2 = self._mock('path-2', and_return_content=DOCUMENT_1)
        result = self._service.read([p1, p2])

        self.assertFalse(result.valid_documents)
        self.assertTrue(result.invalid_documents)

        self.assertEqual('path-1', getattr(result.invalid_documents[0], 'mpvqc_name'))
        self.assertEqual('path-2', getattr(result.invalid_documents[1], 'mpvqc_name'))

    @patch(f'{MODULE}.Path')
    def test_import_document_2(self, path):
        path.return_value.is_file.side_effect = lambda: self._mocked_is_file_function(path)

        p1 = self._mock('path-1', and_return_content=DOCUMENT_2)

        result = self._service.read([p1])
        self.assertFalse(result.invalid_documents)
        self.assertTrue(result.valid_documents)
        self.assertTrue(result.videos)
        self.assertEqual('/home/luffy/Videos/an existing video with spaces.mp4', path.call_args[0][0])
        self.assertEqual(3, len(result.comments))

        comment = result.comments[0]
        self.assertEqual(1, comment.time)
        self.assertEqual('CommentType', comment.comment_type)
        self.assertEqual('Document 2 / Comment 1', comment.comment)

        comment = result.comments[1]
        self.assertEqual(120, comment.time)
        self.assertEqual('CommentType', comment.comment_type)
        self.assertEqual('Document 2 / Comment 2', comment.comment)

        comment = result.comments[2]
        self.assertEqual(10800, comment.time)
        self.assertEqual('CommentType', comment.comment_type)
        self.assertEqual('Document 2 / Comment 3', comment.comment)

    @patch(f'{MODULE}.Path')
    def test_import_document_3(self, path):
        path.return_value.is_file.side_effect = lambda: self._mocked_is_file_function(path)

        p1 = self._mock('path-1', and_return_content=DOCUMENT_3)

        result = self._service.read([p1])
        self.assertFalse(result.invalid_documents)
        self.assertTrue(result.valid_documents)
        self.assertTrue(result.videos)
        self.assertEqual('C:\\Videos\\mpvQC\\an existing video with spaces on Windows.mp4', path.call_args[0][0])
        self.assertEqual(3, len(result.comments))

        comment = result.comments[0]
        self.assertEqual(11, comment.time)
        self.assertEqual('A SPECIAL Comment-_-Type', comment.comment_type)
        self.assertEqual('Document 3 / Comment 1', comment.comment)

        comment = result.comments[1]
        self.assertEqual(1320, comment.time)
        self.assertEqual('YOOOOO-comment-type', comment.comment_type)
        self.assertEqual('Document 3 / Comment 2', comment.comment)

        comment = result.comments[2]
        self.assertEqual(118800, comment.time)
        self.assertEqual('Phrasing', comment.comment_type)
        self.assertEqual('Document 3 / Comment 3', comment.comment)

    @patch(f'{MODULE}.Path')
    def test_import_document_4(self, path):
        path.return_value.is_file.side_effect = lambda: self._mocked_is_file_function(path)

        p1 = self._mock('path-1', and_return_content=DOCUMENT_4)

        result = self._service.read([p1])
        self.assertFalse(result.invalid_documents)
        self.assertTrue(result.valid_documents)
        self.assertFalse(result.videos)
        self.assertEqual('/home/luffy/Videos/a not existing video with spaces.mp4', path.call_args[0][0])
        self.assertEqual(4, len(result.comments))

    @patch(f'{MODULE}.Path')
    def test_import_multiple_documents(self, path):
        path.return_value.is_file.side_effect = lambda: self._mocked_is_file_function(path)

        p1 = self._mock('path-1', and_return_content=DOCUMENT_1)
        p2 = self._mock('path-2', and_return_content=DOCUMENT_2)
        p3 = self._mock('path-3', and_return_content=DOCUMENT_3)
        p4 = self._mock('path-4', and_return_content=DOCUMENT_4)

        result = self._service.read([p1, p2, p3, p4])

        self.assertEqual(1, len(result.invalid_documents))
        self.assertEqual('path-1', getattr(result.invalid_documents[0], 'mpvqc_name'))
        self.assertEqual(3, len(result.valid_documents))
        self.assertEqual(2, len(result.videos))
        self.assertEqual(10, len(result.comments))
