# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

import pytest

from mpvqc.services.state import ApplicationState, StateService


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with):
    common_bindings_with()


def _make(state: ApplicationState) -> StateService:
    service = StateService()
    service._state = state
    return service


def test_record_save_sets_document_and_marks_saved() -> None:
    service = _make(ApplicationState(document=None, saved=False))

    service.record_save(Path("document"))

    assert service.document == Path("document")
    assert service.saved is True


def test_record_change_marks_unsaved() -> None:
    service = _make(ApplicationState(document=Path("document"), saved=True))

    service.record_change()

    assert service.saved is False
    assert service.document == Path("document")


def test_record_reset_clears_document_and_marks_saved() -> None:
    service = _make(ApplicationState(document=Path("document"), saved=False))

    service.record_reset()

    assert service.document is None
    assert service.saved is True


def test_record_import_clears_document_and_marks_unsaved() -> None:
    service = _make(ApplicationState(document=Path("document"), saved=True))

    service.record_import()

    assert service.document is None
    assert service.saved is False


def test_saved_changed_signal_emits_only_on_transition() -> None:
    service = StateService()
    received: list[bool] = []
    service.saved_changed.connect(received.append)

    service.record_change()
    service.record_change()
    service.record_save(Path("document"))
    service.record_save(Path("document2"))
    service.record_change()
    service.record_reset()

    assert received == [False, True, False, True]


def test_has_unsaved_document_signal_emits_only_on_transition() -> None:
    service = StateService()
    received: list[bool] = []
    service.has_unsaved_document_changed.connect(received.append)

    service.record_import()  # unsaved, no doc → False stays False
    service.record_save(Path("doc"))  # saved → False stays False
    service.record_change()  # unsaved with doc → True
    service.record_change()  # idempotent
    service.record_save(Path("doc"))  # saved again → False
    service.record_change()  # True
    service.record_import()  # clears doc → False

    assert received == [True, False, True, False]
