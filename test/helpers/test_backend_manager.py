# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later
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
from test.mocks import MockedDialog

RANDOM_FILE = Path().home() / "Documents" / "my-doc.txt"
RANDOM_VIDEO = Path().home() / "Video" / "my-video.mp4"


@pytest.fixture
def comments_model_mock() -> MagicMock:
    return MagicMock(spec_set=MpvqcCommentModel)


@pytest.fixture
def exporter_service_mock() -> MagicMock:
    return MagicMock(spec_set=DocumentExportService)


@pytest.fixture
def export_document_dialog() -> MockedDialog:
    return MockedDialog()


@pytest.fixture
def manager(
    export_document_dialog,
) -> MpvqcManagerBackendPyObject:
    # noinspection PyCallingNonCallable
    manager = MpvqcManagerBackendPyObject()

    factory = MagicMock()
    factory.createObject.return_value = export_document_dialog
    manager.dialog_export_document_factory = factory

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
