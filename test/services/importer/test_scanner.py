# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from mpvqc.datamodels import (
    Comment,
    DocumentImportResult,
    DocumentRejectionReason,
    RejectedDocument,
    SubtitleSource,
    VideoSource,
)
from mpvqc.services.importer import scanner

DOC_A = Path("/work/a.qc")
DOC_B = Path("/work/b.qc")
DOC_BROKEN = Path("/work/broken.qc")
VIDEO_A = Path("/movies/a.mp4")
VIDEO_B = Path("/movies/b.mkv")
SUB_A = Path("/work/a.en.srt")
SUB_B = Path("/work/a.ja.srt")
COMMENT = Comment(time=0, comment_type="", comment="")

EMPTY_DOCUMENT_RESULT = DocumentImportResult(
    valid_documents=(),
    rejected_documents=(),
    existing_videos=(),
    existing_subtitles=(),
    comments=(),
)


@pytest.fixture(autouse=True)
def read_documents_mock(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    mock = MagicMock(return_value=EMPTY_DOCUMENT_RESULT)
    monkeypatch.setattr(scanner, "read_documents", mock)
    return mock


@pytest.fixture(autouse=True)
def subtitle_videos_mock(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    mock = MagicMock(return_value=())
    monkeypatch.setattr(scanner, "find_videos_in_subtitles", mock)
    return mock


def test_explicit_video_gets_explicit_flag() -> None:
    result = scanner.scan(documents=[], videos=[VIDEO_A], subtitles=[])
    assert result.videos == (VideoSource(path=VIDEO_A, explicitly_provided=True),)


def test_doc_video_gets_doc_flag(read_documents_mock: MagicMock) -> None:
    read_documents_mock.return_value = DocumentImportResult(
        valid_documents=(DOC_A,),
        rejected_documents=(),
        existing_videos=(VIDEO_A,),
        existing_subtitles=(),
        comments=(),
    )

    result = scanner.scan(documents=[DOC_A], videos=[], subtitles=[])

    assert result.videos == (VideoSource(path=VIDEO_A, found_in_document=True),)


def test_subtitle_referenced_video_gets_subtitle_flag(subtitle_videos_mock: MagicMock) -> None:
    subtitle_videos_mock.return_value = (VIDEO_A,)

    result = scanner.scan(documents=[], videos=[], subtitles=[SUB_A])

    assert result.videos == (VideoSource(path=VIDEO_A, found_in_subtitle=True),)


def test_video_sources_merge_flags_when_path_collides(
    read_documents_mock: MagicMock,
    subtitle_videos_mock: MagicMock,
) -> None:
    read_documents_mock.return_value = DocumentImportResult(
        valid_documents=(DOC_A,),
        rejected_documents=(),
        existing_videos=(VIDEO_A,),
        existing_subtitles=(),
        comments=(),
    )
    subtitle_videos_mock.return_value = (VIDEO_A,)

    result = scanner.scan(documents=[DOC_A], videos=[VIDEO_A], subtitles=[SUB_A])

    assert result.videos == (
        VideoSource(path=VIDEO_A, explicitly_provided=True, found_in_document=True, found_in_subtitle=True),
    )


def test_explicit_subtitle_gets_explicit_flag() -> None:
    result = scanner.scan(documents=[], videos=[], subtitles=[SUB_A])
    assert result.subtitles == (SubtitleSource(path=SUB_A, explicitly_provided=True),)


def test_doc_subtitle_gets_doc_flag(read_documents_mock: MagicMock) -> None:
    read_documents_mock.return_value = DocumentImportResult(
        valid_documents=(DOC_A,),
        rejected_documents=(),
        existing_videos=(),
        existing_subtitles=(SUB_A,),
        comments=(),
    )

    result = scanner.scan(documents=[DOC_A], videos=[], subtitles=[])

    assert result.subtitles == (SubtitleSource(path=SUB_A, found_in_document=True),)


def test_subtitle_sources_merge_flags_when_path_collides(read_documents_mock: MagicMock) -> None:
    read_documents_mock.return_value = DocumentImportResult(
        valid_documents=(DOC_A,),
        rejected_documents=(),
        existing_videos=(),
        existing_subtitles=(SUB_A,),
        comments=(),
    )

    result = scanner.scan(documents=[DOC_A], videos=[], subtitles=[SUB_A])

    assert result.subtitles == (SubtitleSource(path=SUB_A, explicitly_provided=True, found_in_document=True),)


def test_subtitle_paths_deduplicated_before_video_detection(
    read_documents_mock: MagicMock,
    subtitle_videos_mock: MagicMock,
) -> None:
    read_documents_mock.return_value = DocumentImportResult(
        valid_documents=(DOC_A,),
        rejected_documents=(),
        existing_videos=(),
        existing_subtitles=(SUB_A,),
        comments=(),
    )

    scanner.scan(documents=[DOC_A], videos=[], subtitles=[SUB_A])

    subtitle_videos_mock.assert_called_once_with((SUB_A,))


def test_comments_and_documents_flow_through(read_documents_mock: MagicMock) -> None:
    read_documents_mock.return_value = DocumentImportResult(
        valid_documents=(DOC_A,),
        rejected_documents=(
            RejectedDocument(DOC_BROKEN, DocumentRejectionReason.INVALID),
            RejectedDocument(DOC_B, DocumentRejectionReason.UNSUPPORTED_VERSION),
        ),
        existing_videos=(),
        existing_subtitles=(),
        comments=(COMMENT, COMMENT, COMMENT),
    )

    result = scanner.scan(documents=[DOC_A, DOC_BROKEN], videos=[], subtitles=[])

    assert result.rejected_documents == (
        RejectedDocument(DOC_BROKEN, DocumentRejectionReason.INVALID),
        RejectedDocument(DOC_B, DocumentRejectionReason.UNSUPPORTED_VERSION),
    )
    assert result.comments == (COMMENT, COMMENT, COMMENT)
