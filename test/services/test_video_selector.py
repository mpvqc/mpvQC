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
from pathlib import Path
from unittest.mock import MagicMock

import inject
from parameterized import parameterized

from mpvqc.services import SettingsService, VideoSelectorService
from test.mocks import MockedMessageBox


class VideoSelectorServiceTest(unittest.TestCase):
    _existing_1 = Path.home() / 'Videos' / 'some-existing-video-1.mp4'
    _existing_2 = Path.home() / 'Videos' / 'some-existing-video-2.mp4'
    _existing_3 = Path.home() / 'Videos' / 'some-existing-video-3.mp4'

    _service = VideoSelectorService()
    _result = Path or None

    @staticmethod
    def mock_user_choice(choice: SettingsService.ImportWhenVideoLinkedInDocument):
        mock = MagicMock()
        mock.import_video_when_video_linked_in_document = choice
        inject.clear_and_configure(lambda binder: binder
                                   .bind(SettingsService, mock))

    def tearDown(self):
        inject.clear()
        self._reset()

    def _select_video_based_on(self, user_input):
        self._service.select_video_from(
            on_video_selected=self._pick_video,
            video_found_dialog_factory=MagicMock(),
            **user_input
        )

    def _pick_video(self, video: Path or None):
        self._result = video

    def _reset(self):
        self._result = None

    @parameterized.expand([
        ({
             'existing_videos_dropped': [_existing_1],
             'existing_videos_from_documents': [],
         }, _existing_1),
        ({
             'existing_videos_dropped': [_existing_2, _existing_3, _existing_1],
             'existing_videos_from_documents': [],
         }, _existing_2),
    ])
    def test_existing_video_dropped_n(self, user_input, expected):
        self._select_video_based_on(user_input)
        self.assertEqual(expected, self._result)

    @parameterized.expand([
        ({
             'existing_videos_dropped': [_existing_1],
             'existing_videos_from_documents': [_existing_2],
         }, _existing_1),
        ({
             'existing_videos_dropped': [],
             'existing_videos_from_documents': [],
         }, None),
        ({
             'existing_videos_dropped': [],
             'existing_videos_from_documents': [_existing_2],
         }, None),
    ])
    def test_user_never_wants_to_import_video(self, user_input, expected):
        self.mock_user_choice(SettingsService.ImportWhenVideoLinkedInDocument.NEVER)

        self._select_video_based_on(user_input)
        self.assertEqual(expected, self._result)

    @parameterized.expand([
        ({
             'existing_videos_dropped': [_existing_1],
             'existing_videos_from_documents': [],
         }, _existing_1),
        ({
             'existing_videos_dropped': [],
             'existing_videos_from_documents': [],
         }, None),
    ])
    def test_no_videos_found_in_document(self, user_input, expected):
        self.mock_user_choice(SettingsService.ImportWhenVideoLinkedInDocument.ALWAYS)

        self._select_video_based_on(user_input)
        self.assertEqual(expected, self._result)

    @parameterized.expand([
        ({
             'existing_videos_dropped': [_existing_1],
             'existing_videos_from_documents': [_existing_2],
         }, _existing_1),
        ({
             'existing_videos_dropped': [],
             'existing_videos_from_documents': [_existing_3],
         }, _existing_3),
    ])
    def test_user_always_wants_to_import_video(self, user_input, expected):
        self.mock_user_choice(SettingsService.ImportWhenVideoLinkedInDocument.ALWAYS)

        self._select_video_based_on(user_input)
        self.assertEqual(expected, self._result)

    def test_user_will_be_asked(self):
        self.mock_user_choice(SettingsService.ImportWhenVideoLinkedInDocument.ASK_EVERY_TIME)

        user_input = {
            'existing_videos_dropped': [self._existing_1],
            'existing_videos_from_documents': [self._existing_2],
        }

        self._select_video_based_on(user_input)
        self.assertEqual(self._existing_1, self._result)
        self._reset()

        user_input = {
            'existing_videos_dropped': [],
            'existing_videos_from_documents': [self._existing_3],
        }

        user_selection = MagicMock()
        user_selection.createObject.return_value = MockedMessageBox()
        self._service.select_video_from(
            video_found_dialog_factory=user_selection,
            on_video_selected=self._pick_video,
            **user_input
        )
        user_selection.createObject.return_value.accepted.emit()
        self.assertEqual(self._existing_3, self._result)
        self._reset()

        self._service.select_video_from(
            video_found_dialog_factory=user_selection,
            on_video_selected=self._pick_video,
            **user_input
        )
        user_selection.createObject.return_value.rejected.emit()
        self.assertIsNone(self._result)
        self._reset()
