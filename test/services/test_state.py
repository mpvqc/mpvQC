# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from typing import NamedTuple

import pytest

from mpvqc.services.state import ApplicationState, StateService


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with):
    common_bindings_with()


def _make(state: ApplicationState) -> StateService:
    service = StateService()
    service._state = state
    return service


def test_save_sets_document_and_marks_saved() -> None:
    service = _make(ApplicationState(document=None, video=Path("video"), saved=False))

    service.save(Path("document"))

    assert service.document == Path("document")
    assert service.saved is True
    assert service._state.video == Path("video")


def test_change_marks_unsaved() -> None:
    service = _make(ApplicationState(document=Path("document"), video=Path("video"), saved=True))

    service.change()

    assert service.saved is False
    assert service.document == Path("document")
    assert service._state.video == Path("video")


def test_reset_clears_document_and_preserves_video() -> None:
    service = _make(ApplicationState(document=Path("document"), video=Path("video"), saved=False))

    service.reset()

    assert service.document is None
    assert service.saved is True
    assert service._state.video == Path("video")


class ImportCase(NamedTuple):
    name: str
    initial: ApplicationState
    video: Path | None
    has_comments: bool
    expected_video: Path | None
    expected_document: Path | None


IMPORT_CASES = [
    ImportCase(
        name="video into empty state: video tracked",
        initial=ApplicationState(document=None, video=None, saved=True),
        video=Path("video"),
        has_comments=False,
        expected_video=Path("video"),
        expected_document=None,
    ),
    ImportCase(
        name="no video into populated: document clears, video preserved",
        initial=ApplicationState(document=Path("doc"), video=Path("video"), saved=True),
        video=None,
        has_comments=True,
        expected_video=Path("video"),
        expected_document=None,
    ),
    ImportCase(
        name="same video, no comments, into populated: document preserved",
        initial=ApplicationState(document=Path("doc"), video=Path("video"), saved=True),
        video=Path("video"),
        has_comments=False,
        expected_video=Path("video"),
        expected_document=Path("doc"),
    ),
    ImportCase(
        name="same video with comments into populated: document clears",
        initial=ApplicationState(document=Path("doc"), video=Path("video"), saved=True),
        video=Path("video"),
        has_comments=True,
        expected_video=Path("video"),
        expected_document=None,
    ),
    ImportCase(
        name="different video into populated: video swaps and document clears",
        initial=ApplicationState(document=Path("doc"), video=Path("old"), saved=True),
        video=Path("new"),
        has_comments=True,
        expected_video=Path("new"),
        expected_document=None,
    ),
]


@pytest.mark.parametrize("case", IMPORT_CASES, ids=lambda c: c.name)
def test_apply_import(case: ImportCase) -> None:
    service = _make(case.initial)

    service.apply_import(video=case.video, has_comments=case.has_comments)

    assert service._state.video == case.expected_video
    assert service.document == case.expected_document


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
