# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later


def test_import_comments(
    service,
    document_with_existing_video_1,
):
    result = service.read([document_with_existing_video_1])

    assert len(result.comments) == 3

    comment = result.comments[0]
    assert comment.time == 1
    assert comment.comment_type == "CommentType"
    assert comment.comment == "Document 2 / Comment 1"

    comment = result.comments[1]
    assert comment.time == 120
    assert comment.comment_type == "CommentType"
    assert comment.comment == "Document 2 / Comment 2"

    comment = result.comments[2]
    assert comment.time == 10800
    assert comment.comment_type == "CommentType"
    assert comment.comment == "Document 2 / Comment 3"


def test_import_comments_with_special_types(
    service,
    document_with_existing_video_2,
):
    result = service.read([document_with_existing_video_2])

    assert len(result.comments) == 3

    comment = result.comments[0]
    assert comment.time == 11
    assert comment.comment_type == "A SPECIAL Comment-_-Type"
    assert comment.comment == "Document 3 / Comment 1"

    comment = result.comments[1]
    assert comment.time == 1320
    assert comment.comment_type == "YOOOOO-comment-type"
    assert comment.comment == "Document 3 / Comment 2"

    comment = result.comments[2]
    assert comment.time == 118800
    assert comment.comment_type == "Phrasing"
    assert comment.comment == "Document 3 / Comment 3"


def test_import_multiple_documents(
    service,
    document_invalid_1,
    document_with_existing_video_1,
    document_with_existing_video_2,
    document_with_nonexistent_video,
):
    result = service.read(
        [
            document_invalid_1,
            document_with_existing_video_1,
            document_with_existing_video_2,
            document_with_nonexistent_video,
        ]
    )

    assert len(result.comments) == 10
