# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later
from collections.abc import Callable
from pathlib import Path
from unittest.mock import MagicMock, patch

import inject
import pytest

from mpvqc.helpers import MpvqcManagerBackendPyObject
from mpvqc.models import MpvqcCommentModel
from mpvqc.services import (
    DocumentExportService,
    StateService,
)
from test.mocks import MockedDialog, MockedMessageBox

RANDOM_FILE = Path().home() / "Documents" / "my-doc.txt"
RANDOM_VIDEO = Path().home() / "Video" / "my-video.mp4"


@pytest.fixture
def comments_model_mock() -> MagicMock:
    return MagicMock(spec_set=MpvqcCommentModel)


@pytest.fixture
def exporter_service_mock() -> MagicMock:
    return MagicMock(spec_set=DocumentExportService)


@pytest.fixture
def state_service() -> StateService:
    return StateService()


@pytest.fixture
def configure_state(state_service) -> Callable:
    from mpvqc.services.state import ApplicationState

    def _configure(**kwargs):
        # noinspection PyProtectedMember
        old = state_service._state
        state_service._state = ApplicationState(
            document=kwargs.get("document", old.document),
            video=kwargs.get("video", old.video),
            saved=bool(kwargs.get("saved", old.saved)),
        )

    return _configure


@pytest.fixture
def confirm_reset_message_box() -> MockedMessageBox:
    return MockedMessageBox()


@pytest.fixture
def export_document_dialog() -> MockedDialog:
    return MockedDialog()


@pytest.fixture
def manager(
    confirm_reset_message_box,
    export_document_dialog,
) -> MpvqcManagerBackendPyObject:
    # noinspection PyCallingNonCallable
    manager = MpvqcManagerBackendPyObject()

    factory = MagicMock()
    factory.createObject.return_value = confirm_reset_message_box
    manager.message_box_new_document_factory = factory

    factory = MagicMock()
    factory.createObject.return_value = export_document_dialog
    manager.dialog_export_document_factory = factory

    manager.message_box_video_found_factory = MagicMock()

    return manager


@pytest.fixture(autouse=True)
def qt_app(comments_model_mock):
    with patch("mpvqc.helpers.backend_manager.QCoreApplication.instance", return_value=MagicMock()) as mock:
        mock.return_value.find_object.return_value = comments_model_mock
        yield mock


@pytest.fixture(autouse=True)
def configure_inject(exporter_service_mock, state_service):
    def config(binder: inject.Binder):
        binder.bind(DocumentExportService, exporter_service_mock)
        binder.bind(StateService, state_service)

    inject.configure(config, clear=True, allow_override=True)


def test_reset_saved_state(manager, configure_state, comments_model_mock):
    configure_state(saved=True)
    assert manager.saved

    manager.reset_impl()
    assert comments_model_mock.clear_comments.called
    assert manager.saved


def test_reset_unsaved_state_do_reset(manager, configure_state, comments_model_mock, confirm_reset_message_box):
    configure_state(saved=False)

    manager.reset_impl()
    confirm_reset_message_box.accepted.emit()

    assert comments_model_mock.clear_comments.called
    assert manager.saved


def test_reset_unsaved_state_cancel_reset(manager, configure_state, comments_model_mock, confirm_reset_message_box):
    configure_state(saved=False)

    manager.reset_impl()
    confirm_reset_message_box.rejected.emit()

    assert not comments_model_mock.clear_comments.called
    assert not manager.saved


def test_save_saved_state_no_document_opens_dialog(
    manager,
    configure_state,
    export_document_dialog,
    exporter_service_mock,
):
    configure_state(saved=True)

    manager.save_impl()

    assert export_document_dialog.openCalled
    assert not exporter_service_mock.save.called


def test_save_saved_state_with_document(
    manager,
    configure_state,
    export_document_dialog,
    exporter_service_mock,
):
    configure_state(saved=True, document=RANDOM_FILE)

    manager.save_impl()

    assert not export_document_dialog.openCalled
    assert exporter_service_mock.save.called
    saved_path = exporter_service_mock.save.call_args[0][0]
    assert saved_path == RANDOM_FILE


def test_save_unsaved_state_do_save(
    manager,
    configure_state,
    export_document_dialog,
    exporter_service_mock,
    type_mapper,
    make_spy,
):
    configure_state(saved=False)
    saved_spy = make_spy(manager.savedChanged)

    manager.save_impl()

    assert export_document_dialog.openCalled

    export_document_dialog.savePressed.emit(type_mapper.map_path_to_url(RANDOM_FILE))

    assert exporter_service_mock.save.called
    saved_path = exporter_service_mock.save.call_args[0][0]
    assert saved_path == RANDOM_FILE
    assert saved_spy.count() == 1


def test_save_unsaved_state_cancel_save(
    manager,
    configure_state,
    export_document_dialog,
    exporter_service_mock,
    make_spy,
):
    configure_state(saved=False)
    saved_spy = make_spy(manager.savedChanged)

    manager.save_impl()

    assert export_document_dialog.openCalled
    export_document_dialog.rejected.emit()
    assert saved_spy.count() == 0
