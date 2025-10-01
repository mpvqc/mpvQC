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
    DocumentImporterService,
    PlayerService,
    StateService,
    TypeMapperService,
    VideoSelectorService,
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
def player_service_mock() -> MagicMock:
    return MagicMock(spec_set=PlayerService)


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
def document_not_compatible_message_box() -> MagicMock:
    return MagicMock()


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
    document_not_compatible_message_box,
) -> MpvqcManagerBackendPyObject:
    # noinspection PyCallingNonCallable
    manager = MpvqcManagerBackendPyObject()

    factory = MagicMock()
    factory.createObject.return_value = confirm_reset_message_box
    manager.message_box_new_document_factory = factory

    factory = MagicMock()
    factory.createObject.return_value = export_document_dialog
    manager.dialog_export_document_factory = factory

    factory = MagicMock()
    factory.createObject.return_value = document_not_compatible_message_box
    manager.message_box_document_not_compatible_factory = factory

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


@pytest.fixture
def reconfigure_inject(
    player_service_mock,
    type_mapper,
):
    def _reconfigure_inject(
        import_result: DocumentImporterService.DocumentImportResult,
        pick_video: Path | None = None,
    ):
        def on_video_selected(*_, **kwargs):
            kwargs["on_video_selected"](pick_video)

        video_selector_mock = MagicMock()
        video_selector_mock.select_video_from.side_effect = on_video_selected

        importer_mock = MagicMock()
        importer_mock.read.return_value = import_result

        def config(binder: inject.Binder):
            binder.bind(VideoSelectorService, video_selector_mock)
            binder.bind(DocumentImporterService, importer_mock)
            binder.bind(PlayerService, player_service_mock)
            binder.bind(TypeMapperService, type_mapper)

        inject.configure(config, clear=True)

    return _reconfigure_inject


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


def test_import_document(
    reconfigure_inject,
    configure_state,
    manager,
    type_mapper,
    comments_model_mock,
):
    reconfigure_inject(
        import_result=DocumentImporterService.DocumentImportResult(
            valid_documents=[RANDOM_FILE],
            invalid_documents=[],
            existing_videos=[],
            comments=[],
        ),
        pick_video=None,
    )

    configure_state(saved=True, document=Path.home())

    manager.open_documents_impl([type_mapper.map_path_to_url(RANDOM_FILE)])

    assert comments_model_mock.import_comments.called


def test_import_video(
    reconfigure_inject,
    configure_state,
    manager,
    type_mapper,
    player_service_mock,
    make_spy,
):
    reconfigure_inject(
        import_result=DocumentImporterService.DocumentImportResult(
            valid_documents=[],
            invalid_documents=[],
            existing_videos=[],
            comments=[],
        ),
        pick_video=RANDOM_VIDEO,
    )

    configure_state(saved=True, document=Path.home())

    manager.open_video_impl(type_mapper.map_path_to_url(RANDOM_VIDEO))

    assert player_service_mock.open_video.called


def test_import_subtitles(
    reconfigure_inject,
    manager,
    type_mapper,
    player_service_mock,
):
    reconfigure_inject(
        import_result=DocumentImporterService.DocumentImportResult(
            valid_documents=[],
            invalid_documents=[],
            existing_videos=[],
            comments=[],
        ),
        pick_video=None,
    )

    manager.open_subtitles_impl([type_mapper.map_path_to_url(RANDOM_FILE)])
    assert player_service_mock.open_subtitles.called


def test_import_multiple_files(
    reconfigure_inject,
    manager,
    type_mapper,
    comments_model_mock,
    player_service_mock,
):
    reconfigure_inject(
        import_result=DocumentImporterService.DocumentImportResult(
            valid_documents=[RANDOM_FILE, RANDOM_FILE],
            invalid_documents=[],
            existing_videos=[],
            comments=[],
        ),
        pick_video=RANDOM_VIDEO,
    )

    manager.open_impl(
        documents=[type_mapper.map_path_to_url(RANDOM_FILE)] * 2,
        videos=[type_mapper.map_path_to_url(RANDOM_VIDEO)],
        subtitles=[type_mapper.map_path_to_url(RANDOM_FILE)],
    )

    assert comments_model_mock.import_comments.called
    assert player_service_mock.open_video.called
    assert player_service_mock.open_subtitles.called


def test_import_erroneous_documents(
    reconfigure_inject,
    manager,
    type_mapper,
    player_service_mock,
    document_not_compatible_message_box,
):
    reconfigure_inject(
        import_result=DocumentImporterService.DocumentImportResult(
            valid_documents=[],
            invalid_documents=[RANDOM_FILE, RANDOM_FILE],
            existing_videos=[],
            comments=[],
        ),
        pick_video=RANDOM_VIDEO,
    )

    manager.open_impl(
        documents=[type_mapper.map_path_to_url(RANDOM_FILE)] * 2,
        videos=[type_mapper.map_path_to_url(RANDOM_VIDEO)],
        subtitles=[],
    )

    assert player_service_mock.open_video.called
    assert document_not_compatible_message_box.open.called
