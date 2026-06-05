# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.datamodels import (
    Comment,
    DocumentImportResult,
    SubtitleImportResult,
    SubtitleSource,
    VideoSource,
)
from mpvqc.services.importer import DocumentImporterService
from mpvqc.services.importer.scanner import ResourceScanner
from mpvqc.services.subtitle_importer import SubtitleImporterService

DOC_A = Path("/work/a.qc")
DOC_B = Path("/work/b.qc")
DOC_BROKEN = Path("/work/broken.qc")
VIDEO_A = Path("/movies/a.mp4")
VIDEO_B = Path("/movies/b.mkv")
SUB_A = Path("/work/a.en.srt")
SUB_B = Path("/work/a.ja.srt")
COMMENT = Comment(time=0, comment_type="", comment="")


@pytest.fixture
def doc_importer_mock() -> MagicMock:
    mock = MagicMock(spec_set=DocumentImporterService)
    mock.read.return_value = DocumentImportResult(
        valid_documents=(),
        invalid_documents=(),
        existing_videos=(),
        existing_subtitles=(),
        comments=(),
    )
    return mock


@pytest.fixture
def sub_importer_mock() -> MagicMock:
    mock = MagicMock(spec_set=SubtitleImporterService)
    mock.read.return_value = SubtitleImportResult(subtitles=(), existing_videos=())
    return mock


@pytest.fixture(autouse=True)
def configure_inject(doc_importer_mock: MagicMock, sub_importer_mock: MagicMock) -> None:
    def config(binder: inject.Binder) -> None:
        binder.bind(DocumentImporterService, doc_importer_mock)
        binder.bind(SubtitleImporterService, sub_importer_mock)

    inject.configure(config, allow_override=True, bind_in_runtime=False, clear=True)


@pytest.fixture
def scanner() -> ResourceScanner:
    return ResourceScanner()


def test_explicit_video_gets_explicit_flag(scanner: ResourceScanner) -> None:
    result = scanner.scan(documents=[], videos=[VIDEO_A], subtitles=[])
    assert result.videos == (VideoSource(path=VIDEO_A, explicitly_provided=True),)


def test_doc_video_gets_doc_flag(scanner: ResourceScanner, doc_importer_mock: MagicMock) -> None:
    doc_importer_mock.read.return_value = DocumentImportResult(
        valid_documents=(DOC_A,),
        invalid_documents=(),
        existing_videos=(VIDEO_A,),
        existing_subtitles=(),
        comments=(),
    )

    result = scanner.scan(documents=[DOC_A], videos=[], subtitles=[])

    assert result.videos == (VideoSource(path=VIDEO_A, found_in_document=True),)


def test_subtitle_referenced_video_gets_subtitle_flag(
    scanner: ResourceScanner,
    sub_importer_mock: MagicMock,
) -> None:
    sub_importer_mock.read.return_value = SubtitleImportResult(
        subtitles=(SUB_A,),
        existing_videos=(VIDEO_A,),
    )

    result = scanner.scan(documents=[], videos=[], subtitles=[SUB_A])

    assert result.videos == (VideoSource(path=VIDEO_A, found_in_subtitle=True),)


def test_video_sources_merge_flags_when_path_collides(
    scanner: ResourceScanner,
    doc_importer_mock: MagicMock,
    sub_importer_mock: MagicMock,
) -> None:
    doc_importer_mock.read.return_value = DocumentImportResult(
        valid_documents=(DOC_A,),
        invalid_documents=(),
        existing_videos=(VIDEO_A,),
        existing_subtitles=(),
        comments=(),
    )
    sub_importer_mock.read.return_value = SubtitleImportResult(subtitles=(SUB_A,), existing_videos=(VIDEO_A,))

    result = scanner.scan(documents=[DOC_A], videos=[VIDEO_A], subtitles=[SUB_A])

    assert result.videos == (
        VideoSource(path=VIDEO_A, explicitly_provided=True, found_in_document=True, found_in_subtitle=True),
    )


def test_explicit_subtitle_gets_explicit_flag(scanner: ResourceScanner) -> None:
    result = scanner.scan(documents=[], videos=[], subtitles=[SUB_A])
    assert result.subtitles == (SubtitleSource(path=SUB_A, explicitly_provided=True),)


def test_doc_subtitle_gets_doc_flag(scanner: ResourceScanner, doc_importer_mock: MagicMock) -> None:
    doc_importer_mock.read.return_value = DocumentImportResult(
        valid_documents=(DOC_A,),
        invalid_documents=(),
        existing_videos=(),
        existing_subtitles=(SUB_A,),
        comments=(),
    )

    result = scanner.scan(documents=[DOC_A], videos=[], subtitles=[])

    assert result.subtitles == (SubtitleSource(path=SUB_A, found_in_document=True),)


def test_subtitle_sources_merge_flags_when_path_collides(
    scanner: ResourceScanner,
    doc_importer_mock: MagicMock,
) -> None:
    doc_importer_mock.read.return_value = DocumentImportResult(
        valid_documents=(DOC_A,),
        invalid_documents=(),
        existing_videos=(),
        existing_subtitles=(SUB_A,),
        comments=(),
    )

    result = scanner.scan(documents=[DOC_A], videos=[], subtitles=[SUB_A])

    assert result.subtitles == (SubtitleSource(path=SUB_A, explicitly_provided=True, found_in_document=True),)


def test_subtitle_paths_deduplicated_before_read(
    scanner: ResourceScanner,
    doc_importer_mock: MagicMock,
    sub_importer_mock: MagicMock,
) -> None:
    doc_importer_mock.read.return_value = DocumentImportResult(
        valid_documents=(DOC_A,),
        invalid_documents=(),
        existing_videos=(),
        existing_subtitles=(SUB_A,),
        comments=(),
    )

    scanner.scan(documents=[DOC_A], videos=[], subtitles=[SUB_A])

    sub_importer_mock.read.assert_called_once_with((SUB_A,))


def test_comments_and_documents_flow_through(scanner: ResourceScanner, doc_importer_mock: MagicMock) -> None:
    doc_importer_mock.read.return_value = DocumentImportResult(
        valid_documents=(DOC_A,),
        invalid_documents=(DOC_BROKEN,),
        existing_videos=(),
        existing_subtitles=(),
        comments=(COMMENT, COMMENT, COMMENT),
    )

    result = scanner.scan(documents=[DOC_A, DOC_BROKEN], videos=[], subtitles=[])

    assert result.valid_documents == (DOC_A,)
    assert result.invalid_documents == (DOC_BROKEN,)
    assert result.comments == (COMMENT, COMMENT, COMMENT)
