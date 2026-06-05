# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import NamedTuple

import pytest

from mpvqc.services.exporter.documents.v1 import render


def test_renders_minimal_document(configure_mocks):
    configure_mocks()

    content = render()

    assert content.endswith("\n")
    assert json.loads(content) == {
        "$schema": "https://raw.githubusercontent.com/mpvqc/mpvQC/main/docs/document-format/v1.json",
        "version": 1,
        "comments": [],
    }


def test_renders_full_document(configure_mocks, build_info_service_mock):
    build_info_service_mock.name = "mpvQC"
    build_info_service_mock.version = "0.9.0"
    configure_mocks(
        video=Path.home() / "video.mkv",
        nickname="ಠ_ಠ",
        subtitles=[Path.home() / "video.de.ass", Path.home() / "video.en.srt"],
        comments=[
            {"time": 0, "commentType": "Translation", "comment": "My first comment"},
            {"time": (15 * 60 + 29) * 1000 + 340, "commentType": "Spelling", "comment": ""},
        ],
        write_header_date=True,
        write_header_generator=True,
        write_header_nickname=True,
        write_header_video_path=True,
        write_header_subtitles=True,
    )

    document = json.loads(render())

    created_at = document.pop("created_at")
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", created_at)
    assert document == {
        "$schema": "https://raw.githubusercontent.com/mpvqc/mpvQC/main/docs/document-format/v1.json",
        "version": 1,
        "generator": "mpvQC 0.9.0",
        "author": "ಠ_ಠ",
        "video": str((Path.home() / "video.mkv").resolve()),
        "subtitles": [str((Path.home() / "video.de.ass").resolve()), str((Path.home() / "video.en.srt").resolve())],
        "comments": [
            {"time": "00:00:00.000", "type": "Translation", "text": "My first comment"},
            {"time": "00:15:29.340", "type": "Spelling", "text": ""},
        ],
    }


def test_renders_keys_in_specification_order(configure_mocks):
    configure_mocks(
        video="/path/to/video.mkv",
        nickname="lorem",
        subtitles=["/path/to/video.de.ass"],
        write_header_date=True,
        write_header_generator=True,
        write_header_nickname=True,
        write_header_video_path=True,
        write_header_subtitles=True,
    )

    document = json.loads(render())

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
def test_omits_field_when_toggled_on_but_empty(configure_mocks, case):
    configure_mocks(**case.settings)

    document = json.loads(render())

    assert case.absent_field not in document
