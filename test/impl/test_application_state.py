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

import inject

from mpvqc.impl import ImportChange, InitialState
from mpvqc.impl.application_state import ApplicationState, OtherState
from mpvqc.services import TypeMapperService


class ImportChangeTest(unittest.TestCase):
    """"""

    def test_import_change(self):
        change = ImportChange(documents=[], video=None)
        self.assertFalse(change.only_video_imported)
        self.assertFalse(change.exactly_one_document_imported)

        change = ImportChange(documents=[Path.home()], video=None)
        self.assertFalse(change.only_video_imported)
        self.assertTrue(change.exactly_one_document_imported)
        self.assertEqual(Path.home(), change.imported_document)

        change = ImportChange(documents=[Path.home(), Path.home().joinpath("other")], video=None)
        self.assertFalse(change.only_video_imported)
        self.assertFalse(change.exactly_one_document_imported)

        change = ImportChange(documents=[], video=Path.home())
        self.assertTrue(change.only_video_imported)
        self.assertFalse(change.exactly_one_document_imported)

        change = ImportChange(documents=[Path.home()], video=Path.home())
        self.assertFalse(change.only_video_imported)
        self.assertTrue(change.exactly_one_document_imported)

        change = ImportChange(documents=[Path.home(), Path.home().joinpath("other")], video=Path.home())
        self.assertFalse(change.only_video_imported)
        self.assertFalse(change.exactly_one_document_imported)


class ApplicationStateTest(unittest.TestCase):
    """"""

    def test_find_video(self):
        state = ApplicationState(document=None, video=None, saved=True)
        imported_video = None
        change = ImportChange(documents=[], video=imported_video)
        self.assertIsNone(state.find_video(change=change))

        state = ApplicationState(document=None, video=None, saved=True)
        imported_video = Path.home()
        change = ImportChange(documents=[], video=imported_video)
        self.assertEqual(imported_video, state.find_video(change))

        existing_video = Path.home() / "existing"
        state = ApplicationState(document=None, video=existing_video, saved=True)
        imported_video = None
        change = ImportChange(documents=[], video=imported_video)
        self.assertEqual(existing_video, state.find_video(change))

        existing_video = Path.home() / "existing"
        state = ApplicationState(document=None, video=existing_video, saved=True)
        imported_video = Path.home()
        change = ImportChange(documents=[], video=imported_video)
        self.assertEqual(imported_video, state.find_video(change))

    def test_handle_save(self):
        state = ApplicationState(document=None, video=None, saved=True)
        new_document = Path.home() / "document"
        state = state.handle_save(document=new_document)
        self.assertEqual(new_document, state.document)
        self.assertTrue(state.saved)

        video = Path.home() / "video"
        document = Path.home() / "document"
        state = ApplicationState(document=document, video=video, saved=False)
        new_document = Path.home() / "new-document"
        state = state.handle_save(document=new_document)
        self.assertEqual(new_document, state.document)
        self.assertEqual(video, state.video)
        self.assertTrue(state.saved)

    def test_handle_change(self):
        state = ApplicationState(document=None, video=None, saved=True)
        state = state.handle_change()
        self.assertFalse(state.saved)

        video = Path.home() / "video"
        document = Path.home() / "document"
        state = ApplicationState(document=document, video=video, saved=False)
        state = state.handle_change()
        self.assertEqual(document, state.document)
        self.assertEqual(video, state.video)
        self.assertFalse(state.saved)

    def test_handle_reset(self):
        state = ApplicationState(document=None, video=None, saved=True)
        state = state.handle_reset()
        self.assertTrue(state.saved)
        self.assertIsNone(state.video)
        self.assertIsNone(state.document)

        video = Path.home() / "video"
        document = Path.home() / "document"
        state = ApplicationState(document=document, video=video, saved=False)
        state = state.handle_reset()
        self.assertTrue(state.saved)
        self.assertEqual(video, state.video)
        self.assertIsNone(state.document)


class InitialStateTest(unittest.TestCase):
    """"""

    def test_initial_state(self):
        state = InitialState.new()
        self.assertIsNone(state.video)
        self.assertIsNone(state.document)
        self.assertTrue(state.saved)

        video = Path.home()
        state = InitialState.new(video=video)
        self.assertEqual(video, state.video)
        self.assertIsNone(state.document)
        self.assertTrue(state.saved)

    def test_handle_import(self):
        state = InitialState.new()
        imported_video = Path.home()
        change = ImportChange(documents=[], video=imported_video)
        state = state.handle_import(change)
        self.assertIsInstance(state, InitialState)
        self.assertEqual(imported_video, state.video)

        initial_video = Path.home()
        state = InitialState.new(video=initial_video)
        imported_video = Path.home() / "imported-video"
        change = ImportChange(documents=[], video=imported_video)
        state = state.handle_import(change)
        self.assertIsInstance(state, InitialState)
        self.assertEqual(imported_video, state.video)

        initial_video = Path.home()
        state = InitialState.new(video=initial_video)
        imported_video = Path.home() / "imported-video"
        imported_document = Path.home() / "imported-document"
        change = ImportChange(documents=[imported_document], video=imported_video)
        state = state.handle_import(change)
        self.assertEqual(imported_video, state.video)
        self.assertEqual(imported_document, state.document)
        self.assertTrue(state.saved)

        initial_video = Path.home()
        state = InitialState.new(video=initial_video)
        imported_video = None
        imported_document_1 = Path.home() / "imported-document-1"
        imported_document_2 = Path.home() / "imported-document-2"
        change = ImportChange(documents=[imported_document_1, imported_document_2], video=imported_video)
        state = state.handle_import(change)
        self.assertEqual(initial_video, state.video)
        self.assertIsNone(state.document)
        self.assertFalse(state.saved)


class OtherStateTest(unittest.TestCase):
    """"""

    def setUp(self):
        # fmt: off
        inject.clear_and_configure(lambda binder: binder
                                   .bind(TypeMapperService, TypeMapperService()))
        # fmt: on

    def tearDown(self):
        inject.clear()

    def test_handle_import(self):
        initial_document = None
        initial_video = Path.home() / "video"
        initial_saved = True
        state = OtherState(initial_document, initial_video, initial_saved)
        imported_video = Path.home() / "video"
        imported_documents = []
        change = ImportChange(documents=imported_documents, video=imported_video)
        state = state.handle_import(change)
        self.assertIsNone(state.document)
        self.assertEqual(initial_saved, state.saved)
        self.assertEqual(imported_video, state.video)

        initial_document = Path.home() / "document"
        initial_video = Path.home() / "video"
        initial_saved = False
        state = OtherState(initial_document, initial_video, initial_saved)
        imported_video = Path.home() / "video"
        imported_documents = []
        change = ImportChange(documents=imported_documents, video=imported_video)
        state = state.handle_import(change)
        self.assertEqual(initial_document, state.document)
        self.assertEqual(initial_saved, state.saved)
        self.assertEqual(imported_video, state.video)

        initial_document = Path.home() / "document"
        initial_video = Path.home() / "video-initial"
        initial_saved = True
        state = OtherState(initial_document, initial_video, initial_saved)
        imported_video = Path.home() / "video-imported"
        imported_documents = []
        change = ImportChange(documents=imported_documents, video=imported_video)
        state = state.handle_import(change)
        self.assertIsNone(state.document)
        self.assertFalse(state.saved)
        self.assertEqual(imported_video, state.video)

        initial_document = Path.home() / "document"
        initial_video = Path.home() / "video-1"
        initial_saved = True
        state = OtherState(initial_document, initial_video, initial_saved)
        imported_video = Path.home() / "video-2"
        imported_document = Path.home() / "imported-document"
        change = ImportChange(documents=[imported_document], video=imported_video)
        state = state.handle_import(change)
        self.assertIsNone(state.document)
        self.assertFalse(state.saved)
        self.assertEqual(imported_video, state.video)
