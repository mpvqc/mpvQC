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

from mpvqc.exporting.services import render_backup, render_v1
from mpvqc.importing.services import read_documents
from mpvqc.shared import Comment

SCHEMA = Path(__file__).parents[2] / "docs" / "document-format" / "v1.json"
README = Path(__file__).parents[2] / "docs" / "document-format" / "README.md"


@pytest.fixture(scope="module")
def validator() -> Draft202012Validator:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


class ConformanceCase(NamedTuple):
    name: str
    settings: dict[str, str | bool | list[str] | list[Comment]]


CONFORMANCE_CASES = [
    ConformanceCase(
        name="minimal document",
        settings={},
    ),
    ConformanceCase(
        name="full document",
        settings={
            "video": "/path/to/video.mkv",
            "nickname": "lorem",
            "subtitles": ["/path/to/video.de.ass", "/path/to/video.en.srt"],
            "comments": [
                Comment(time=0, comment_type="Translation", comment="Lorem ipsum"),
                # Hebrew: type "Phrasing"
                Comment(time=(15 * 60 + 29) * 1000 + 340, comment_type="ניסוח", comment=""),
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
def test_rendered_documents_validate_against_schema(make_snapshot, validator, case: ConformanceCase):
    snapshot = make_snapshot(generator="mpvQC 0.9.0", **case.settings)

    document = json.loads(render_v1(snapshot))

    validator.validate(document)


class SchemaViolationCase(NamedTuple):
    name: str
    document: dict[str, str | int | list[str] | list[dict[str, str | int]]]


SCHEMA_VIOLATIONS = [
    SchemaViolationCase(
        name="missing version",
        document={"comments": []},
    ),
    SchemaViolationCase(
        name="missing comments",
        document={"version": 1},
    ),
    SchemaViolationCase(
        name="unknown version",
        document={"version": 2, "comments": []},
    ),
    SchemaViolationCase(
        name="unknown top-level field",
        document={"version": 1, "comments": [], "frame": 25},
    ),
    SchemaViolationCase(
        name="foreign $schema url",
        document={"$schema": "https://example.com/v1.json", "version": 1, "comments": []},
    ),
    SchemaViolationCase(
        name="empty subtitles array",
        document={"version": 1, "comments": [], "subtitles": []},
    ),
    SchemaViolationCase(
        name="created_at with offset",
        document={"version": 1, "comments": [], "created_at": "2026-06-06T10:00:00+02:00"},
    ),
    SchemaViolationCase(
        name="three-digit hours",
        document={"version": 1, "comments": [{"time": "100:00:00.000", "type": "T", "text": ""}]},
    ),
    SchemaViolationCase(
        name="centisecond time",
        document={"version": 1, "comments": [{"time": "00:00:01.34", "type": "T", "text": ""}]},
    ),
    SchemaViolationCase(
        name="unknown comment field",
        document={"version": 1, "comments": [{"time": "00:00:01.000", "type": "T", "text": "", "frame": 25}]},
    ),
    SchemaViolationCase(
        name="comment missing text",
        document={"version": 1, "comments": [{"time": "00:00:01.000", "type": "T"}]},
    ),
    SchemaViolationCase(
        name="text with newline",
        document={"version": 1, "comments": [{"time": "00:00:01.000", "type": "T", "text": "a\nb"}]},
    ),
    SchemaViolationCase(
        name="empty type",
        document={"version": 1, "comments": [{"time": "00:00:01.000", "type": "", "text": ""}]},
    ),
]


@pytest.mark.parametrize("case", SCHEMA_VIOLATIONS, ids=lambda case: case.name)
def test_schema_rejects_contract_violations(validator, case: SchemaViolationCase):
    with pytest.raises(ValidationError):
        validator.validate(case.document)


def test_readme_example_validates_against_schema(validator):
    readme = README.read_text(encoding="utf-8")
    example = re.search(r"<!-- verified-by-tests: example-v1 -->\s*```json\n(.*?)```", readme, re.DOTALL)
    assert example is not None

    validator.validate(json.loads(example.group(1)))


def test_rendered_backup_validates_against_schema(make_snapshot, validator):
    snapshot = make_snapshot(
        video="/path/to/video.mkv",
        comments=[Comment(time=754321, comment_type="Spelling", comment="Lorem ipsum")],
    )

    document = json.loads(render_backup(snapshot))

    validator.validate(document)


def test_backup_imports_losslessly(make_snapshot, tmp_path):
    snapshot = make_snapshot(comments=[Comment(time=754321, comment_type="Spelling", comment="Lorem ipsum")])

    document = tmp_path / "backup.json"
    document.write_text(render_backup(snapshot), encoding="utf-8")

    result = read_documents((document,))

    assert result.rejected_documents == ()
    assert [(c.time, c.comment_type, c.comment) for c in result.comments] == [(754321, "Spelling", "Lorem ipsum")]


def test_exported_document_imports_losslessly(make_snapshot, tmp_path):
    snapshot = make_snapshot(
        comments=[
            Comment(time=0, comment_type="Translation", comment="Lorem ipsum"),
            Comment(time=(15 * 60 + 29) * 1000 + 340, comment_type="Spelling", comment=""),
            Comment(time=359999 * 1000 + 999, comment_type="Custom Type", comment="dolor sit amet"),
            # Hebrew: type "Phrasing", text "from right to left"
            Comment(time=60 * 1000, comment_type="ניסוח", comment="מימין לשמאל"),
            # CJK: type "subtitles", text "test" / "Chinese" / "Korean"
            Comment(time=61 * 1000, comment_type="字幕", comment="テスト 中文 한국어 😀🎬"),
        ]
    )

    document = tmp_path / "report.json"
    document.write_text(render_v1(snapshot), encoding="utf-8")

    result = read_documents((document,))

    assert result.rejected_documents == ()
    assert [(c.time, c.comment_type, c.comment) for c in result.comments] == [
        (0, "Translation", "Lorem ipsum"),
        ((15 * 60 + 29) * 1000 + 340, "Spelling", ""),
        (359999 * 1000 + 999, "Custom Type", "dolor sit amet"),
        (60 * 1000, "Phrasing", "מימין לשמאל"),
        (61 * 1000, "字幕", "テスト 中文 한국어 😀🎬"),
    ]
