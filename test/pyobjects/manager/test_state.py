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

from pathlib import Path

import inject
import pytest

from mpvqc.pyobjects.manager.state import ApplicationState, ImportChange, InitialState, OtherState
from mpvqc.services import TypeMapperService


@pytest.fixture(autouse=True)
def setup_inject(type_mapper):
    def config(binder: inject.Binder):
        binder.bind(TypeMapperService, type_mapper)

    inject.configure(config, clear=True)


def test_import_change():
    change = ImportChange(documents=[], video=None)
    assert not change.only_video_imported
    assert not change.exactly_one_document_imported

    change = ImportChange(documents=[Path.home()], video=None)
    assert not change.only_video_imported
    assert change.exactly_one_document_imported
    assert Path.home() == change.imported_document

    change = ImportChange(documents=[Path.home(), Path.home().joinpath("other")], video=None)
    assert not change.only_video_imported
    assert not change.exactly_one_document_imported

    change = ImportChange(documents=[], video=Path.home())
    assert change.only_video_imported
    assert not change.exactly_one_document_imported

    change = ImportChange(documents=[Path.home()], video=Path.home())
    assert not change.only_video_imported
    assert change.exactly_one_document_imported

    change = ImportChange(documents=[Path.home(), Path.home().joinpath("other")], video=Path.home())
    assert not change.only_video_imported
    assert not change.exactly_one_document_imported


def test_find_video():
    state = ApplicationState(document=None, video=None, saved=True)
    imported_video = None
    change = ImportChange(documents=[], video=imported_video)
    assert state.find_video(change=change) is None

    state = ApplicationState(document=None, video=None, saved=True)
    imported_video = Path.home()
    change = ImportChange(documents=[], video=imported_video)
    assert imported_video == state.find_video(change)

    existing_video = Path.home() / "existing"
    state = ApplicationState(document=None, video=existing_video, saved=True)
    imported_video = None
    change = ImportChange(documents=[], video=imported_video)
    assert existing_video == state.find_video(change)

    existing_video = Path.home() / "existing"
    state = ApplicationState(document=None, video=existing_video, saved=True)
    imported_video = Path.home()
    change = ImportChange(documents=[], video=imported_video)
    assert imported_video == state.find_video(change)


def test_handle_save():
    state = ApplicationState(document=None, video=None, saved=True)
    new_document = Path.home() / "document"
    state = state.handle_save(document=new_document)
    assert new_document == state.document
    assert state.saved

    video = Path.home() / "video"
    document = Path.home() / "document"
    state = ApplicationState(document=document, video=video, saved=False)
    new_document = Path.home() / "new-document"
    state = state.handle_save(document=new_document)
    assert new_document == state.document
    assert video == state.video
    assert state.saved


def test_handle_change():
    state = ApplicationState(document=None, video=None, saved=True)
    state = state.handle_change()
    assert not state.saved

    video = Path.home() / "video"
    document = Path.home() / "document"
    state = ApplicationState(document=document, video=video, saved=False)
    state = state.handle_change()
    assert document == state.document
    assert video == state.video
    assert not state.saved


def test_handle_reset():
    state = ApplicationState(document=None, video=None, saved=True)
    state = state.handle_reset()
    assert state.saved
    assert state.video is None
    assert state.document is None

    video = Path.home() / "video"
    document = Path.home() / "document"
    state = ApplicationState(document=document, video=video, saved=False)
    state = state.handle_reset()
    assert state.saved
    assert video == state.video
    assert state.document is None


def test_initial_state():
    state = InitialState.new()
    assert state.video is None
    assert state.document is None
    assert state.saved

    video = Path.home()
    state = InitialState.new(video=video)
    assert video == state.video
    assert state.document is None
    assert state.saved


def test_handle_import_from_initial_state():
    state = InitialState.new()
    imported_video = Path.home()
    change = ImportChange(documents=[], video=imported_video)
    state = state.handle_import(change)
    assert isinstance(state, InitialState)
    assert imported_video == state.video

    initial_video = Path.home()
    state = InitialState.new(video=initial_video)
    imported_video = Path.home() / "imported-video"
    change = ImportChange(documents=[], video=imported_video)
    state = state.handle_import(change)
    assert isinstance(state, InitialState)
    assert imported_video == state.video

    initial_video = Path.home()
    state = InitialState.new(video=initial_video)
    imported_video = Path.home() / "imported-video"
    imported_document = Path.home() / "imported-document"
    change = ImportChange(documents=[imported_document], video=imported_video)
    state = state.handle_import(change)
    assert imported_video == state.video
    assert imported_document == state.document
    assert state.saved

    initial_video = Path.home()
    state = InitialState.new(video=initial_video)
    imported_video = None
    imported_document_1 = Path.home() / "imported-document-1"
    imported_document_2 = Path.home() / "imported-document-2"
    change = ImportChange(documents=[imported_document_1, imported_document_2], video=imported_video)
    state = state.handle_import(change)
    assert initial_video == state.video
    assert state.document is None
    assert not state.saved


def test_handle_import_from_other_state():
    initial_document = None
    initial_video = Path.home() / "video"
    initial_saved = True
    state = OtherState(initial_document, initial_video, initial_saved)
    imported_video = Path.home() / "video"
    imported_documents = []
    change = ImportChange(documents=imported_documents, video=imported_video)
    state = state.handle_import(change)
    assert state.document is None
    assert initial_saved == state.saved
    assert imported_video == state.video

    initial_document = Path.home() / "document"
    initial_video = Path.home() / "video"
    initial_saved = False
    state = OtherState(initial_document, initial_video, initial_saved)
    imported_video = Path.home() / "video"
    imported_documents = []
    change = ImportChange(documents=imported_documents, video=imported_video)
    state = state.handle_import(change)
    assert initial_document is state.document
    assert initial_saved == state.saved
    assert imported_video == state.video

    initial_document = Path.home() / "document"
    initial_video = Path.home() / "video-initial"
    initial_saved = True
    state = OtherState(initial_document, initial_video, initial_saved)
    imported_video = Path.home() / "video-imported"
    imported_documents = []
    change = ImportChange(documents=imported_documents, video=imported_video)
    state = state.handle_import(change)
    assert state.document is None
    assert not state.saved
    assert imported_video == state.video

    initial_document = Path.home() / "document"
    initial_video = Path.home() / "video-1"
    initial_saved = True
    state = OtherState(initial_document, initial_video, initial_saved)
    imported_video = Path.home() / "video-2"
    imported_document = Path.home() / "imported-document"
    change = ImportChange(documents=[imported_document], video=imported_video)
    state = state.handle_import(change)
    assert state.document is None
    assert not state.saved
    assert imported_video == state.video
