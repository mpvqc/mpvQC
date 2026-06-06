# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import NamedTuple

import pytest

from mpvqc.datamodels import DocumentRejectionReason, RejectedDocument
from mpvqc.services.importer.reader import read_documents

DOCUMENT_FORMAT_README = Path(__file__).parents[4] / "docs" / "document-format" / "README.md"


def write_document(tmp_path, content: str):
    file_path = tmp_path / "document.json"
    file_path.write_text(content, encoding="utf-8")
    return file_path


def make_document(comments: list, **fields) -> str:
    return json.dumps({"version": 1, "comments": comments, **fields})


def test_import_v1_comments(tmp_path):
    document = write_document(
        tmp_path,
        make_document(
            [
                {"time": "00:00:00.000", "type": "A SPECIAL Comment-_-Type", "text": "Comment 1"},
                # Hebrew: type "Phrasing"
                {"time": "00:15:29.340", "type": "ניסוח", "text": "Comment 2"},
                {"time": "33:00:00.999", "type": "Translation", "text": ""},
            ]
        ),
    )

    result = read_documents([document])

    assert result.valid_documents == (document,)

    comment = result.comments[0]
    assert comment.time == 0
    assert comment.comment_type == "A SPECIAL Comment-_-Type"
    assert comment.comment == "Comment 1"

    comment = result.comments[1]
    assert comment.time == (15 * 60 + 29) * 1000 + 340
    assert comment.comment_type == "Phrasing"
    assert comment.comment == "Comment 2"

    comment = result.comments[2]
    assert comment.time == 33 * 3600 * 1000 + 999
    assert comment.comment_type == "Translation"
    assert not comment.comment


def test_import_v1_video_and_subtitles(tmp_path, video_file_existing_1):
    existing_subtitle = tmp_path / "existing.ass"
    existing_subtitle.touch()
    missing_subtitle = tmp_path / "missing.ass"

    document = write_document(
        tmp_path,
        make_document(
            [],
            video=str(video_file_existing_1),
            subtitles=[str(existing_subtitle), str(missing_subtitle)],
        ),
    )

    result = read_documents([document])

    assert result.valid_documents == (document,)
    assert result.existing_videos == (video_file_existing_1,)
    assert result.existing_subtitles == (existing_subtitle,)


def test_import_v1_minimal_document(tmp_path):
    document = write_document(tmp_path, make_document([]))

    result = read_documents([document])

    assert result.valid_documents == (document,)
    assert result.rejected_documents == ()
    assert result.comments == ()


def test_import_v1_ignores_unknown_fields(tmp_path):
    document = write_document(
        tmp_path,
        make_document(
            [{"time": "00:00:01.000", "type": "Translation", "text": "Comment", "frame": 25}],
            created_at="2026-06-05T16:24:13Z",
            generator="other-tool 1.0",
            author="lorem",
            custom_extension={"nested": True},
        ),
    )

    result = read_documents([document])

    assert result.valid_documents == (document,)
    assert len(result.comments) == 1


class InvalidDocumentCase(NamedTuple):
    name: str
    content: str


INVALID_DOCUMENTS = [
    InvalidDocumentCase("missing version", json.dumps({"comments": []})),
    InvalidDocumentCase("version as string", json.dumps({"version": "1", "comments": []})),
    InvalidDocumentCase("version as bool", json.dumps({"version": True, "comments": []})),
    InvalidDocumentCase("version as float", json.dumps({"version": 1.0, "comments": []})),
    InvalidDocumentCase("missing comments", json.dumps({"version": 1})),
    InvalidDocumentCase("comments not a list", json.dumps({"version": 1, "comments": "00:00:01.000"})),
    InvalidDocumentCase("comment entry not an object", make_document(["not a dict"])),
    InvalidDocumentCase("comment missing text", make_document([{"time": "00:00:01.000", "type": "T"}])),
    InvalidDocumentCase("one-digit hours", make_document([{"time": "0:00:01.000", "type": "T", "text": "t"}])),
    InvalidDocumentCase("centisecond time", make_document([{"time": "00:00:01.00", "type": "T", "text": "t"}])),
    InvalidDocumentCase("minutes beyond 59", make_document([{"time": "00:75:01.000", "type": "T", "text": "t"}])),
    InvalidDocumentCase("time as number", make_document([{"time": 1000, "type": "T", "text": "t"}])),
    InvalidDocumentCase("video not a string", make_document([], video=123)),
    InvalidDocumentCase("subtitle not a string", make_document([], subtitles=["/a.ass", 5])),
    InvalidDocumentCase("truncated json", '{"version": 1,'),
    InvalidDocumentCase("json array", "[]"),
    InvalidDocumentCase("json string", '"just a string"'),
]


@pytest.mark.parametrize("case", INVALID_DOCUMENTS, ids=lambda case: case.name)
def test_import_v1_invalid_documents(tmp_path, case):
    document = write_document(tmp_path, case.content)

    result = read_documents([document])

    assert result.valid_documents == ()
    assert result.rejected_documents == (RejectedDocument(document, DocumentRejectionReason.INVALID),)
    assert result.comments == ()


def test_import_v1_unsupported_version(tmp_path):
    document = write_document(tmp_path, json.dumps({"version": 999, "comments": []}))

    result = read_documents([document])

    assert result.valid_documents == ()
    assert result.rejected_documents == (RejectedDocument(document, DocumentRejectionReason.UNSUPPORTED_VERSION),)
    assert result.comments == ()


def test_import_readme_example_document(tmp_path):
    readme = DOCUMENT_FORMAT_README.read_text(encoding="utf-8")
    example = re.search(r"<!-- verified-by-tests: example-v1 -->\s*```json\n(.*?)```", readme, re.DOTALL)
    assert example is not None
    document = write_document(tmp_path, example.group(1))

    result = read_documents([document])

    assert result.valid_documents == (document,)
    assert len(result.comments) == 1

    comment = result.comments[0]
    assert comment.time == (15 * 60 + 29) * 1000 + 340
    assert comment.comment_type == "Translation"
    assert comment.comment == "Lorem ipsum dolor sit amet"


def test_import_mixed_formats(tmp_path, document_with_existing_video_1):
    v1_document = write_document(
        tmp_path,
        make_document([{"time": "00:00:01.000", "type": "Translation", "text": "From v1"}]),
    )

    result = read_documents([document_with_existing_video_1, v1_document])

    assert set(result.valid_documents) == {document_with_existing_video_1, v1_document}
    assert len(result.comments) == 4
