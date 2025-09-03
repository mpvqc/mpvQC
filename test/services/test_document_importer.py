# mpvQC
#
# Copyright (C) 2024
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pathlib import Path

import inject
import pytest

from mpvqc.services import DocumentImporterService, ReverseTranslatorService

DOCUMENT_1 = """\
erroneous_document
"""

DOCUMENT_2 = """\
[FILE]
nick: some-weird-nick
path       :                 {video}

[DATA]
[00:00:11][A SPECIAL Comment-_-Type] Document 2 / Comment 1
[00:22:00][YOOOOO-comment-type] Document 2 / Comment 2
[33:00:00][ניסוח] Document 2 / Comment 3
"""

DOCUMENT_3 = """\
[FILE]
path       : {video}

[DATA]
[99:99:99][End] The end
"""


@pytest.fixture(autouse=True, scope="module")
def configure_inject():
    def config(binder: inject.Binder):
        binder.bind(ReverseTranslatorService, ReverseTranslatorService())

    inject.configure(config, clear=True)


@pytest.fixture
def video_exists(tmp_path) -> Path:
    video = tmp_path / "video.mp4"
    video.touch(exist_ok=True)
    return video


@pytest.fixture
def video_not_exists(tmp_path) -> Path:
    return tmp_path / "no-video.mp4"


@pytest.fixture
def make_document_mock(tmp_path):
    def _make_document_mock(name, content, video=None):
        file = tmp_path / f"{name}.txt"
        if video is not None:
            file.write_text(content.format(video=f"{video.resolve()}"))
        else:
            file.write_text(content)
        return file

    return _make_document_mock


@pytest.fixture(scope="module")
def service() -> DocumentImporterService:
    return DocumentImporterService()


def test_import_invalid_document(service, make_document_mock):
    name = "path-1"
    path = make_document_mock(name, content=DOCUMENT_1)
    result = service.read([path])
    assert not result.valid_documents
    assert result.invalid_documents
    assert name in f"{result.invalid_documents[0]}"


def test_import_valid_document(service, make_document_mock, video_exists, video_not_exists):
    name = "path-1"
    path = make_document_mock(name, content=DOCUMENT_2, video=video_exists)

    result = service.read([path])

    assert not result.invalid_documents

    assert result.valid_documents
    assert name in f"{result.valid_documents[0].path}"
    assert result.valid_documents[0].video_exists
    assert result.valid_documents[0].video_path == video_exists

    assert len(result.comments) == 3
    comment = result.comments[0]
    assert comment.time == 11
    assert comment.comment_type == "A SPECIAL Comment-_-Type"
    assert comment.comment == "Document 2 / Comment 1"
    comment = result.comments[1]
    assert comment.time == 1320
    assert comment.comment_type == "YOOOOO-comment-type"
    assert comment.comment == "Document 2 / Comment 2"
    comment = result.comments[2]
    assert comment.time == 118800
    assert comment.comment_type == "Phrasing"
    assert comment.comment == "Document 2 / Comment 3"


def test_import_valid_document_with_non_existing_video(service, make_document_mock, video_not_exists):
    path = make_document_mock("path-1", content=DOCUMENT_3, video=video_not_exists)

    result = service.read([path])

    assert result.valid_documents
    assert not result.valid_documents[0].video_exists
    assert result.valid_documents[0].video_path == video_not_exists


def test_import_multiple_documents(service, make_document_mock):
    path_1 = make_document_mock("path-1", content=DOCUMENT_1)
    path_2 = make_document_mock("path-2", content=DOCUMENT_2)
    path_3 = make_document_mock("path-3", content=DOCUMENT_3)

    result = service.read([path_1, path_2, path_3])

    assert len(result.invalid_documents) == 1
    assert len(result.valid_documents) == 2
    assert len(result.comments) == 4
