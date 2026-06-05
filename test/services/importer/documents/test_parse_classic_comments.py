# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from mpvqc.services.importer.reader import read_documents

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


def test_import_skips_malformed_lines_and_keeps_document_valid(tmp_path):
    document = tmp_path / "document.txt"
    document.write_text(DOCUMENT_WITH_MALFORMED_LINES, encoding="utf-8")

    result = read_documents([document])

    assert result.valid_documents == (document,)
    assert result.rejected_documents == ()
    assert [(c.time, c.comment_type, c.comment) for c in result.comments] == [
        (1 * 1000, "Translation", "A valid comment"),
        (4 * 1000, "Spelling", "Another valid comment"),
    ]


def test_import_comments(
    document_with_existing_video_1,
):
    result = read_documents([document_with_existing_video_1])

    assert len(result.comments) == 3

    comment = result.comments[0]
    assert comment.time == 1 * 1000
    assert comment.comment_type == "CommentType"
    assert comment.comment == "Document 2 / Comment 1"

    comment = result.comments[1]
    assert comment.time == 120 * 1000
    assert comment.comment_type == "CommentType"
    assert comment.comment == "Document 2 / Comment 2"

    comment = result.comments[2]
    assert comment.time == 10800 * 1000
    assert comment.comment_type == "CommentType"
    assert comment.comment == "Document 2 / Comment 3"


def test_import_comments_with_special_types(
    document_with_existing_video_2,
):
    result = read_documents([document_with_existing_video_2])

    assert len(result.comments) == 3

    comment = result.comments[0]
    assert comment.time == 11 * 1000
    assert comment.comment_type == "A SPECIAL Comment-_-Type"
    assert comment.comment == "Document 3 / Comment 1"

    comment = result.comments[1]
    assert comment.time == 1320 * 1000
    assert comment.comment_type == "YOOOOO-comment-type"
    assert comment.comment == "Document 3 / Comment 2"

    comment = result.comments[2]
    assert comment.time == 118800 * 1000
    assert comment.comment_type == "Phrasing"
    assert comment.comment == "Document 3 / Comment 3"


def test_import_multiple_documents(
    document_invalid_1,
    document_with_existing_video_1,
    document_with_existing_video_2,
    document_with_nonexistent_video,
):
    result = read_documents(
        [
            document_invalid_1,
            document_with_existing_video_1,
            document_with_existing_video_2,
            document_with_nonexistent_video,
        ]
    )

    assert len(result.comments) == 10
