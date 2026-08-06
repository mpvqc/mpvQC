# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import NamedTuple

import pytest

from mpvqc.importing.domain import DocumentRejectionReason, RejectedDocument
from mpvqc.importing.services import read_documents

DOCUMENT_FORMAT_README = Path(__file__).parents[3] / "docs" / "document-format" / "README.md"


def write_classic_document(tmp_path: Path, name: str, content: str) -> Path:
    file_path = tmp_path / name
    file_path.write_text(content, encoding="utf-8")
    return file_path


def write_v1_document(tmp_path: Path, name: str, data: dict) -> Path:
    file_path = tmp_path / name
    file_path.write_text(json.dumps(data), encoding="utf-8")
    return file_path


def test_import_invalid_documents(tmp_path):
    document_1 = write_classic_document(tmp_path, "invalid_1.txt", "erroneous_document\n")
    document_2 = write_classic_document(tmp_path, "invalid_2.txt", "erroneous_document\n")

    result = read_documents([document_1, document_2])

    assert [r.path for r in result.rejected_documents] == [document_1, document_2]


def test_import_unreadable_documents(tmp_path):
    invalid_encoding = tmp_path / "invalid_encoding.txt"
    invalid_encoding.write_bytes(b"[FILE]\n\xff\xfe not valid utf-8")
    missing = tmp_path / "this_document_does_not_exist.txt"

    result = read_documents([invalid_encoding, missing])

    rejected_paths = [r.path for r in result.rejected_documents]
    assert invalid_encoding in rejected_paths
    assert missing in rejected_paths


def test_import_documents_with_utf8_bom(tmp_path):
    classic = tmp_path / "classic.txt"
    classic.write_text("[FILE]\n\n[DATA]\n[00:00:10] [Translation] first\n", encoding="utf-8-sig")
    v1 = tmp_path / "document.json"
    v1_content = '{"version": 1, "comments": [{"time": "00:00:20.000", "type": "Translation", "text": "second"}]}'
    v1.write_text(v1_content, encoding="utf-8-sig")

    result = read_documents([classic, v1])

    assert result.rejected_documents == ()
    assert len(result.comments) == 2


def test_import_translates_comment_type_from_the_current_language(tmp_path):
    # Hebrew: type "Spelling"
    document = write_classic_document(tmp_path, "document.txt", "[FILE]\n\n[DATA]\n[00:00:11][איות] a comment\n")

    result = read_documents([document])

    assert result.comments[0].comment_type == "Spelling"


def test_import_document_with_existing_video(tmp_path):
    video = tmp_path / "video.mp4"
    video.touch()
    document = write_classic_document(tmp_path, "document.txt", f"[FILE]\npath: {video}\n\n[DATA]\n")

    result = read_documents([document])

    assert result.rejected_documents == ()
    assert result.existing_videos == (video,)


def test_import_document_with_nonexistent_video(tmp_path):
    video = tmp_path / "missing.mp4"
    content = f"[FILE]\npath: {video}\n\n[DATA]\n[00:00:01][Translation] a comment\n"
    document = write_classic_document(tmp_path, "document.txt", content)

    result = read_documents([document])

    assert result.rejected_documents == ()
    assert result.existing_videos == ()
    assert len(result.comments) == 1


def test_import_document_with_existing_subtitle(tmp_path):
    subtitle = tmp_path / "subtitle.ass"
    subtitle.touch()
    document = write_classic_document(tmp_path, "document.txt", f"[FILE]\nsubtitle: {subtitle}\n")

    result = read_documents([document])

    assert result.rejected_documents == ()
    assert result.existing_subtitles == (subtitle,)


def test_import_document_with_nonexistent_subtitle(tmp_path):
    subtitle = tmp_path / "missing.ass"
    content = f"[FILE]\nsubtitle: {subtitle}\n\n[DATA]\n[00:00:01][Translation] a comment\n"
    document = write_classic_document(tmp_path, "document.txt", content)

    result = read_documents([document])

    assert result.rejected_documents == ()
    assert result.existing_subtitles == ()
    assert len(result.comments) == 1


def test_import_v1_video_and_subtitles(tmp_path):
    video = tmp_path / "video.mp4"
    video.touch()
    existing_subtitle = tmp_path / "existing.ass"
    existing_subtitle.touch()
    missing_subtitle = tmp_path / "missing.ass"
    document = write_v1_document(
        tmp_path,
        "document.json",
        {
            "version": 1,
            "video": str(video),
            "subtitles": [str(existing_subtitle), str(missing_subtitle)],
            "comments": [],
        },
    )

    result = read_documents([document])

    assert result.rejected_documents == ()
    assert result.existing_videos == (video,)
    assert result.existing_subtitles == (existing_subtitle,)


def test_import_multiple_documents_of_mixed_formats(tmp_path):
    invalid = write_classic_document(tmp_path, "invalid.txt", "erroneous_document\n")
    video = tmp_path / "video.mp4"
    video.touch()
    classic_document = write_classic_document(
        tmp_path,
        "classic.txt",
        f"[FILE]\npath: {video}\n\n[DATA]\n[00:00:01][Translation] one\n[00:00:02][Translation] two\n",
    )
    v1_document = write_v1_document(
        tmp_path,
        "document.json",
        {"version": 1, "comments": [{"time": "00:00:01.000", "type": "Translation", "text": "three"}]},
    )

    result = read_documents([invalid, classic_document, v1_document])

    assert [r.path for r in result.rejected_documents] == [invalid]
    assert result.existing_videos == (video,)
    assert len(result.comments) == 3


class InvalidJsonCase(NamedTuple):
    name: str
    content: str


INVALID_JSON_DOCUMENTS = [
    InvalidJsonCase("missing version", json.dumps({"comments": []})),
    InvalidJsonCase("version as string", json.dumps({"version": "1", "comments": []})),
    InvalidJsonCase("version as bool", json.dumps({"version": True, "comments": []})),
    InvalidJsonCase("version as float", json.dumps({"version": 1.0, "comments": []})),
    InvalidJsonCase("truncated json", '{"version": 1,'),
    InvalidJsonCase("json array", "[]"),
    InvalidJsonCase("json string", '"just a string"'),
]


@pytest.mark.parametrize("case", INVALID_JSON_DOCUMENTS, ids=lambda case: case.name)
def test_import_rejects_documents_with_malformed_version(tmp_path, case):
    document = tmp_path / "document.json"
    document.write_text(case.content, encoding="utf-8")

    result = read_documents([document])

    assert result.rejected_documents == (RejectedDocument(document, DocumentRejectionReason.INVALID),)


def test_import_unsupported_version(tmp_path):
    document = write_v1_document(tmp_path, "document.json", {"version": 999, "comments": []})

    result = read_documents([document])

    assert result.rejected_documents == (RejectedDocument(document, DocumentRejectionReason.UNSUPPORTED_VERSION),)


def test_import_rejects_malformed_v1_document(tmp_path):
    document = write_v1_document(tmp_path, "document.json", {"version": 1})

    result = read_documents([document])

    assert result.rejected_documents == (RejectedDocument(document, DocumentRejectionReason.INVALID),)


def test_import_readme_example_document(tmp_path):
    readme = DOCUMENT_FORMAT_README.read_text(encoding="utf-8")
    example = re.search(r"<!-- verified-by-tests: example-v1 -->\s*```json\n(.*?)```", readme, re.DOTALL)
    assert example is not None
    document = tmp_path / "document.json"
    document.write_text(example.group(1), encoding="utf-8")

    result = read_documents([document])

    assert result.rejected_documents == ()
    assert len(result.comments) == 1

    comment = result.comments[0]
    assert comment.time == (15 * 60 + 29) * 1000 + 340
    assert comment.comment_type == "Translation"
    assert comment.comment == "Lorem ipsum dolor sit amet"
