# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from typing import NamedTuple

import inject
import pytest

from mpvqc.services import TypeMapperService
from mpvqc.services.state import (
    CHANGE_ACTION,
    RESET_ACTION,
    ApplicationState,
    ImportAction,
    ImportChange,
    SaveAction,
    reduce,
)


@pytest.fixture(autouse=True)
def setup_inject(type_mapper):
    def config(binder: inject.Binder):
        binder.bind(TypeMapperService, type_mapper)

    inject.configure(config, clear=True)


def initial_state(video: Path | None = None) -> ApplicationState:
    return ApplicationState(None, video, True)


class ImportChangeTestCase(NamedTuple):
    name: str
    documents: list[Path]
    video: Path | None
    expected_only_video: bool
    expected_exactly_one_doc: bool


IMPORT_CHANGE_TEST_CASES = [
    ImportChangeTestCase(
        name="no documents, no video",
        documents=[],
        video=None,
        expected_only_video=False,
        expected_exactly_one_doc=False,
    ),
    ImportChangeTestCase(
        name="one document, no video",
        documents=[Path("document")],
        video=None,
        expected_only_video=False,
        expected_exactly_one_doc=True,
    ),
    ImportChangeTestCase(
        name="multiple documents, no video",
        documents=[Path("document1"), Path("document2")],
        video=None,
        expected_only_video=False,
        expected_exactly_one_doc=False,
    ),
    ImportChangeTestCase(
        name="no documents, with video",
        documents=[],
        video=Path("video"),
        expected_only_video=True,
        expected_exactly_one_doc=False,
    ),
    ImportChangeTestCase(
        name="one document, with video",
        documents=[Path("document")],
        video=Path("video"),
        expected_only_video=False,
        expected_exactly_one_doc=True,
    ),
    ImportChangeTestCase(
        name="multiple documents, with video",
        documents=[Path("document1"), Path("document2")],
        video=Path("video"),
        expected_only_video=False,
        expected_exactly_one_doc=False,
    ),
]


@pytest.mark.parametrize("case", IMPORT_CHANGE_TEST_CASES, ids=lambda case: case.name)
def test_import_change(case: ImportChangeTestCase) -> None:
    change = ImportChange(documents=case.documents, video=case.video)
    assert change.only_video_imported == case.expected_only_video
    assert change.exactly_one_document_imported == case.expected_exactly_one_doc

    if case.expected_exactly_one_doc:
        assert change.imported_document == case.documents[0]


class SaveActionTestCase(NamedTuple):
    name: str
    initial_document: Path | None
    initial_video: Path | None
    initial_saved: bool
    save_document: Path
    expected_video: Path | None
    expected_saved: bool


SAVE_ACTION_TEST_CASES = [
    SaveActionTestCase(
        name="save to initial state with no video",
        initial_document=None,
        initial_video=None,
        initial_saved=True,
        save_document=Path("document"),
        expected_video=None,
        expected_saved=True,
    ),
    SaveActionTestCase(
        name="save with existing video and document",
        initial_document=Path("document"),
        initial_video=Path("video"),
        initial_saved=False,
        save_document=Path("new-document"),
        expected_video=Path("video"),
        expected_saved=True,
    ),
]


@pytest.mark.parametrize("case", SAVE_ACTION_TEST_CASES, ids=lambda case: case.name)
def test_reduce_save_action(case: SaveActionTestCase) -> None:
    state = ApplicationState(case.initial_document, case.initial_video, case.initial_saved)
    state = reduce(state, SaveAction(case.save_document))
    assert case.save_document == state.document
    assert case.expected_video == state.video
    assert case.expected_saved == state.saved


class ChangeActionTestCase(NamedTuple):
    name: str
    initial_document: Path | None
    initial_video: Path | None
    initial_saved: bool
    expected_document: Path | None
    expected_video: Path | None


CHANGE_ACTION_TEST_CASES = [
    ChangeActionTestCase(
        name="change from initial state",
        initial_document=None,
        initial_video=None,
        initial_saved=True,
        expected_document=None,
        expected_video=None,
    ),
    ChangeActionTestCase(
        name="change with existing video and document",
        initial_document=Path("document"),
        initial_video=Path("video"),
        initial_saved=False,
        expected_document=Path("document"),
        expected_video=Path("video"),
    ),
]


@pytest.mark.parametrize("case", CHANGE_ACTION_TEST_CASES, ids=lambda case: case.name)
def test_reduce_change_action(case: ChangeActionTestCase) -> None:
    state = ApplicationState(case.initial_document, case.initial_video, case.initial_saved)
    state = reduce(state, CHANGE_ACTION)
    assert case.expected_document == state.document
    assert case.expected_video == state.video
    assert not state.saved


class ResetActionTestCase(NamedTuple):
    name: str
    initial_document: Path | None
    initial_video: Path | None
    initial_saved: bool
    expected_video: Path | None


RESET_ACTION_TEST_CASES = [
    ResetActionTestCase(
        name="reset from initial state",
        initial_document=None,
        initial_video=None,
        initial_saved=True,
        expected_video=None,
    ),
    ResetActionTestCase(
        name="reset with existing video and document",
        initial_document=Path("document"),
        initial_video=Path("video"),
        initial_saved=False,
        expected_video=Path("video"),
    ),
]


@pytest.mark.parametrize("case", RESET_ACTION_TEST_CASES, ids=lambda case: case.name)
def test_reduce_reset_action(case: ResetActionTestCase) -> None:
    state = ApplicationState(case.initial_document, case.initial_video, case.initial_saved)
    state = reduce(state, RESET_ACTION)
    assert state.saved
    assert case.expected_video == state.video
    assert state.document is None


class ImportActionTestCase(NamedTuple):
    name: str
    initial_document: Path | None
    initial_video: Path | None
    initial_saved: bool
    import_documents: list[Path]
    import_video: Path | None
    expected_document: Path | None
    expected_video: Path | None
    expected_saved: bool


IMPORT_ACTION_TEST_CASES = [
    ImportActionTestCase(
        name="from initial state: import video only",
        initial_document=None,
        initial_video=None,
        initial_saved=True,
        import_documents=[],
        import_video=Path("video"),
        expected_document=None,
        expected_video=Path("video"),
        expected_saved=True,
    ),
    ImportActionTestCase(
        name="from initial state: import different video",
        initial_document=None,
        initial_video=Path("video-initial"),
        initial_saved=True,
        import_documents=[],
        import_video=Path("video-imported"),
        expected_document=None,
        expected_video=Path("video-imported"),
        expected_saved=True,
    ),
    ImportActionTestCase(
        name="from initial state: import one document with video",
        initial_document=None,
        initial_video=Path("video-initial"),
        initial_saved=True,
        import_documents=[Path("document")],
        import_video=Path("video-imported"),
        expected_document=Path("document"),
        expected_video=Path("video-imported"),
        expected_saved=True,
    ),
    ImportActionTestCase(
        name="from initial state: import multiple documents without video",
        initial_document=None,
        initial_video=Path("video-initial"),
        initial_saved=True,
        import_documents=[Path("document1"), Path("document2")],
        import_video=None,
        expected_document=None,
        expected_video=Path("video-initial"),
        expected_saved=False,
    ),
    ImportActionTestCase(
        name="from other state: import same video, no document, should preserve state",
        initial_document=None,
        initial_video=Path("video"),
        initial_saved=True,
        import_documents=[],
        import_video=Path("video"),
        expected_document=None,
        expected_video=Path("video"),
        expected_saved=True,
    ),
    ImportActionTestCase(
        name="from other state: import same video with document, should preserve document and saved state",
        initial_document=Path("document"),
        initial_video=Path("video"),
        initial_saved=False,
        import_documents=[],
        import_video=Path("video"),
        expected_document=Path("document"),
        expected_video=Path("video"),
        expected_saved=False,
    ),
    ImportActionTestCase(
        name="from other state: import different video, should reset",
        initial_document=Path("document"),
        initial_video=Path("video-initial"),
        initial_saved=True,
        import_documents=[],
        import_video=Path("video-imported"),
        expected_document=None,
        expected_video=Path("video-imported"),
        expected_saved=False,
    ),
    ImportActionTestCase(
        name="from other state: import document with different video, should reset",
        initial_document=Path("document"),
        initial_video=Path("video-1"),
        initial_saved=True,
        import_documents=[Path("imported-document")],
        import_video=Path("video-2"),
        expected_document=None,
        expected_video=Path("video-2"),
        expected_saved=False,
    ),
]


@pytest.mark.parametrize("case", IMPORT_ACTION_TEST_CASES, ids=lambda case: case.name)
def test_reduce_import_action(case: ImportActionTestCase) -> None:
    state = ApplicationState(case.initial_document, case.initial_video, case.initial_saved)
    change = ImportChange(documents=case.import_documents, video=case.import_video)
    state = reduce(state, ImportAction(change))
    assert case.expected_document == state.document
    assert case.expected_video == state.video
    assert case.expected_saved == state.saved
