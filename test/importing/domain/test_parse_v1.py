# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from typing import NamedTuple

import pytest

from mpvqc.importing.domain import parse_v1


def identity(comment_type: str) -> str:
    return comment_type


def make_data(comments: list, **fields) -> dict:
    return {"comments": comments, **fields}


def test_parse_v1_comments():
    data = make_data(
        [
            {"time": "00:00:00.000", "type": "A SPECIAL Comment-_-Type", "text": "Comment 1"},
            {"time": "00:15:29.340", "type": "Phrasing", "text": "Comment 2"},
            {"time": "33:00:00.999", "type": "Translation", "text": ""},
        ]
    )

    result = parse_v1(data, identity)

    assert [(c.time, c.comment_type, c.comment) for c in result.comments] == [
        (0, "A SPECIAL Comment-_-Type", "Comment 1"),
        ((15 * 60 + 29) * 1000 + 340, "Phrasing", "Comment 2"),
        (33 * 3600 * 1000 + 999, "Translation", ""),
    ]


def test_parse_v1_translates_comment_type():
    data = make_data([{"time": "00:00:00.000", "type": "ניסוח", "text": "x"}])

    def translate(comment_type: str) -> str:
        return {"ניסוח": "Phrasing"}.get(comment_type, comment_type)

    result = parse_v1(data, translate)

    assert result.comments[0].comment_type == "Phrasing"


def test_parse_v1_video_and_subtitles():
    data = make_data([], video="/path/to/video.mkv", subtitles=["/a.ass", "/b.ass"])

    result = parse_v1(data, identity)

    assert result.video == Path("/path/to/video.mkv")
    assert result.subtitles == (Path("/a.ass"), Path("/b.ass"))


def test_parse_v1_without_video_or_subtitles():
    result = parse_v1(make_data([]), identity)

    assert result.video is None
    assert result.subtitles == ()


def test_parse_v1_ignores_unknown_fields():
    data = make_data(
        [{"time": "00:00:01.000", "type": "Translation", "text": "Comment"}],
        created_at="2026-06-05T16:24:13Z",
        generator="other-tool 1.0",
        author="lorem",
        custom_extension={"nested": True},
    )

    result = parse_v1(data, identity)

    assert len(result.comments) == 1


class InvalidCase(NamedTuple):
    name: str
    data: dict
    match: str


INVALID_V1_DATA = [
    InvalidCase(
        name="missing comments",
        data={},
        match="Expected 'comments'",
    ),
    InvalidCase(
        name="comments not a list",
        data={"comments": "00:00:01.000"},
        match="Expected 'comments'",
    ),
    InvalidCase(
        name="comment entry not an object",
        data=make_data(["not a dict"]),
        match="Expected a comment",
    ),
    InvalidCase(
        name="comment missing text",
        data=make_data([{"time": "00:00:01.000", "type": "T"}]),
        match="Expected a comment",
    ),
    InvalidCase(
        name="one-digit hours",
        data=make_data([{"time": "0:00:01.000", "type": "T", "text": "t"}]),
        match="Expected a comment",
    ),
    InvalidCase(
        name="centisecond time",
        data=make_data([{"time": "00:00:01.00", "type": "T", "text": "t"}]),
        match="Expected a comment",
    ),
    InvalidCase(
        name="minutes beyond 59",
        data=make_data([{"time": "00:75:01.000", "type": "T", "text": "t"}]),
        match="Expected a comment",
    ),
    InvalidCase(
        name="time as number",
        data=make_data([{"time": 1000, "type": "T", "text": "t"}]),
        match="Expected a comment",
    ),
    InvalidCase(
        name="video not a string",
        data=make_data([], video=123),
        match="Expected 'video'",
    ),
    InvalidCase(
        name="subtitle not a string",
        data=make_data([], subtitles=["/a.ass", 5]),
        match="Expected 'subtitles'",
    ),
]


@pytest.mark.parametrize("case", INVALID_V1_DATA, ids=lambda case: case.name)
def test_parse_v1_rejects_invalid_data(case: InvalidCase):
    with pytest.raises(ValueError, match=case.match):
        parse_v1(case.data, identity)
