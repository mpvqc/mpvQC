# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from mpvqc.services.importer.reader import read_documents


def test_import_document_with_existing_video(
    document_with_existing_video_1,
    video_file_existing_1,
):
    result = read_documents([document_with_existing_video_1])

    assert not result.invalid_documents
    assert result.valid_documents
    assert len(result.existing_videos) == 1
    assert video_file_existing_1 in result.existing_videos


def test_import_document_with_nonexistent_video(
    document_with_nonexistent_video,
):
    result = read_documents([document_with_nonexistent_video])

    assert not result.invalid_documents
    assert result.valid_documents
    assert not result.existing_videos


def test_import_multiple_documents_video_detection(
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

    assert len(result.invalid_documents) == 1
    assert document_invalid_1 in result.invalid_documents
    assert len(result.valid_documents) == 3
    assert len(result.existing_videos) == 2
