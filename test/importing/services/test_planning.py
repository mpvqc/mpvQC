# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from mpvqc.importing.domain import (
    DocumentRejectionReason,
    ErrorsPresent,
    FinishedPlan,
    LoadFoundVideo,
    RejectedDocument,
    SessionMerge,
    SubtitleSource,
    SubtitlesSkip,
    UnfinishedPlan,
    VideoSkip,
    VideoSource,
)
from mpvqc.importing.services import plan, scan

if TYPE_CHECKING:
    from pathlib import Path


def write_document(tmp_path: Path, name: str, content: str) -> Path:
    file_path = tmp_path / name
    file_path.write_text(content, encoding="utf-8")
    return file_path


def write_subtitle_referencing(tmp_path: Path, name: str, video: Path) -> Path:
    file_path = tmp_path / name
    file_path.write_text(f"[Script Info]\nVideo File: {video}\n", encoding="utf-8-sig")
    return file_path


def test_valid_document_composes_into_a_finished_plan(tmp_path: Path) -> None:
    document = tmp_path / "document.json"
    document.write_text(
        json.dumps({"version": 1, "comments": [{"time": "00:00:01.000", "type": "Phrasing", "text": "A comment"}]}),
        encoding="utf-8",
    )

    result = plan(
        [document],
        [],
        [],
        found_video_setting=LoadFoundVideo.ASK_EVERY_TIME,
        has_existing_comments=False,
        is_any_candidate_loaded=lambda _paths: False,
    )

    assert isinstance(result, FinishedPlan)
    assert len(result.comments) == 1
    assert result.comments[0].comment == "A comment"
    assert result.session == SessionMerge()
    assert result.video == VideoSkip()
    assert result.subtitles == SubtitlesSkip()


def test_invalid_document_composes_into_an_unfinished_plan(tmp_path: Path) -> None:
    document = tmp_path / "broken.json"
    document.write_text(json.dumps({"comments": []}), encoding="utf-8")

    result = plan(
        [document],
        [],
        [],
        found_video_setting=LoadFoundVideo.ASK_EVERY_TIME,
        has_existing_comments=False,
        is_any_candidate_loaded=lambda _paths: False,
    )

    assert isinstance(result, UnfinishedPlan)
    assert isinstance(result.errors, ErrorsPresent)
    assert result.errors.rejected_documents[0].path == document


def test_doc_video_gets_doc_flag(tmp_path: Path) -> None:
    video = tmp_path / "movie.mp4"
    video.touch()
    document = write_document(tmp_path, "a.qc", f"[FILE]\npath: {video}\n\n[DATA]\n")

    result = scan(documents=[document], videos=[], subtitles=[])

    assert result.videos == (VideoSource(path=video.resolve(), found_in_document=True),)


def test_subtitle_referenced_video_gets_subtitle_flag(tmp_path: Path) -> None:
    video = tmp_path / "movie.mp4"
    video.touch()
    subtitle = write_subtitle_referencing(tmp_path, "a.ass", video)

    result = scan(documents=[], videos=[], subtitles=[subtitle])

    assert result.videos == (VideoSource(path=video.resolve(), found_in_subtitle=True),)


def test_doc_subtitle_gets_doc_flag(tmp_path: Path) -> None:
    subtitle = tmp_path / "a.en.srt"
    subtitle.touch()
    document = write_document(tmp_path, "a.qc", f"[FILE]\nsubtitle: {subtitle}\n")

    result = scan(documents=[document], videos=[], subtitles=[])

    assert result.subtitles == (SubtitleSource(path=subtitle.resolve(), found_in_document=True),)


def test_comments_and_rejected_documents_flow_through(tmp_path: Path) -> None:
    valid = write_document(
        tmp_path,
        "valid.qc",
        "[FILE]\n\n[DATA]\n[00:00:01][Translation] one\n[00:00:02][Translation] two\n[00:00:03][Translation] three\n",
    )
    broken = write_document(tmp_path, "broken.qc", "erroneous_document\n")
    unsupported = write_document(tmp_path, "future.json", '{"version": 999, "comments": []}')

    result = scan(documents=[valid, broken, unsupported], videos=[], subtitles=[])

    assert result.rejected_documents == (
        RejectedDocument(broken, DocumentRejectionReason.INVALID),
        RejectedDocument(unsupported, DocumentRejectionReason.UNSUPPORTED_VERSION),
    )
    assert tuple(c.comment for c in result.comments) == ("one", "two", "three")


def test_video_sources_merge_when_spelling_differs(tmp_path: Path) -> None:
    real = tmp_path / "movie.mkv"
    real.write_bytes(b"")
    (tmp_path / "sub").mkdir()
    alias = tmp_path / "sub" / ".." / "movie.mkv"
    document = write_document(tmp_path, "a.qc", f"[FILE]\npath: {alias}\n\n[DATA]\n")

    result = scan(documents=[document], videos=[real], subtitles=[])

    assert result.videos == (VideoSource(path=real.resolve(), explicitly_provided=True, found_in_document=True),)


def test_subtitle_sources_merge_when_spelling_differs(tmp_path: Path) -> None:
    real = tmp_path / "subs.ass"
    real.write_text("", encoding="utf-8")
    (tmp_path / "sub").mkdir()
    alias = tmp_path / "sub" / ".." / "subs.ass"
    document = write_document(tmp_path, "a.qc", f"[FILE]\nsubtitle: {alias}\n")

    result = scan(documents=[document], videos=[], subtitles=[real])

    assert result.subtitles == (SubtitleSource(path=real.resolve(), explicitly_provided=True, found_in_document=True),)
