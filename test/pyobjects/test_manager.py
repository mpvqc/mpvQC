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
from pathlib import Path
from unittest.mock import MagicMock, patch

import inject

from mpvqc.impl import OtherState
from mpvqc.pyobjects import MpvqcManagerPyObject
from mpvqc.services import (
    DocumentExportService,
    DocumentImporterService,
    PlayerService,
    TypeMapperService,
    VideoSelectorService,
)
from test.mocks import MockedDialog, MockedMessageBox


class ManagerResetTest(unittest.TestCase):
    """"""

    def init(self, q_app: MagicMock):
        # noinspection PyCallingNonCallable
        self._manager: MpvqcManagerPyObject = MpvqcManagerPyObject()

        self._mocked_message_box = MockedMessageBox()
        factory = MagicMock()
        factory.createObject.return_value = self._mocked_message_box
        self._manager.message_box_new_document_factory = factory

        self._mocked_comments_model = MagicMock()
        q_app.return_value.find_object.return_value = self._mocked_comments_model

    @patch("mpvqc.pyobjects.manager.QCoreApplication.instance", return_value=MagicMock())
    def test_saved_reset(self, q_app_mock):
        self.init(q_app_mock)

        state_before = self._manager.state
        self.assertTrue(state_before.saved)

        self._manager.reset_impl()

        state_after = self._manager.state
        self.assertTrue(state_after.saved)
        self.assertEqual(state_before, state_after)
        self._mocked_comments_model.clear_comments.assert_called_once()

    @patch("mpvqc.pyobjects.manager.QCoreApplication.instance", return_value=MagicMock())
    def test_unsaved_reset_do_reset(self, q_app_mock):
        self.init(q_app_mock)

        self._manager.state = OtherState(document=None, video=None, saved=False)
        self._manager.reset_impl()
        self._mocked_message_box.accepted.emit()

        self._mocked_comments_model.clear_comments.assert_called_once()

    @patch("mpvqc.pyobjects.manager.QCoreApplication.instance", return_value=MagicMock())
    def test_unsaved_reset_cancel_reset(self, q_app_mock):
        self.init(q_app_mock)

        self._manager.state = OtherState(document=None, video=None, saved=False)
        self._manager.reset_impl()
        self._mocked_message_box.rejected.emit()

        self.assertFalse(self._mocked_comments_model.clear_comments.called)


class ManagerSaveTest(unittest.TestCase):
    _type_mapper = TypeMapperService()

    def init(self):
        # noinspection PyCallingNonCallable
        self._manager: MpvqcManagerPyObject = MpvqcManagerPyObject()
        self._document = Path().home() / "Documents" / "my-doc.txt"

        self._mocked_dialog = MockedDialog()
        factory = MagicMock()
        factory.createObject.return_value = self._mocked_dialog
        self._manager.dialog_export_document_factory = factory

        self._exporter_mock = MagicMock()
        # fmt: off
        inject.clear_and_configure(lambda binder: binder
                                   .bind(DocumentExportService, self._exporter_mock))
        # fmt: on

    def tearDown(self):
        inject.clear()

    @patch("mpvqc.pyobjects.manager.QCoreApplication.instance", return_value=MagicMock())
    def test_saved_save(self, *_):
        self.init()

        self._manager.state = OtherState(document=None, video=None, saved=True)

        self._manager.save_impl()
        self.assertFalse(self._exporter_mock.save.called)

        self._manager.state = OtherState(document=self._document, video=None, saved=True)
        self._manager.save_impl()

        self._exporter_mock.save.assert_called_once()
        saved_path = self._exporter_mock.save.call_args[0][0]
        self.assertEqual(self._document, saved_path)

    @patch("mpvqc.pyobjects.manager.QCoreApplication.instance", return_value=MagicMock())
    def test_unsaved_save_do_save(self, *_):
        self.init()

        self._manager.state = OtherState(document=None, video=None, saved=True)
        self._manager.save_impl()

        self._mocked_dialog.savePressed.emit(self._type_mapper.map_path_to_url(self._document))

        self._exporter_mock.save.assert_called_once()
        saved_path = self._exporter_mock.save.call_args[0][0]
        self.assertEqual(self._document, saved_path)

        self.assertTrue(self._manager.state.saved)
        self.assertEqual(self._document, self._manager.state.document)

    @patch("mpvqc.pyobjects.manager.QCoreApplication.instance", return_value=MagicMock())
    def test_unsaved_save_cancel_save(self, *_):
        self.init()

        self._manager.state = OtherState(document=None, video=None, saved=False)
        self._manager.save_impl()

        self.assertFalse(self._exporter_mock.save.called)
        self.assertFalse(self._manager.state.saved)
        self.assertIsNone(self._manager.state.document)


class ManagerImportTest(unittest.TestCase):
    _type_mapper = TypeMapperService()

    _document = Path().home() / "Documents" / "my-doc.txt"
    _document_url = _type_mapper.map_path_to_url(_document)

    _video = Path().home() / "Video" / "my-video.mp4"
    _video_url = _type_mapper.map_path_to_url(_video)

    def init(
        self,
        q_app: MagicMock,
        *,
        import_result: DocumentImporterService.DocumentImportResult,
        pick_video: Path or None = None,
    ):
        # noinspection PyCallingNonCallable
        self._manager: MpvqcManagerPyObject = MpvqcManagerPyObject()

        # Mock message boxes
        self._mocked_message_box_document_not_compatible = MagicMock()
        factory = MagicMock()
        factory.createObject.return_value = self._mocked_message_box_document_not_compatible
        self._manager.message_box_document_not_compatible_factory = factory

        self._manager.message_box_video_found_factory = MagicMock()

        # Mock pyobjects
        self._mocked_comments_model = MagicMock()
        q_app.return_value.find_object.return_value = self._mocked_comments_model

        # Mock services
        self._video_selector_mock = MagicMock()

        def on_video_selected(*args, **kwargs):
            kwargs["on_video_selected"](pick_video)

        self._video_selector_mock.select_video_from.side_effect = on_video_selected

        self._importer_mock = MagicMock()
        self._importer_mock.read.return_value = import_result

        self._player_mock = MagicMock()

        # fmt: off
        inject.clear_and_configure(lambda binder: binder
                                   .bind(VideoSelectorService, self._video_selector_mock)
                                   .bind(DocumentImporterService, self._importer_mock)
                                   .bind(PlayerService, self._player_mock)
                                   .bind(TypeMapperService, TypeMapperService()))
        # fmt: on

    @patch("mpvqc.pyobjects.manager.QCoreApplication.instance", return_value=MagicMock())
    def test_import_document(self, q_app_mock):
        self.init(
            q_app_mock,
            pick_video=None,
            import_result=DocumentImporterService.DocumentImportResult(
                valid_documents=[self._document], invalid_documents=[], existing_videos=[], comments=[]
            ),
        )

        self._manager.state = OtherState(document=Path.home(), video=None, saved=True)
        self._manager.open_documents_impl([self._document_url])

        self._mocked_comments_model.import_comments.assert_called_once()
        self.assertFalse(self._manager.state.saved)
        self.assertIsNone(self._manager.state.document)

    @patch("mpvqc.pyobjects.manager.QCoreApplication.instance", return_value=MagicMock())
    def test_import_video(self, q_app_mock):
        self.init(
            q_app_mock,
            pick_video=self._video,
            import_result=DocumentImporterService.DocumentImportResult(
                valid_documents=[], invalid_documents=[], existing_videos=[], comments=[]
            ),
        )

        self._manager.state = OtherState(document=Path.home(), video=None, saved=True)
        self._manager.open_video_impl(self._video_url)

        self._player_mock.open_video.assert_called_once()
        self.assertFalse(self._manager.state.saved)
        self.assertIsNone(self._manager.state.document)
        self.assertEqual(self._video, self._manager.state.video)

    @patch("mpvqc.pyobjects.manager.QCoreApplication.instance", return_value=MagicMock())
    def test_import_subtitles(self, q_app_mock):
        self.init(
            q_app_mock,
            pick_video=None,
            import_result=DocumentImporterService.DocumentImportResult(
                valid_documents=[], invalid_documents=[], existing_videos=[], comments=[]
            ),
        )

        self._manager.open_subtitles_impl([self._document_url])

        self._player_mock.open_subtitles.assert_called_once()

    @patch("mpvqc.pyobjects.manager.QCoreApplication.instance", return_value=MagicMock())
    def test_import_multiple(self, q_app_mock):
        self.init(
            q_app_mock,
            pick_video=self._video,
            import_result=DocumentImporterService.DocumentImportResult(
                valid_documents=[self._document, self._document], invalid_documents=[], existing_videos=[], comments=[]
            ),
        )

        self._manager.open_impl(
            documents=[self._document_url, self._document_url], videos=[self._video_url], subtitles=[self._document_url]
        )

        self._mocked_comments_model.import_comments.assert_called_once()
        self._player_mock.open_video.assert_called_once()
        self._player_mock.open_subtitles.assert_called_once()

    @patch("mpvqc.pyobjects.manager.QCoreApplication.instance", return_value=MagicMock())
    def test_import_erroneous_documents(self, q_app_mock):
        self.init(
            q_app_mock,
            pick_video=self._video,
            import_result=DocumentImporterService.DocumentImportResult(
                valid_documents=[], invalid_documents=[self._document, self._document], existing_videos=[], comments=[]
            ),
        )

        self._manager.open_impl([self._document_url, self._document_url], [self._video_url], [])

        self._player_mock.open_video.assert_called_once()
        self._mocked_message_box_document_not_compatible.open.assert_called_once()
