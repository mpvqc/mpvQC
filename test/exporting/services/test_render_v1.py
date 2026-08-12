# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path
from typing import NamedTuple

import pytest

from mpvqc.exporting.services import render_v1
from mpvqc.shared import Comment

_CAPTURED_AT = datetime(2026, 1, 1, 0, 0, 0, tzinfo=UTC)


def test_renders_minimal_document(make_snapshot):
    content = render_v1(make_snapshot())

    assert content.endswith("\n")
    assert json.loads(content) == {
        "$schema": "https://raw.githubusercontent.com/mpvqc/mpvQC/main/docs/document-format/v1.json",
        "version": 1,
        "comments": [],
    }


def test_renders_full_document(make_snapshot):
    snapshot = make_snapshot(
        captured_at=_CAPTURED_AT,
        generator="mpvQC 0.9.0",
        video=Path.home() / "video.mkv",
        nickname="ಠ_ಠ",
        subtitles=[Path.home() / "video.de.ass", Path.home() / "video.en.srt"],
        comments=[
            Comment(time=0, comment_type="Translation", comment="My first comment"),
            Comment(time=(15 * 60 + 29) * 1000 + 340, comment_type="Spelling", comment=""),
        ],
        write_header_date=True,
        write_header_generator=True,
        write_header_nickname=True,
        write_header_video_path=True,
        write_header_subtitles=True,
    )

    document = json.loads(render_v1(snapshot))

    assert document == {
        "$schema": "https://raw.githubusercontent.com/mpvqc/mpvQC/main/docs/document-format/v1.json",
        "version": 1,
        "created_at": "2026-01-01T00:00:00Z",
        "generator": "mpvQC 0.9.0",
        "author": "ಠ_ಠ",
        "video": str((Path.home() / "video.mkv").resolve()),
        "subtitles": [str((Path.home() / "video.de.ass").resolve()), str((Path.home() / "video.en.srt").resolve())],
        "comments": [
            {"time": "00:00:00.000", "type": "Translation", "text": "My first comment"},
            {"time": "00:15:29.340", "type": "Spelling", "text": ""},
        ],
    }


def test_renders_keys_in_specification_order(make_snapshot):
    snapshot = make_snapshot(
        video="/path/to/video.mkv",
        nickname="lorem",
        subtitles=["/path/to/video.de.ass"],
        write_header_date=True,
        write_header_generator=True,
        write_header_nickname=True,
        write_header_video_path=True,
        write_header_subtitles=True,
    )

    document = json.loads(render_v1(snapshot))

    assert list(document) == [
        "$schema",
        "version",
        "created_at",
        "generator",
        "author",
        "video",
        "subtitles",
        "comments",
    ]


class OmissionCase(NamedTuple):
    name: str
    settings: dict
    absent_field: str


OMITTED_WHEN_EMPTY = [
    OmissionCase("blank author", {"write_header_nickname": True, "nickname": ""}, "author"),
    OmissionCase("no video", {"write_header_video_path": True, "video": None}, "video"),
    OmissionCase("no subtitles", {"write_header_subtitles": True, "subtitles": []}, "subtitles"),
]


@pytest.mark.parametrize("case", OMITTED_WHEN_EMPTY, ids=lambda case: case.name)
def test_omits_field_when_toggled_on_but_empty(make_snapshot, case):
    document = json.loads(render_v1(make_snapshot(**case.settings)))

    assert case.absent_field not in document


def test_renders_created_at_in_utc(make_snapshot):
    captured_at = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone(timedelta(hours=2)))

    document = json.loads(render_v1(make_snapshot(write_header_date=True, captured_at=captured_at)))

    assert document["created_at"] == "2026-01-01T10:00:00Z"
