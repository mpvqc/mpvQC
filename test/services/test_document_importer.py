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

from unittest.mock import MagicMock, patch

import inject
import pytest

from mpvqc.services import DocumentImporter2Service, DocumentImporterService, ReverseTranslatorService

DOCUMENT_1 = """\
erroneous_document
"""

DOCUMENT_2 = """\
[FILE]
nick: some-weird-nick
path: /home/luffy/Videos/an existing video with spaces.mp4

[DATA]
[00:00:01][CommentType] Document 2 / Comment 1
[00:02:00][CommentType] Document 2 / Comment 2
[03:00:00][CommentType] Document 2 / Comment 3
"""

DOCUMENT_3 = """\
[FILE]
nick: some-weird-nick
path       :                 C:\\Videos\\mpvQC\\an existing video with spaces on Windows.mp4

[DATA]
[00:00:11][A SPECIAL Comment-_-Type] Document 3 / Comment 1
[00:22:00][YOOOOO-comment-type] Document 3 / Comment 2
[33:00:00][ניסוח] Document 3 / Comment 3
"""

DOCUMENT_4 = """\
[FILE]
nick: some-weird-nick
path       :                 /home/luffy/Videos/a not existing video with spaces.mp4

[DATA]
[00:00:11][A SPECIAL Comment-_-Type] Document 3 / Comment 1
[00:22:00][YOOOOO-comment-type] Document 3 / Comment 2
[00:00:00][ניסוח] Document 3 / Comment 3
[33:00:00][ניסוח] Document 3 / Comment 4
"""


@pytest.fixture(autouse=True, scope="module")
def configure_inject():
    def config(binder: inject.Binder):
        binder.bind(ReverseTranslatorService, ReverseTranslatorService())

    inject.configure(config, clear=True)


@pytest.fixture
def make_document_mock(tmp_path):
    def _make_document_mock(name, and_return_content):
        file = tmp_path / f"{name}.txt"
        file.write_text(and_return_content)
        return file

    return _make_document_mock


@pytest.fixture(scope="module")
def mocked_pathlib():
    def _mocked_is_file_function(mocked_path: MagicMock):
        file_path = mocked_path.call_args[0][0]
        return "an existing video" in file_path

    with patch("mpvqc.services.document_importer.Path") as mock:
        mock.return_value.is_file.side_effect = lambda: _mocked_is_file_function(mock)
        yield mock


@pytest.fixture(scope="module")
def service() -> DocumentImporterService:
    return DocumentImporterService()


@pytest.fixture(scope="module")
def service2() -> DocumentImporter2Service:
    return DocumentImporter2Service()


def test_import_invalid_documents(service, make_document_mock):
    path_1 = make_document_mock("path-1", and_return_content=DOCUMENT_1)
    path_2 = make_document_mock("path-2", and_return_content=DOCUMENT_1)

    result = service.read([path_1, path_2])

    assert not result.valid_documents
    assert result.invalid_documents
    assert "path-1" in f"{result.invalid_documents[0]}"
    assert "path-2" in f"{result.invalid_documents[1]}"


def test_import_valid_documents(service, make_document_mock, mocked_pathlib):
    path_1 = make_document_mock("path-1", and_return_content=DOCUMENT_2)
    result = service.read([path_1])
    assert not result.invalid_documents
    assert result.valid_documents
    assert result.existing_videos
    assert mocked_pathlib.call_args[0][0] == "/home/luffy/Videos/an existing video with spaces.mp4"
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

    path_2 = make_document_mock("path-2", and_return_content=DOCUMENT_3)
    result = service.read([path_2])
    assert not result.invalid_documents
    assert result.valid_documents
    assert result.existing_videos
    assert mocked_pathlib.call_args[0][0] == "C:\\Videos\\mpvQC\\an existing video with spaces on Windows.mp4"
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

    path_3 = make_document_mock("path-3", and_return_content=DOCUMENT_4)
    result = service.read([path_3])
    assert not result.invalid_documents
    assert result.valid_documents
    assert not result.existing_videos
    assert mocked_pathlib.call_args[0][0] == "/home/luffy/Videos/a not existing video with spaces.mp4"
    assert len(result.comments) == 4


def test_import_multiple_documents(service, make_document_mock, mocked_pathlib):
    path_1 = make_document_mock("path-1", and_return_content=DOCUMENT_1)
    path_2 = make_document_mock("path-2", and_return_content=DOCUMENT_2)
    path_3 = make_document_mock("path-3", and_return_content=DOCUMENT_3)
    path_4 = make_document_mock("path-4", and_return_content=DOCUMENT_4)

    result = service.read([path_1, path_2, path_3, path_4])

    assert len(result.invalid_documents) == 1
    assert "path-1" in f"{result.invalid_documents[0]}"
    assert len(result.valid_documents) == 3
    assert len(result.existing_videos) == 2
    assert len(result.comments) == 10


def test_import_invalid_documents2(service2, make_document_mock):
    path_1 = make_document_mock("path-1", and_return_content=DOCUMENT_1)
    path_2 = make_document_mock("path-2", and_return_content=DOCUMENT_1)

    result = service2.read([path_1, path_2])

    assert not result.valid_documents
    assert result.invalid_documents
    assert "path-1" in f"{result.invalid_documents[0]}"
    assert "path-2" in f"{result.invalid_documents[1]}"
