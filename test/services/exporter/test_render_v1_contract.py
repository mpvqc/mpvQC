# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import NamedTuple

import pytest
from jsonschema import Draft202012Validator, ValidationError

from mpvqc.services.exporter.documents.v1 import render_backup, render_v1
from mpvqc.services.importer.reader import read_documents

SCHEMA = Path(__file__).parents[3] / "docs" / "document-format" / "v1.json"
README = Path(__file__).parents[3] / "docs" / "document-format" / "README.md"


@pytest.fixture(scope="module")
def validator() -> Draft202012Validator:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


class ConformanceCase(NamedTuple):
    name: str
    settings: dict


CONFORMANCE_CASES = [
    ConformanceCase("minimal document", {}),
    ConformanceCase(
        "full document",
        {
            "video": "/path/to/video.mkv",
            "nickname": "lorem",
            "subtitles": ["/path/to/video.de.ass", "/path/to/video.en.srt"],
            "comments": [
                {"time": 0, "commentType": "Translation", "comment": "Lorem ipsum"},
                # Hebrew: type "Phrasing"
                {"time": (15 * 60 + 29) * 1000 + 340, "commentType": "ניסוח", "comment": ""},
            ],
            "write_header_date": True,
            "write_header_generator": True,
            "write_header_nickname": True,
            "write_header_video_path": True,
            "write_header_subtitles": True,
        },
    ),
]


@pytest.mark.parametrize("case", CONFORMANCE_CASES, ids=lambda case: case.name)
def test_rendered_documents_validate_against_schema(make_context, validator, case):
    context = make_context(generator="mpvQC 0.9.0", **case.settings)

    document = json.loads(render_v1(context))

    validator.validate(document)


class SchemaViolationCase(NamedTuple):
    name: str
    document: dict


SCHEMA_VIOLATIONS = [
    SchemaViolationCase("missing version", {"comments": []}),
    SchemaViolationCase("missing comments", {"version": 1}),
    SchemaViolationCase("unknown version", {"version": 2, "comments": []}),
    SchemaViolationCase("unknown top-level field", {"version": 1, "comments": [], "frame": 25}),
    SchemaViolationCase(
        "foreign $schema url", {"$schema": "https://example.com/v1.json", "version": 1, "comments": []}
    ),
    SchemaViolationCase("empty subtitles array", {"version": 1, "comments": [], "subtitles": []}),
    SchemaViolationCase(
        "created_at with offset", {"version": 1, "comments": [], "created_at": "2026-06-06T10:00:00+02:00"}
    ),
    SchemaViolationCase(
        "three-digit hours", {"version": 1, "comments": [{"time": "100:00:00.000", "type": "T", "text": ""}]}
    ),
    SchemaViolationCase(
        "centisecond time", {"version": 1, "comments": [{"time": "00:00:01.34", "type": "T", "text": ""}]}
    ),
    SchemaViolationCase(
        "unknown comment field",
        {"version": 1, "comments": [{"time": "00:00:01.000", "type": "T", "text": "", "frame": 25}]},
    ),
    SchemaViolationCase("comment missing text", {"version": 1, "comments": [{"time": "00:00:01.000", "type": "T"}]}),
    SchemaViolationCase(
        "text with newline", {"version": 1, "comments": [{"time": "00:00:01.000", "type": "T", "text": "a\nb"}]}
    ),
    SchemaViolationCase("empty type", {"version": 1, "comments": [{"time": "00:00:01.000", "type": "", "text": ""}]}),
]


@pytest.mark.parametrize("case", SCHEMA_VIOLATIONS, ids=lambda case: case.name)
def test_schema_rejects_contract_violations(validator, case):
    with pytest.raises(ValidationError):
        validator.validate(case.document)


def test_readme_example_validates_against_schema(validator):
    readme = README.read_text(encoding="utf-8")
    example = re.search(r"<!-- verified-by-tests: example-v1 -->\s*```json\n(.*?)```", readme, re.DOTALL)
    assert example is not None

    validator.validate(json.loads(example.group(1)))


def test_rendered_backup_validates_against_schema(make_context, validator):
    context = make_context(
        video="/path/to/video.mkv",
        comments=[{"time": 754321, "commentType": "Spelling", "comment": "Lorem ipsum"}],
    )

    document = json.loads(render_backup(context))

    validator.validate(document)


def test_backup_imports_losslessly(make_context, tmp_path):
    context = make_context(comments=[{"time": 754321, "commentType": "Spelling", "comment": "Lorem ipsum"}])

    document = tmp_path / "backup.json"
    document.write_text(render_backup(context), encoding="utf-8")

    result = read_documents([document])

    assert result.valid_documents == (document,)
    assert [(c.time, c.comment_type, c.comment) for c in result.comments] == [(754321, "Spelling", "Lorem ipsum")]


def test_exported_document_imports_losslessly(make_context, tmp_path):
    context = make_context(
        comments=[
            {"time": 0, "commentType": "Translation", "comment": "Lorem ipsum"},
            {"time": (15 * 60 + 29) * 1000 + 340, "commentType": "Spelling", "comment": ""},
            {"time": 359999 * 1000 + 999, "commentType": "Custom Type", "comment": "dolor sit amet"},
            # Hebrew: type "Phrasing", text "from right to left"
            {"time": 60 * 1000, "commentType": "ניסוח", "comment": "מימין לשמאל"},
            # CJK: type "subtitles", text "test" / "Chinese" / "Korean"
            {"time": 61 * 1000, "commentType": "字幕", "comment": "テスト 中文 한국어 😀🎬"},
        ]
    )

    document = tmp_path / "report.json"
    document.write_text(render_v1(context), encoding="utf-8")

    result = read_documents([document])

    assert result.valid_documents == (document,)
    assert [(c.time, c.comment_type, c.comment) for c in result.comments] == [
        (0, "Translation", "Lorem ipsum"),
        ((15 * 60 + 29) * 1000 + 340, "Spelling", ""),
        (359999 * 1000 + 999, "Custom Type", "dolor sit amet"),
        (60 * 1000, "Phrasing", "מימין לשמאל"),
        (61 * 1000, "字幕", "テスト 中文 한국어 😀🎬"),
    ]
