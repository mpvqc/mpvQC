# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from typing import NamedTuple
from unittest.mock import Mock

import inject
import pytest

from mpvqc.services import (
    DocumentImporterService,
    PlayerService,
    SettingsService,
    StateService,
    SubtitleImporterService,
)
from mpvqc.services.importer import ImporterService


@pytest.fixture
def document_importer_service_mock():
    mock = Mock(spec_set=DocumentImporterService)
    mock.NO_IMPORT = DocumentImporterService.NO_IMPORT
    return mock


@pytest.fixture
def subtitle_importer_service_mock():
    mock = Mock(spec_set=SubtitleImporterService)
    mock.NO_IMPORT = SubtitleImporterService.NO_IMPORT
    return mock


@pytest.fixture
def player_service_mock():
    player = Mock(spec_set=PlayerService)
    player.is_video_loaded.return_value = False
    return player


@pytest.fixture
def state_service_mock():
    return Mock(spec_set=StateService)


@pytest.fixture(autouse=True)
def configure_inject(
    common_bindings_with,
    settings_service,
    document_importer_service_mock,
    subtitle_importer_service_mock,
    player_service_mock,
    state_service_mock,
):
    def custom_bindings(binder: inject.Binder):
        binder.bind(SettingsService, settings_service)
        binder.bind(DocumentImporterService, document_importer_service_mock)
        binder.bind(SubtitleImporterService, subtitle_importer_service_mock)
        binder.bind(PlayerService, player_service_mock)
        binder.bind(StateService, state_service_mock)

    common_bindings_with(custom_bindings)


@pytest.fixture
def service():
    return ImporterService()


def test_example_1_single_explicit_video(
    service,
    document_importer_service_mock,
    subtitle_importer_service_mock,
    player_service_mock,
    state_service_mock,
    make_spy,
):
    # Given
    video = Path.home() / "video.mp4"
    document_importer_service_mock.read.return_value = DocumentImporterService.NO_IMPORT
    subtitle_importer_service_mock.read.return_value = SubtitleImporterService.NO_IMPORT
    player_service_mock.is_video_loaded.return_value = False

    comments_spy = make_spy(service.comments_ready_for_import)
    invalid_docs_spy = make_spy(service.erroneous_documents_imported)
    ask_user_spy = make_spy(service.ask_user_what_to_import)

    # When
    service.open(documents=[], videos=[video], subtitles=[])

    # Then
    assert ask_user_spy.count() == 0
    assert comments_spy.count() == 0
    assert invalid_docs_spy.count() == 0

    player_service_mock.open_video.assert_called_once_with(video)
    state_service_mock.import_documents.assert_called_once()


def test_example_2_single_document_no_video_references(
    service,
    document_importer_service_mock,
    subtitle_importer_service_mock,
    player_service_mock,
    state_service_mock,
    make_spy,
):
    # Given
    document = Path.home() / "comments.txt"

    comment1 = Mock()
    comment2 = Mock()

    doc_result = DocumentImporterService.DocumentImportResult(
        comments=(comment1, comment2),
        valid_documents=(document,),
        invalid_documents=(),
        existing_videos=(),
        existing_subtitles=(),
    )

    document_importer_service_mock.read.return_value = doc_result
    subtitle_importer_service_mock.read.return_value = SubtitleImporterService.NO_IMPORT
    player_service_mock.is_video_loaded.return_value = False

    comments_spy = make_spy(service.comments_ready_for_import)
    invalid_docs_spy = make_spy(service.erroneous_documents_imported)
    ask_user_spy = make_spy(service.ask_user_what_to_import)

    # When
    service.open(documents=[document], videos=[], subtitles=[])

    # Then
    assert ask_user_spy.count() == 0
    assert comments_spy.count() == 1
    assert comments_spy.at(0, 0) == (comment1, comment2)
    assert invalid_docs_spy.count() == 0

    player_service_mock.open_video.assert_not_called()
    state_service_mock.import_documents.assert_called_once()


class ParameterizedTestCase(NamedTuple):
    setting: SettingsService.ImportFoundVideo
    expect_ask_user_count: int
    expect_comments_count: int
    expect_video_opened_count: int
    expect_state_updated_count: int


@pytest.mark.parametrize(
    "test_case",
    [
        ParameterizedTestCase(
            setting=SettingsService.ImportFoundVideo.ALWAYS,
            expect_ask_user_count=0,
            expect_comments_count=1,
            expect_video_opened_count=1,
            expect_state_updated_count=1,
        ),
        ParameterizedTestCase(
            setting=SettingsService.ImportFoundVideo.ASK_EVERY_TIME,
            expect_ask_user_count=1,
            expect_comments_count=0,
            expect_video_opened_count=0,
            expect_state_updated_count=0,
        ),
        ParameterizedTestCase(
            setting=SettingsService.ImportFoundVideo.NEVER,
            expect_ask_user_count=0,
            expect_comments_count=1,
            expect_video_opened_count=0,
            expect_state_updated_count=1,
        ),
    ],
    ids=["setting_always", "setting_ask", "setting_never"],
)
def test_single_document_one_video_not_loaded(
    service,
    document_importer_service_mock,
    subtitle_importer_service_mock,
    player_service_mock,
    state_service_mock,
    settings_service,
    make_spy,
    test_case: ParameterizedTestCase,
):
    # Given
    document = Path.home() / "comments.txt"
    video = Path.home() / "video.mp4"

    doc_result = DocumentImporterService.DocumentImportResult(
        comments=(Mock(),),
        valid_documents=(document,),
        invalid_documents=(),
        existing_videos=(video,),
        existing_subtitles=(),
    )

    document_importer_service_mock.read.return_value = doc_result
    subtitle_importer_service_mock.read.return_value = SubtitleImporterService.NO_IMPORT
    player_service_mock.is_video_loaded.return_value = False
    settings_service.import_found_video = test_case.setting.value

    comments_spy = make_spy(service.comments_ready_for_import)
    invalid_docs_spy = make_spy(service.erroneous_documents_imported)
    ask_user_spy = make_spy(service.ask_user_what_to_import)

    # When
    service.open(documents=[document], videos=[], subtitles=[])

    # Then
    assert ask_user_spy.count() == test_case.expect_ask_user_count
    assert comments_spy.count() == test_case.expect_comments_count
    assert invalid_docs_spy.count() == 0

    assert player_service_mock.open_video.call_count == test_case.expect_video_opened_count
    assert state_service_mock.import_documents.call_count == test_case.expect_state_updated_count


def test_single_document_one_video_already_loaded(
    service,
    document_importer_service_mock,
    subtitle_importer_service_mock,
    player_service_mock,
    state_service_mock,
    make_spy,
):
    # Given
    document = Path.home() / "comments.txt"
    video = Path.home() / "video.mp4"

    doc_result = DocumentImporterService.DocumentImportResult(
        comments=(Mock(),),
        valid_documents=(document,),
        invalid_documents=(),
        existing_videos=(video,),
        existing_subtitles=(),
    )

    document_importer_service_mock.read.return_value = doc_result
    subtitle_importer_service_mock.read.return_value = SubtitleImporterService.NO_IMPORT
    player_service_mock.is_video_loaded.return_value = True

    comments_spy = make_spy(service.comments_ready_for_import)
    invalid_docs_spy = make_spy(service.erroneous_documents_imported)
    ask_user_spy = make_spy(service.ask_user_what_to_import)

    # When
    service.open(documents=[document], videos=[], subtitles=[])

    # Then
    assert ask_user_spy.count() == 0
    assert comments_spy.count() == 1
    assert invalid_docs_spy.count() == 0

    assert player_service_mock.open_video.call_count == 0
    assert state_service_mock.import_documents.call_count == 1


def test_single_document_multiple_videos(
    service,
    document_importer_service_mock,
    subtitle_importer_service_mock,
    player_service_mock,
    state_service_mock,
    make_spy,
):
    # Given
    document = Path.home() / "comments.txt"
    subtitle = Path.home() / "subs.srt"
    video1 = Path.home() / "video1.mp4"
    video2 = Path.home() / "video2.mp4"

    doc_result = DocumentImporterService.DocumentImportResult(
        comments=(Mock(),),
        valid_documents=(document,),
        invalid_documents=(),
        existing_videos=(video1,),
        existing_subtitles=(subtitle,),
    )

    sub_result = SubtitleImporterService.SubtitleImportResult(
        subtitles=(subtitle,),
        existing_videos=(video2,),
    )

    document_importer_service_mock.read.return_value = doc_result
    subtitle_importer_service_mock.read.return_value = sub_result
    player_service_mock.is_video_loaded.return_value = False

    comments_spy = make_spy(service.comments_ready_for_import)
    invalid_docs_spy = make_spy(service.erroneous_documents_imported)
    ask_user_spy = make_spy(service.ask_user_what_to_import)

    # When
    service.open(documents=[document], videos=[], subtitles=[])

    # Then
    assert ask_user_spy.count() == 1
    assert comments_spy.count() == 0
    assert invalid_docs_spy.count() == 0

    assert player_service_mock.open_video.call_count == 0
    assert state_service_mock.import_documents.call_count == 0


@pytest.mark.parametrize(
    "test_case",
    [
        ParameterizedTestCase(
            setting=SettingsService.ImportFoundVideo.ALWAYS,
            expect_ask_user_count=0,
            expect_comments_count=1,
            expect_video_opened_count=1,
            expect_state_updated_count=1,
        ),
        ParameterizedTestCase(
            setting=SettingsService.ImportFoundVideo.ASK_EVERY_TIME,
            expect_ask_user_count=1,
            expect_comments_count=0,
            expect_video_opened_count=0,
            expect_state_updated_count=0,
        ),
        ParameterizedTestCase(
            setting=SettingsService.ImportFoundVideo.NEVER,
            expect_ask_user_count=0,
            expect_comments_count=1,
            expect_video_opened_count=0,
            expect_state_updated_count=1,
        ),
    ],
    ids=["setting_always", "setting_ask", "setting_never"],
)
def test_single_document_video_from_subtitle_not_loaded(
    service,
    document_importer_service_mock,
    subtitle_importer_service_mock,
    player_service_mock,
    state_service_mock,
    settings_service,
    make_spy,
    test_case: ParameterizedTestCase,
):
    # Given
    document = Path.home() / "comments.txt"
    subtitle = Path.home() / "subs.srt"
    video = Path.home() / "video.mp4"

    doc_result = DocumentImporterService.DocumentImportResult(
        comments=(Mock(),),
        valid_documents=(document,),
        invalid_documents=(),
        existing_videos=(),
        existing_subtitles=(subtitle,),
    )

    sub_result = SubtitleImporterService.SubtitleImportResult(
        subtitles=(subtitle,),
        existing_videos=(video,),
    )

    document_importer_service_mock.read.return_value = doc_result
    subtitle_importer_service_mock.read.return_value = sub_result
    player_service_mock.is_video_loaded.return_value = False
    settings_service.import_found_video = test_case.setting.value

    comments_spy = make_spy(service.comments_ready_for_import)
    invalid_docs_spy = make_spy(service.erroneous_documents_imported)
    ask_user_spy = make_spy(service.ask_user_what_to_import)

    # When
    service.open(documents=[document], videos=[], subtitles=[])

    # Then
    assert ask_user_spy.count() == test_case.expect_ask_user_count
    assert comments_spy.count() == test_case.expect_comments_count
    assert invalid_docs_spy.count() == 0

    assert player_service_mock.open_video.call_count == test_case.expect_video_opened_count
    assert state_service_mock.import_documents.call_count == test_case.expect_state_updated_count


@pytest.mark.parametrize(
    "test_case",
    [
        ParameterizedTestCase(
            setting=SettingsService.ImportFoundVideo.ALWAYS,
            expect_ask_user_count=0,
            expect_comments_count=1,
            expect_video_opened_count=1,
            expect_state_updated_count=1,
        ),
        ParameterizedTestCase(
            setting=SettingsService.ImportFoundVideo.ASK_EVERY_TIME,
            expect_ask_user_count=1,
            expect_comments_count=0,
            expect_video_opened_count=0,
            expect_state_updated_count=0,
        ),
        ParameterizedTestCase(
            setting=SettingsService.ImportFoundVideo.NEVER,
            expect_ask_user_count=0,
            expect_comments_count=1,
            expect_video_opened_count=0,
            expect_state_updated_count=1,
        ),
    ],
    ids=["setting_always", "setting_ask", "setting_never"],
)
def test_single_document_video_and_subtitle_same_video_not_loaded(
    service,
    document_importer_service_mock,
    subtitle_importer_service_mock,
    player_service_mock,
    state_service_mock,
    settings_service,
    make_spy,
    test_case: ParameterizedTestCase,
):
    # Given
    document = Path.home() / "comments.txt"
    subtitle = Path.home() / "subs.srt"
    video = Path.home() / "video.mp4"

    doc_result = DocumentImporterService.DocumentImportResult(
        comments=(Mock(),),
        valid_documents=(document,),
        invalid_documents=(),
        existing_videos=(video,),
        existing_subtitles=(subtitle,),
    )

    sub_result = SubtitleImporterService.SubtitleImportResult(
        subtitles=(subtitle,),
        existing_videos=(video,),
    )

    document_importer_service_mock.read.return_value = doc_result
    subtitle_importer_service_mock.read.return_value = sub_result
    player_service_mock.is_video_loaded.return_value = False
    settings_service.import_found_video = test_case.setting.value

    comments_spy = make_spy(service.comments_ready_for_import)
    invalid_docs_spy = make_spy(service.erroneous_documents_imported)
    ask_user_spy = make_spy(service.ask_user_what_to_import)

    # When
    service.open(documents=[document], videos=[], subtitles=[])

    # Then
    assert ask_user_spy.count() == test_case.expect_ask_user_count
    assert comments_spy.count() == test_case.expect_comments_count
    assert invalid_docs_spy.count() == 0

    assert player_service_mock.open_video.call_count == test_case.expect_video_opened_count
    assert state_service_mock.import_documents.call_count == test_case.expect_state_updated_count

    if test_case.expect_video_opened_count > 0:
        player_service_mock.open_video.assert_called_once_with(video)
        player_service_mock.open_subtitles.assert_called_once_with((subtitle,))
    elif test_case.expect_ask_user_count == 0:
        player_service_mock.open_subtitles.assert_called_once_with((subtitle,))


def test_single_document_video_and_subtitle_same_video_already_loaded(
    service,
    document_importer_service_mock,
    subtitle_importer_service_mock,
    player_service_mock,
    state_service_mock,
    make_spy,
):
    # Given
    document = Path.home() / "comments.txt"
    subtitle = Path.home() / "subs.srt"
    video = Path.home() / "video.mp4"

    doc_result = DocumentImporterService.DocumentImportResult(
        comments=(Mock(),),
        valid_documents=(document,),
        invalid_documents=(),
        existing_videos=(video,),
        existing_subtitles=(subtitle,),
    )

    sub_result = SubtitleImporterService.SubtitleImportResult(
        subtitles=(subtitle,),
        existing_videos=(video,),
    )

    document_importer_service_mock.read.return_value = doc_result
    subtitle_importer_service_mock.read.return_value = sub_result
    player_service_mock.is_video_loaded.return_value = True

    comments_spy = make_spy(service.comments_ready_for_import)
    invalid_docs_spy = make_spy(service.erroneous_documents_imported)
    ask_user_spy = make_spy(service.ask_user_what_to_import)

    # When
    service.open(documents=[document], videos=[], subtitles=[])

    # Then
    assert ask_user_spy.count() == 0
    assert comments_spy.count() == 1
    assert invalid_docs_spy.count() == 0

    player_service_mock.open_video.assert_not_called()
    player_service_mock.open_subtitles.assert_called_once_with((subtitle,))
    state_service_mock.import_documents.assert_called_once()


def test_multiple_documents_single_video_already_loaded(
    service,
    document_importer_service_mock,
    subtitle_importer_service_mock,
    player_service_mock,
    state_service_mock,
    make_spy,
):
    # Given
    document1 = Path.home() / "comments1.txt"
    document2 = Path.home() / "comments2.txt"
    subtitle1 = Path.home() / "subs1.srt"
    subtitle2 = Path.home() / "subs2.srt"
    video = Path.home() / "video.mp4"

    comment1 = Mock()
    comment2 = Mock()

    doc_result = DocumentImporterService.DocumentImportResult(
        comments=(comment1, comment2),
        valid_documents=(document1, document2),
        invalid_documents=(),
        existing_videos=(video,),
        existing_subtitles=(subtitle1, subtitle2),
    )

    sub_result = SubtitleImporterService.SubtitleImportResult(
        subtitles=(subtitle1, subtitle2),
        existing_videos=(video,),
    )

    document_importer_service_mock.read.return_value = doc_result
    subtitle_importer_service_mock.read.return_value = sub_result
    player_service_mock.is_video_loaded.return_value = True

    comments_spy = make_spy(service.comments_ready_for_import)
    invalid_docs_spy = make_spy(service.erroneous_documents_imported)
    ask_user_spy = make_spy(service.ask_user_what_to_import)

    # When
    service.open(documents=[document1, document2], videos=[], subtitles=[])

    # Then
    assert ask_user_spy.count() == 0
    assert comments_spy.count() == 1
    assert comments_spy.at(0, 0) == (comment1, comment2)
    assert invalid_docs_spy.count() == 0

    assert player_service_mock.open_video.call_count == 0
    player_service_mock.open_subtitles.assert_called_once_with((subtitle1, subtitle2))
    assert state_service_mock.import_documents.call_count == 1


def test_multiple_documents_video_not_loaded(
    service,
    document_importer_service_mock,
    subtitle_importer_service_mock,
    player_service_mock,
    state_service_mock,
    make_spy,
):
    # Given
    document1 = Path.home() / "comments1.txt"
    document2 = Path.home() / "comments2.txt"
    subtitle1 = Path.home() / "subs1.srt"
    subtitle2 = Path.home() / "subs2.srt"
    video1 = Path.home() / "video1.mp4"
    video2 = Path.home() / "video2.mp4"
    video3 = Path.home() / "video3.mp4"

    comment1 = Mock()
    comment2 = Mock()

    doc_result = DocumentImporterService.DocumentImportResult(
        comments=(comment1, comment2),
        valid_documents=(document1, document2),
        invalid_documents=(),
        existing_videos=(video1,),
        existing_subtitles=(subtitle1, subtitle2),
    )

    sub_result = SubtitleImporterService.SubtitleImportResult(
        subtitles=(subtitle1, subtitle2),
        existing_videos=(video2, video3),
    )

    document_importer_service_mock.read.return_value = doc_result
    subtitle_importer_service_mock.read.return_value = sub_result
    player_service_mock.is_video_loaded.return_value = False

    comments_spy = make_spy(service.comments_ready_for_import)
    invalid_docs_spy = make_spy(service.erroneous_documents_imported)
    ask_user_spy = make_spy(service.ask_user_what_to_import)

    # When
    service.open(documents=[document1, document2], videos=[], subtitles=[])

    # Then
    assert ask_user_spy.count() == 1

    # Verify ask_user signal contents
    asked_videos = ask_user_spy.at(0, 0)
    asked_subtitles = ask_user_spy.at(0, 1)
    assert len(asked_videos) == 3
    video_paths = [v.path for v in asked_videos]
    assert set(video_paths) == {video1, video2, video3}
    assert set(asked_subtitles) == {subtitle1, subtitle2}

    assert comments_spy.count() == 0
    assert invalid_docs_spy.count() == 0

    assert player_service_mock.open_video.call_count == 0
    assert state_service_mock.import_documents.call_count == 0


def test_document_and_explicit_video(
    service,
    document_importer_service_mock,
    subtitle_importer_service_mock,
    player_service_mock,
    state_service_mock,
    make_spy,
):
    # Given
    document = Path.home() / "comments.txt"
    video = Path.home() / "video.mp4"
    subtitle = Path.home() / "subs.srt"

    comment1 = Mock()
    comment2 = Mock()

    doc_result = DocumentImporterService.DocumentImportResult(
        comments=(comment1, comment2),
        valid_documents=(document,),
        invalid_documents=(),
        existing_videos=(),
        existing_subtitles=(subtitle,),
    )

    sub_result = SubtitleImporterService.SubtitleImportResult(
        subtitles=(subtitle,),
        existing_videos=(),
    )

    document_importer_service_mock.read.return_value = doc_result
    subtitle_importer_service_mock.read.return_value = sub_result
    player_service_mock.is_video_loaded.return_value = False

    comments_spy = make_spy(service.comments_ready_for_import)
    invalid_docs_spy = make_spy(service.erroneous_documents_imported)
    ask_user_spy = make_spy(service.ask_user_what_to_import)

    # When
    service.open(documents=[document], videos=[video], subtitles=[])

    # Then
    assert ask_user_spy.count() == 0
    assert comments_spy.count() == 1
    assert comments_spy.at(0, 0) == (comment1, comment2)
    assert invalid_docs_spy.count() == 0

    player_service_mock.open_video.assert_called_once_with(video)
    player_service_mock.open_subtitles.assert_called_once_with((subtitle,))
    state_service_mock.import_documents.assert_called_once()


def test_multiple_subtitles_same_video_already_loaded(
    service,
    document_importer_service_mock,
    subtitle_importer_service_mock,
    player_service_mock,
    state_service_mock,
    make_spy,
):
    # Given
    subtitle1 = Path.home() / "subs1.srt"
    subtitle2 = Path.home() / "subs2.srt"
    video = Path.home() / "video.mp4"

    sub_result = SubtitleImporterService.SubtitleImportResult(
        subtitles=(subtitle1, subtitle2),
        existing_videos=(video, video),
    )

    document_importer_service_mock.read.return_value = DocumentImporterService.NO_IMPORT
    subtitle_importer_service_mock.read.return_value = sub_result
    player_service_mock.is_video_loaded.return_value = True

    comments_spy = make_spy(service.comments_ready_for_import)
    invalid_docs_spy = make_spy(service.erroneous_documents_imported)
    ask_user_spy = make_spy(service.ask_user_what_to_import)

    # When
    service.open(documents=[], videos=[], subtitles=[subtitle1, subtitle2])

    # Then
    assert ask_user_spy.count() == 0
    assert comments_spy.count() == 0
    assert invalid_docs_spy.count() == 0

    player_service_mock.open_video.assert_not_called()
    player_service_mock.open_subtitles.assert_called_once_with((subtitle1, subtitle2))
    state_service_mock.import_documents.assert_not_called()


def test_multiple_subtitles_different_videos(
    service,
    document_importer_service_mock,
    subtitle_importer_service_mock,
    player_service_mock,
    state_service_mock,
    make_spy,
):
    # Given
    subtitle1 = Path.home() / "subs1.srt"
    subtitle2 = Path.home() / "subs2.srt"
    video1 = Path.home() / "video1.mp4"
    video2 = Path.home() / "video2.mp4"

    sub_result = SubtitleImporterService.SubtitleImportResult(
        subtitles=(subtitle1, subtitle2),
        existing_videos=(video1, video2),
    )

    document_importer_service_mock.read.return_value = DocumentImporterService.NO_IMPORT
    subtitle_importer_service_mock.read.return_value = sub_result
    player_service_mock.is_video_loaded.return_value = False

    comments_spy = make_spy(service.comments_ready_for_import)
    invalid_docs_spy = make_spy(service.erroneous_documents_imported)
    ask_user_spy = make_spy(service.ask_user_what_to_import)

    # When
    service.open(documents=[], videos=[], subtitles=[subtitle1, subtitle2])

    # Then
    assert ask_user_spy.count() == 1

    # Verify ask_user signal contents
    asked_videos = ask_user_spy.at(0, 0)
    asked_subtitles = ask_user_spy.at(0, 1)
    assert len(asked_videos) == 2
    video_paths = [v.path for v in asked_videos]
    assert set(video_paths) == {video1, video2}
    assert set(asked_subtitles) == {subtitle1, subtitle2}

    assert comments_spy.count() == 0
    assert invalid_docs_spy.count() == 0

    player_service_mock.open_video.assert_not_called()
    player_service_mock.open_subtitles.assert_not_called()
    state_service_mock.import_documents.assert_not_called()


class ParameterizedTestCase(NamedTuple):
    setting: SettingsService.ImportFoundVideo
    expect_ask_user_count: int
    expect_comments_count: int
    expect_video_opened_count: int
    expect_state_updated_count: int
    expect_subtitles_opened_count: int = 0  # Add default for existing tests


@pytest.mark.parametrize(
    "test_case",
    [
        ParameterizedTestCase(
            setting=SettingsService.ImportFoundVideo.ALWAYS,
            expect_ask_user_count=0,
            expect_comments_count=0,
            expect_video_opened_count=1,
            expect_state_updated_count=1,
            expect_subtitles_opened_count=1,
        ),
        ParameterizedTestCase(
            setting=SettingsService.ImportFoundVideo.ASK_EVERY_TIME,
            expect_ask_user_count=1,
            expect_comments_count=0,
            expect_video_opened_count=0,
            expect_state_updated_count=0,
            expect_subtitles_opened_count=0,
        ),
        ParameterizedTestCase(
            setting=SettingsService.ImportFoundVideo.NEVER,
            expect_ask_user_count=0,
            expect_comments_count=0,
            expect_video_opened_count=0,
            expect_state_updated_count=0,
            expect_subtitles_opened_count=1,
        ),
    ],
    ids=["setting_always", "setting_ask", "setting_never"],
)
def test_subtitle_with_video_reference_not_loaded(
    service,
    document_importer_service_mock,
    subtitle_importer_service_mock,
    player_service_mock,
    state_service_mock,
    settings_service,
    make_spy,
    test_case: ParameterizedTestCase,
):
    # Given
    subtitle = Path.home() / "subs.srt"
    video = Path.home() / "video.mp4"

    sub_result = SubtitleImporterService.SubtitleImportResult(
        subtitles=(subtitle,),
        existing_videos=(video,),
    )

    document_importer_service_mock.read.return_value = DocumentImporterService.NO_IMPORT
    subtitle_importer_service_mock.read.return_value = sub_result
    player_service_mock.is_video_loaded.return_value = False
    settings_service.import_found_video = test_case.setting.value

    comments_spy = make_spy(service.comments_ready_for_import)
    invalid_docs_spy = make_spy(service.erroneous_documents_imported)
    ask_user_spy = make_spy(service.ask_user_what_to_import)

    # When
    service.open(documents=[], videos=[], subtitles=[subtitle])

    # Then
    assert ask_user_spy.count() == test_case.expect_ask_user_count
    assert comments_spy.count() == test_case.expect_comments_count
    assert invalid_docs_spy.count() == 0

    assert player_service_mock.open_video.call_count == test_case.expect_video_opened_count
    assert player_service_mock.open_subtitles.call_count == test_case.expect_subtitles_opened_count
    assert state_service_mock.import_documents.call_count == test_case.expect_state_updated_count


def test_multiple_explicit_videos(
    service,
    document_importer_service_mock,
    subtitle_importer_service_mock,
    player_service_mock,
    state_service_mock,
    make_spy,
):
    # Given
    video1 = Path.home() / "video1.mp4"
    video2 = Path.home() / "video2.mp4"

    document_importer_service_mock.read.return_value = DocumentImporterService.NO_IMPORT
    subtitle_importer_service_mock.read.return_value = SubtitleImporterService.NO_IMPORT
    player_service_mock.is_video_loaded.return_value = False

    comments_spy = make_spy(service.comments_ready_for_import)
    invalid_docs_spy = make_spy(service.erroneous_documents_imported)
    ask_user_spy = make_spy(service.ask_user_what_to_import)

    # When
    service.open(documents=[], videos=[video1, video2], subtitles=[])

    # Then
    assert ask_user_spy.count() == 1

    # Verify ask_user signal contents
    asked_videos = ask_user_spy.at(0, 0)
    asked_subtitles = ask_user_spy.at(0, 1)
    assert len(asked_videos) == 2
    video_paths = [v.path for v in asked_videos]
    assert set(video_paths) == {video1, video2}
    assert asked_subtitles == ()

    assert comments_spy.count() == 0
    assert invalid_docs_spy.count() == 0

    player_service_mock.open_video.assert_not_called()
    player_service_mock.open_subtitles.assert_not_called()
    state_service_mock.import_documents.assert_not_called()


def test_multiple_videos_one_already_loaded(
    service,
    document_importer_service_mock,
    subtitle_importer_service_mock,
    player_service_mock,
    state_service_mock,
    make_spy,
):
    # Given
    document = Path.home() / "comments.txt"
    subtitle1 = Path.home() / "subs1.srt"
    subtitle2 = Path.home() / "subs2.srt"
    video1 = Path.home() / "video1.mp4"  # This one is already loaded
    video2 = Path.home() / "video2.mp4"

    comment1 = Mock()
    comment2 = Mock()

    doc_result = DocumentImporterService.DocumentImportResult(
        comments=(comment1, comment2),
        valid_documents=(document,),
        invalid_documents=(),
        existing_videos=(),
        existing_subtitles=(subtitle1, subtitle2),
    )

    sub_result = SubtitleImporterService.SubtitleImportResult(
        subtitles=(subtitle1, subtitle2),
        existing_videos=(video1, video2),
    )

    document_importer_service_mock.read.return_value = doc_result
    subtitle_importer_service_mock.read.return_value = sub_result

    # video1 is already loaded
    player_service_mock.is_video_loaded.side_effect = lambda path: path == video1

    comments_spy = make_spy(service.comments_ready_for_import)
    invalid_docs_spy = make_spy(service.erroneous_documents_imported)
    ask_user_spy = make_spy(service.ask_user_what_to_import)

    # When
    service.open(documents=[document], videos=[], subtitles=[])

    # Then
    assert ask_user_spy.count() == 0
    assert comments_spy.count() == 1
    assert comments_spy.at(0, 0) == (comment1, comment2)
    assert invalid_docs_spy.count() == 0

    player_service_mock.open_video.assert_not_called()
    player_service_mock.open_subtitles.assert_called_once_with((subtitle1, subtitle2))
    state_service_mock.import_documents.assert_called_once()
