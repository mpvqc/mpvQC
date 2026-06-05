# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later


def test_import_document_with_existing_video(
    service,
    document_with_existing_video_1,
    video_file_existing_1,
):
    result = service.read([document_with_existing_video_1])

    assert not result.invalid_documents
    assert result.valid_documents
    assert len(result.existing_videos) == 1
    assert video_file_existing_1 in result.existing_videos


def test_import_document_with_nonexistent_video(
    service,
    document_with_nonexistent_video,
):
    result = service.read([document_with_nonexistent_video])

    assert not result.invalid_documents
    assert result.valid_documents
    assert not result.existing_videos


def test_import_multiple_documents_video_detection(
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

    assert len(result.invalid_documents) == 1
    assert document_invalid_1 in result.invalid_documents
    assert len(result.valid_documents) == 3
    assert len(result.existing_videos) == 2
