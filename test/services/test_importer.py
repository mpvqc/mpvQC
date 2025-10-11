# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from typing import NamedTuple
from unittest.mock import Mock

import inject
import pytest

from mpvqc.datamodels import Comment
from mpvqc.services import (
    DocumentExportService,
    DocumentImporterService,
    ImporterService,
    PlayerService,
    SettingsService,
    StateService,
    SubtitleImporterService,
    TypeMapperService,
)
from mpvqc.services.importer import AskingAbout, ImportState


@pytest.fixture
def mock_doc_importer():
    return Mock(spec_set=DocumentImporterService)


@pytest.fixture
def mock_sub_importer():
    return Mock(spec_set=SubtitleImporterService)


@pytest.fixture
def mock_doc_exporter():
    return Mock(spec_set=DocumentExportService)


@pytest.fixture
def mock_player():
    return Mock(spec_set=PlayerService)


@pytest.fixture
def mock_state():
    return Mock(spec_set=StateService)


@pytest.fixture(autouse=True)
def configure_inject(
    settings_service,
    mock_doc_importer,
    mock_sub_importer,
    mock_doc_exporter,
    mock_player,
    mock_state,
    type_mapper,
):
    def config(binder: inject.Binder):
        binder.bind(SettingsService, settings_service)
        binder.bind(DocumentImporterService, mock_doc_importer)
        binder.bind(SubtitleImporterService, mock_sub_importer)
        binder.bind(DocumentExportService, mock_doc_exporter)
        binder.bind(PlayerService, mock_player)
        binder.bind(StateService, mock_state)
        binder.bind(TypeMapperService, type_mapper)

    inject.configure(config, clear=True)


@pytest.fixture
def configure_for_open(mock_doc_importer, mock_sub_importer, settings_service):
    def setup(document_videos, subtitle_videos, import_setting, comments: list[Comment] | None = None):
        settings_service.import_found_video = import_setting

        mock_doc_importer.read.return_value = DocumentImporterService.DocumentImportResult(
            valid_documents=[], invalid_documents=[], existing_videos=document_videos, comments=comments or []
        )
        mock_sub_importer.read.return_value = SubtitleImporterService.SubtitleImportResult(
            subtitles=[],
            existing_videos=subtitle_videos,
        )

    return setup


@pytest.fixture
def make_state():
    def _make_state(
        selected_video=None,
        valid_documents=None,
        invalid_documents=None,
        subtitles=None,
        comments=None,
        video_from_subtitle=None,
    ):
        document_result = DocumentImporterService.DocumentImportResult(
            valid_documents=valid_documents or [],
            invalid_documents=invalid_documents or [],
            existing_videos=[],
            comments=comments or [],
        )
        subtitle_result = SubtitleImporterService.SubtitleImportResult(
            subtitles=subtitles or [],
            existing_videos=[],
        )

        return ImportState(
            imported_documents=document_result,
            imported_subtitles=subtitle_result,
            dropped_videos=[],
            selected_video=selected_video,
            video_source=AskingAbout.SUBTITLE if video_from_subtitle else None,
        )

    return _make_state


@pytest.fixture
def service():
    return ImporterService()


class SynchronousTestCase(NamedTuple):
    name: str
    dropped_videos: list[Path]
    document_videos: list[Path]
    subtitle_videos: list[Path]
    import_setting: int
    expected_video: Path | None


@pytest.mark.parametrize(
    "test_case",
    [
        SynchronousTestCase(
            name="dropped_video_wins",
            dropped_videos=[Path("dropped_video")],
            document_videos=[Path("video_from_document")],
            subtitle_videos=[Path("video_from_subtitle")],
            import_setting=SettingsService.ImportFoundVideo.ALWAYS.value,
            expected_video=Path("dropped_video"),
        ),
        SynchronousTestCase(
            name="document_wins",
            dropped_videos=[],
            document_videos=[Path("video_from_document")],
            subtitle_videos=[Path("video_from_subtitle")],
            import_setting=SettingsService.ImportFoundVideo.ALWAYS.value,
            expected_video=Path("video_from_document"),
        ),
        SynchronousTestCase(
            name="document_wins",
            dropped_videos=[],
            document_videos=[],
            subtitle_videos=[Path("video_from_subtitle")],
            import_setting=SettingsService.ImportFoundVideo.ALWAYS.value,
            expected_video=Path("video_from_subtitle"),
        ),
        SynchronousTestCase(
            name="nothing",
            dropped_videos=[],
            document_videos=[Path("video_from_document")],
            subtitle_videos=[Path("video_from_subtitle")],
            import_setting=SettingsService.ImportFoundVideo.NEVER.value,
            expected_video=None,
        ),
        SynchronousTestCase(
            name="no_videos",
            dropped_videos=[],
            document_videos=[],
            subtitle_videos=[],
            import_setting=SettingsService.ImportFoundVideo.ALWAYS.value,
            expected_video=None,
        ),
    ],
    ids=lambda tc: tc.name,
)
def test_open_synchronous(
    service,
    configure_for_open,
    mock_player,
    test_case,
):
    configure_for_open(
        test_case.document_videos,
        test_case.subtitle_videos,
        test_case.import_setting,
    )

    service.open(documents=[], videos=test_case.dropped_videos, subtitles=[])

    if test_case.expected_video is None:
        mock_player.open_video.assert_not_called()
    else:
        mock_player.open_video.assert_called_once_with(str(test_case.expected_video))


class UserInteractionTestCase(NamedTuple):
    name: str
    document_videos: list[Path]
    subtitle_videos: list[Path]
    user_accepts_doc: bool | None
    user_accepts_sub: bool | None
    should_ask_about_document: bool
    should_ask_about_subtitle: bool
    expected_video: Path | None


@pytest.mark.parametrize(
    "test_case",
    [
        UserInteractionTestCase(
            name="accept_document",
            document_videos=[Path("video_from_document")],
            subtitle_videos=[Path("video_from_subtitle")],
            user_accepts_doc=True,
            user_accepts_sub=None,
            should_ask_about_document=True,
            should_ask_about_subtitle=False,
            expected_video=Path("video_from_document"),
        ),
        UserInteractionTestCase(
            name="accept_subtitle",
            document_videos=[],
            subtitle_videos=[Path("video_from_subtitle")],
            user_accepts_doc=None,
            user_accepts_sub=True,
            should_ask_about_document=False,
            should_ask_about_subtitle=True,
            expected_video=Path("video_from_subtitle"),
        ),
        UserInteractionTestCase(
            name="accept_subtitle_2",
            document_videos=[Path("video_from_document")],
            subtitle_videos=[Path("video_from_subtitle")],
            user_accepts_doc=False,
            user_accepts_sub=True,
            should_ask_about_document=True,
            should_ask_about_subtitle=True,
            expected_video=Path("video_from_subtitle"),
        ),
        UserInteractionTestCase(
            name="reject_document_reject_subtitle",
            document_videos=[Path("video_from_document")],
            subtitle_videos=[Path("video_from_subtitle")],
            user_accepts_doc=False,
            user_accepts_sub=False,
            should_ask_about_document=True,
            should_ask_about_subtitle=True,
            expected_video=None,
        ),
        UserInteractionTestCase(
            name="reject_subtitle",
            document_videos=[],
            subtitle_videos=[Path("video_from_subtitle")],
            user_accepts_doc=None,
            user_accepts_sub=False,
            should_ask_about_document=False,
            should_ask_about_subtitle=True,
            expected_video=None,
        ),
    ],
    ids=lambda tc: tc.name,
)
def test_open_with_user_interaction(
    service,
    configure_for_open,
    mock_player,
    make_spy,
    test_case,
):
    configure_for_open(
        test_case.document_videos,
        test_case.subtitle_videos,
        import_setting=SettingsService.ImportFoundVideo.ASK_EVERY_TIME.value,
    )

    doc_spy = make_spy(service.ask_user_document_video_import)
    sub_spy = make_spy(service.ask_user_subtitle_video_import)

    service.open(documents=[], videos=[], subtitles=[])

    # Check and handle document video
    assert doc_spy.count() == (1 if test_case.should_ask_about_document else 0)
    if doc_spy.count() == 1:
        import_id = doc_spy.at(0, 0)
        video_name = doc_spy.at(0, 1)
        assert video_name == test_case.document_videos[0].name
        service.continue_video_determination(import_id, test_case.user_accepts_doc)

    # Check and handle subtitle video (after document response)
    assert sub_spy.count() == (1 if test_case.should_ask_about_subtitle else 0)
    if sub_spy.count() == 1:
        import_id = sub_spy.at(0, 0)
        video_name = sub_spy.at(0, 1)
        assert video_name == test_case.subtitle_videos[0].name
        service.continue_video_determination(import_id, test_case.user_accepts_sub)

    if test_case.expected_video is None:
        mock_player.open_video.assert_not_called()
    else:
        mock_player.open_video.assert_called_once_with(str(test_case.expected_video))


def test_open_loads_comments(service, configure_for_open, make_spy):
    spy = make_spy(service.comments_ready_for_import)

    configure_for_open(
        document_videos=[],
        subtitle_videos=[],
        import_setting=SettingsService.ImportFoundVideo.ASK_EVERY_TIME.value,
        comments=[],
    )

    service.open(documents=[], videos=[], subtitles=[])
    assert spy.count() == 0

    configure_for_open(
        document_videos=[],
        subtitle_videos=[],
        import_setting=SettingsService.ImportFoundVideo.ASK_EVERY_TIME.value,
        comments=[Comment(7, "comment type", "comment")],
    )

    service.open(documents=[], videos=[], subtitles=[])
    assert spy.count() == 1


def test_continue_with_import_opens_video_when_selected(service, mock_player, make_state):
    video_path = Path.home() / "video.mp4"
    state = make_state(selected_video=video_path)

    service._continue_with_import(state)

    mock_player.open_video.assert_called_once_with(str(video_path.resolve()))


def test_continue_with_import_opens_subtitles_when_present(service, mock_player, type_mapper, make_state):
    subtitle_path = Path.home() / "sub.srt"
    state = make_state(subtitles=[subtitle_path])

    service._continue_with_import(state)

    expected_subtitles = type_mapper.map_paths_to_str([subtitle_path])
    mock_player.open_subtitles.assert_called_once_with(subtitles=expected_subtitles)


def test_continue_with_import_imports_documents_when_video_present(service, mock_state, make_state):
    docs = [Path.home() / "doc.txt"]
    video_path = Path.home() / "video.mp4"

    state = make_state(
        selected_video=video_path,
        valid_documents=docs,
        video_from_subtitle=False,
    )
    service._continue_with_import(state)
    mock_state.import_documents.assert_called_with(
        documents=docs,
        video=video_path.resolve(),
        video_from_subtitle=False,
    )

    state = make_state(
        selected_video=video_path,
        valid_documents=docs,
        video_from_subtitle=True,
    )
    service._continue_with_import(state)
    mock_state.import_documents.assert_called_with(
        documents=docs,
        video=video_path.resolve(),
        video_from_subtitle=True,
    )


def test_continue_with_import_imports_documents_when_only_documents(service, mock_state, make_state):
    docs = [Path("doc.txt")]
    state = make_state(valid_documents=docs)

    service._continue_with_import(state)

    mock_state.import_documents.assert_called_once_with(documents=docs, video=None, video_from_subtitle=False)


def test_continue_with_import_emits_invalid_documents(service, make_spy, make_state):
    spy = make_spy(service.erroneous_documents_imported)
    state = make_state(invalid_documents=[Path("bad1.txt"), Path("bad2.txt")])

    service._continue_with_import(state)

    assert spy.count() == 1
    assert spy.at(0, 0) == ["bad1.txt", "bad2.txt"]
