# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.services import DocumentImporterService

DOCUMENT_INVALID = """\
erroneous_document
"""

DOCUMENT_WITH_EXISTING_VIDEO = """\
[FILE]
nick: some-weird-nick
path: {video_path}

[DATA]
[00:00:01][CommentType] Document 2 / Comment 1
[00:02:00][CommentType] Document 2 / Comment 2
[03:00:00][CommentType] Document 2 / Comment 3
"""

DOCUMENT_WITH_SPECIAL_COMMENT_TYPES = """\
[FILE]
nick: some-weird-nick
path: {video_path}

[DATA]
[00:00:11][A SPECIAL Comment-_-Type] Document 3 / Comment 1
[00:22:00][YOOOOO-comment-type] Document 3 / Comment 2
[33:00:00][ניסוח] Document 3 / Comment 3
"""

DOCUMENT_WITH_NONEXISTENT_VIDEO = """\
[FILE]
nick: some-weird-nick
path: {video_path}

[DATA]
[00:00:11][A SPECIAL Comment-_-Type] Document 4 / Comment 1
[00:22:00][YOOOOO-comment-type] Document 4 / Comment 2
[00:00:00][ניסוח] Document 4 / Comment 3
[33:00:00][ניסוח] Document 4 / Comment 4
"""


@pytest.fixture(autouse=True, scope="module")
def configure_inject(common_bindings_with):
    common_bindings_with()


@pytest.fixture(scope="session")
def video_file_existing_1(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("data")
    file_path = temp_dir / "an existing video with spaces.mp4"
    file_path.touch()
    return file_path


@pytest.fixture(scope="session")
def video_file_existing_2(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("data")
    file_path = temp_dir / "another existing video.mp4"
    file_path.touch()
    return file_path


@pytest.fixture(scope="session")
def video_file_not_existing(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("data")
    return temp_dir / "a not existing video with spaces.mp4"


@pytest.fixture(scope="session")
def document_invalid_1(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("data")
    file_path = temp_dir / "document_invalid_1.txt"
    file_path.write_text(DOCUMENT_INVALID, encoding="utf-8")
    return file_path


@pytest.fixture(scope="session")
def document_invalid_2(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("data")
    file_path = temp_dir / "document_invalid_2.txt"
    file_path.write_text(DOCUMENT_INVALID, encoding="utf-8")
    return file_path


@pytest.fixture(scope="session")
def document_with_existing_video_1(tmp_path_factory, video_file_existing_1):
    temp_dir = tmp_path_factory.mktemp("data")
    file_path = temp_dir / "document_with_video_1.txt"
    content = DOCUMENT_WITH_EXISTING_VIDEO.format(video_path=video_file_existing_1)
    file_path.write_text(content, encoding="utf-8")
    return file_path


@pytest.fixture(scope="session")
def document_with_existing_video_2(tmp_path_factory, video_file_existing_2):
    temp_dir = tmp_path_factory.mktemp("data")
    file_path = temp_dir / "document_with_video_2.txt"
    content = DOCUMENT_WITH_SPECIAL_COMMENT_TYPES.format(video_path=video_file_existing_2)
    file_path.write_text(content, encoding="utf-8")
    return file_path


@pytest.fixture(scope="session")
def document_with_nonexistent_video(tmp_path_factory, video_file_not_existing):
    temp_dir = tmp_path_factory.mktemp("data")
    file_path = temp_dir / "document_with_nonexistent_video.txt"
    content = DOCUMENT_WITH_NONEXISTENT_VIDEO.format(video_path=video_file_not_existing)
    file_path.write_text(content, encoding="utf-8")
    return file_path


@pytest.fixture(scope="session")
def service():
    return DocumentImporterService()
