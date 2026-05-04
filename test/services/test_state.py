# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from typing import NamedTuple

import pytest

from mpvqc.services.state import (
    ApplicationState,
    ImportChange,
    StateService,
)


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with):
    common_bindings_with()


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
    change = ImportChange(documents=case.documents, video=case.video, video_from_subtitle=True)
    assert change.only_video_imported == case.expected_only_video
    assert change.exactly_one_document_imported == case.expected_exactly_one_doc

    if case.expected_exactly_one_doc:
        assert change.imported_document == case.documents[0]


class SaveTestCase(NamedTuple):
    name: str
    initial_document: Path | None
    initial_video: Path | None
    initial_saved: bool
    save_document: Path
    expected_video: Path | None
    expected_saved: bool


SAVE_TEST_CASES = [
    SaveTestCase(
        name="save to initial state with no video",
        initial_document=None,
        initial_video=None,
        initial_saved=True,
        save_document=Path("document"),
        expected_video=None,
        expected_saved=True,
    ),
    SaveTestCase(
        name="save with existing video and document",
        initial_document=Path("document"),
        initial_video=Path("video"),
        initial_saved=False,
        save_document=Path("new-document"),
        expected_video=Path("video"),
        expected_saved=True,
    ),
]


@pytest.mark.parametrize("case", SAVE_TEST_CASES, ids=lambda case: case.name)
def test_save(case: SaveTestCase) -> None:
    service = StateService()
    service._state = ApplicationState(case.initial_document, case.initial_video, case.initial_saved)

    service.save(case.save_document)

    assert case.save_document == service.document
    assert case.expected_video == service._state.video
    assert case.expected_saved == service.saved


class ChangeTestCase(NamedTuple):
    name: str
    initial_document: Path | None
    initial_video: Path | None
    initial_saved: bool
    expected_document: Path | None
    expected_video: Path | None


CHANGE_TEST_CASES = [
    ChangeTestCase(
        name="change from initial state",
        initial_document=None,
        initial_video=None,
        initial_saved=True,
        expected_document=None,
        expected_video=None,
    ),
    ChangeTestCase(
        name="change with existing video and document",
        initial_document=Path("document"),
        initial_video=Path("video"),
        initial_saved=False,
        expected_document=Path("document"),
        expected_video=Path("video"),
    ),
]


@pytest.mark.parametrize("case", CHANGE_TEST_CASES, ids=lambda case: case.name)
def test_change(case: ChangeTestCase) -> None:
    service = StateService()
    service._state = ApplicationState(case.initial_document, case.initial_video, case.initial_saved)

    service.change()

    assert case.expected_document == service.document
    assert case.expected_video == service._state.video
    assert not service.saved


class ResetTestCase(NamedTuple):
    name: str
    initial_document: Path | None
    initial_video: Path | None
    initial_saved: bool
    expected_video: Path | None


RESET_TEST_CASES = [
    ResetTestCase(
        name="reset from initial state",
        initial_document=None,
        initial_video=None,
        initial_saved=True,
        expected_video=None,
    ),
    ResetTestCase(
        name="reset with existing video and document",
        initial_document=Path("document"),
        initial_video=Path("video"),
        initial_saved=False,
        expected_video=Path("video"),
    ),
]


@pytest.mark.parametrize("case", RESET_TEST_CASES, ids=lambda case: case.name)
def test_reset(case: ResetTestCase) -> None:
    service = StateService()
    service._state = ApplicationState(case.initial_document, case.initial_video, case.initial_saved)

    service.reset()

    assert service.saved
    assert case.expected_video == service._state.video
    assert service.document is None


class ImportTestCase(NamedTuple):
    name: str
    initial_document: Path | None
    initial_video: Path | None
    initial_saved: bool
    import_documents: list[Path]
    import_video: Path | None
    video_from_subtitle: bool
    expected_document: Path | None
    expected_video: Path | None
    expected_saved: bool


IMPORT_TEST_CASES = [
    ImportTestCase(
        name="from initial state: import video only",
        initial_document=None,
        initial_video=None,
        initial_saved=True,
        import_documents=[],
        import_video=Path("video"),
        video_from_subtitle=False,
        expected_document=None,
        expected_video=Path("video"),
        expected_saved=True,
    ),
    ImportTestCase(
        name="from initial state: import different video",
        initial_document=None,
        initial_video=Path("video-initial"),
        initial_saved=True,
        import_documents=[],
        import_video=Path("video-imported"),
        video_from_subtitle=False,
        expected_document=None,
        expected_video=Path("video-imported"),
        expected_saved=True,
    ),
    ImportTestCase(
        name="from initial state: import one document with video from document",
        initial_document=None,
        initial_video=Path("video-initial"),
        initial_saved=True,
        import_documents=[Path("document")],
        import_video=Path("video-imported"),
        video_from_subtitle=False,
        expected_document=Path("document"),
        expected_video=Path("video-imported"),
        expected_saved=True,
    ),
    ImportTestCase(
        name="from initial state: import one document with video from subtitle",
        initial_document=None,
        initial_video=None,
        initial_saved=True,
        import_documents=[Path("document")],
        import_video=Path("video-imported"),
        video_from_subtitle=True,
        expected_document=None,
        expected_video=Path("video-imported"),
        expected_saved=True,
    ),
    ImportTestCase(
        name="from initial state: import multiple documents without video",
        initial_document=None,
        initial_video=Path("video-initial"),
        initial_saved=True,
        import_documents=[Path("document1"), Path("document2")],
        import_video=None,
        video_from_subtitle=False,
        expected_document=None,
        expected_video=Path("video-initial"),
        expected_saved=False,
    ),
    ImportTestCase(
        name="from initial state: import multiple documents with video from subtitle",
        initial_document=None,
        initial_video=None,
        initial_saved=True,
        import_documents=[Path("document1"), Path("document2")],
        import_video=Path("video-imported"),
        video_from_subtitle=True,
        expected_document=None,
        expected_video=Path("video-imported"),
        expected_saved=False,
    ),
    ImportTestCase(
        name="from other state: import same video, no document, should preserve state",
        initial_document=None,
        initial_video=Path("video"),
        initial_saved=True,
        import_documents=[],
        import_video=Path("video"),
        video_from_subtitle=False,
        expected_document=None,
        expected_video=Path("video"),
        expected_saved=True,
    ),
    ImportTestCase(
        name="from other state: import same video with document, should preserve document",
        initial_document=Path("document"),
        initial_video=Path("video"),
        initial_saved=False,
        import_documents=[],
        import_video=Path("video"),
        video_from_subtitle=False,
        expected_document=Path("document"),
        expected_video=Path("video"),
        expected_saved=False,
    ),
    ImportTestCase(
        name="from other state: import different video, should reset",
        initial_document=Path("document"),
        initial_video=Path("video-initial"),
        initial_saved=True,
        import_documents=[],
        import_video=Path("video-imported"),
        video_from_subtitle=False,
        expected_document=None,
        expected_video=Path("video-imported"),
        expected_saved=False,
    ),
    ImportTestCase(
        name="from other state: import document with different video from document, should reset",
        initial_document=Path("document"),
        initial_video=Path("video-1"),
        initial_saved=True,
        import_documents=[Path("imported-document")],
        import_video=Path("video-2"),
        video_from_subtitle=False,
        expected_document=None,
        expected_video=Path("video-2"),
        expected_saved=False,
    ),
    ImportTestCase(
        name="from other state: import document with different video from subtitle, should reset",
        initial_document=Path("document"),
        initial_video=Path("video-1"),
        initial_saved=True,
        import_documents=[Path("imported-document")],
        import_video=Path("video-2"),
        video_from_subtitle=True,
        expected_document=None,
        expected_video=Path("video-2"),
        expected_saved=False,
    ),
]


@pytest.mark.parametrize("case", IMPORT_TEST_CASES, ids=lambda case: case.name)
def test_import(case: ImportTestCase) -> None:
    service = StateService()
    service._state = ApplicationState(case.initial_document, case.initial_video, case.initial_saved)

    service.import_documents(case.import_documents, case.import_video, case.video_from_subtitle)

    assert case.expected_document == service.document
    assert case.expected_video == service._state.video
    assert case.expected_saved == service.saved


def test_saved_changed_signal_emits_only_on_transition() -> None:
    service = StateService()
    received: list[bool] = []
    service.saved_changed.connect(received.append)

    service.change()
    service.change()
    service.save(Path("document"))
    service.save(Path("document2"))
    service.change()
    service.reset()

    assert received == [False, True, False, True]
