# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import NamedTuple

import pytest
from jsonschema import Draft202012Validator

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
def test_rendered_documents_validate_against_schema(
    configure_mocks, render_context, build_info_service_mock, validator, case
):
    build_info_service_mock.name = "mpvQC"
    build_info_service_mock.version = "0.9.0"
    configure_mocks(**case.settings)

    document = json.loads(render_v1(render_context))

    validator.validate(document)


def test_readme_example_validates_against_schema(validator):
    readme = README.read_text(encoding="utf-8")
    example = re.search(r"<!-- verified-by-tests: example-v1 -->\s*```json\n(.*?)```", readme, re.DOTALL)
    assert example is not None

    validator.validate(json.loads(example.group(1)))


def test_rendered_backup_validates_against_schema(configure_mocks, render_context, validator):
    configure_mocks(
        video="/path/to/video.mkv",
        comments=[{"time": 754321, "commentType": "Spelling", "comment": "Lorem ipsum"}],
    )

    document = json.loads(render_backup(render_context))

    validator.validate(document)


def test_backup_imports_losslessly(configure_mocks, render_context, tmp_path):
    configure_mocks(comments=[{"time": 754321, "commentType": "Spelling", "comment": "Lorem ipsum"}])

    document = tmp_path / "backup.json"
    document.write_text(render_backup(render_context), encoding="utf-8")

    result = read_documents([document])

    assert result.valid_documents == (document,)
    assert [(c.time, c.comment_type, c.comment) for c in result.comments] == [(754321, "Spelling", "Lorem ipsum")]


def test_exported_document_imports_losslessly(configure_mocks, render_context, tmp_path):
    configure_mocks(
        comments=[
            {"time": 0, "commentType": "Translation", "comment": "Lorem ipsum"},
            {"time": (15 * 60 + 29) * 1000 + 340, "commentType": "Spelling", "comment": ""},
            {"time": 359999 * 1000 + 999, "commentType": "Custom Type", "comment": "dolor sit amet"},
        ]
    )

    document = tmp_path / "report.json"
    document.write_text(render_v1(render_context), encoding="utf-8")

    result = read_documents([document])

    assert result.valid_documents == (document,)
    assert [(c.time, c.comment_type, c.comment) for c in result.comments] == [
        (0, "Translation", "Lorem ipsum"),
        ((15 * 60 + 29) * 1000 + 340, "Spelling", ""),
        (359999 * 1000 + 999, "Custom Type", "dolor sit amet"),
    ]
