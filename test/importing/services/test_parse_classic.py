# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

from mpvqc.importing.services import parse_classic


def identity(comment_type: str) -> str:
    return comment_type


def test_parse_classic_extracts_video_path():
    content = "[FILE]\nnick: someone\npath: /videos/movie.mkv\n\n[DATA]\n"

    result = parse_classic(content, identity)

    assert result.video == Path("/videos/movie.mkv")


def test_parse_classic_without_video_path():
    content = "[FILE]\nnick: someone\n"

    result = parse_classic(content, identity)

    assert result.video is None


def test_parse_classic_extracts_subtitles():
    content = "[FILE]\nnick: someone\nsubtitle: /subs/one.ass\nsubtitle: /subs/two.ass\n"

    result = parse_classic(content, identity)

    assert result.subtitles == (Path("/subs/one.ass"), Path("/subs/two.ass"))


def test_parse_classic_without_subtitles():
    content = "[FILE]\nnick: someone\n"

    result = parse_classic(content, identity)

    assert result.subtitles == ()


DOCUMENT_WITH_MALFORMED_LINES = """\
[FILE]
nick: someone

[DATA]
[00:00:01][Translation] A valid comment
[0:00:02][Translation] one-digit hour is not a comment line
[00:00:03] missing the type bracket
random prose between comments
[00:00:04][Spelling] Another valid comment
"""


def test_parse_classic_skips_malformed_lines():
    result = parse_classic(DOCUMENT_WITH_MALFORMED_LINES, identity)

    assert [(c.time, c.comment_type, c.comment) for c in result.comments] == [
        (1 * 1000, "Translation", "A valid comment"),
        (4 * 1000, "Spelling", "Another valid comment"),
    ]


def test_parse_classic_converts_timestamps_to_milliseconds():
    content = (
        "[FILE]\n\n[DATA]\n[00:00:01][CommentType] one\n[00:02:00][CommentType] two\n[03:00:00][CommentType] three\n"
    )

    result = parse_classic(content, identity)

    assert [c.time for c in result.comments] == [1 * 1000, 120 * 1000, 10800 * 1000]


def test_parse_classic_keeps_special_comment_types_untranslated():
    content = "[FILE]\n\n[DATA]\n[00:00:11][A SPECIAL Comment-_-Type] one\n[00:22:00][YOOOOO-comment-type] two\n"

    result = parse_classic(content, identity)

    assert [c.comment_type for c in result.comments] == ["A SPECIAL Comment-_-Type", "YOOOOO-comment-type"]


def test_parse_classic_translates_comment_type():
    content = "[FILE]\n\n[DATA]\n[00:00:11][ניסוח] a comment\n"

    def translate(comment_type: str) -> str:
        return {"ניסוח": "Phrasing"}.get(comment_type, comment_type)

    result = parse_classic(content, translate)

    assert result.comments[0].comment_type == "Phrasing"
