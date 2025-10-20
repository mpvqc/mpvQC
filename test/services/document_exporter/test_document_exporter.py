# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from pathlib import Path
from unittest.mock import MagicMock

import inject
import pytest
from jinja2 import TemplateError, TemplateSyntaxError
from PySide6.QtCore import QStandardPaths

from mpvqc.services import DocumentExportService, DocumentRenderService


@pytest.fixture
def document_renderer_service_mock() -> MagicMock:
    mock = MagicMock()

    def config(binder: inject.Binder):
        binder.bind(DocumentRenderService, mock)

    inject.configure(config, clear=True)
    return mock


@pytest.fixture
def service() -> DocumentExportService:
    return DocumentExportService()


@dataclass
class FilePathProposalTestSet:
    video: Path | None
    nickname: str | None
    expected: Path


HOME = Path.home()
MOVIES = Path(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.MoviesLocation))


@pytest.mark.parametrize(
    "case",
    [
        FilePathProposalTestSet(
            video=HOME / "Documents" / "my-movie.mp4",
            nickname="some-nickname",
            expected=HOME / "Documents" / "[QC]_my-movie_some-nickname.txt",
        ),
        FilePathProposalTestSet(
            video=HOME / "Documents" / "my-movie.mp4",
            nickname=None,
            expected=HOME / "Documents" / "[QC]_my-movie.txt",
        ),
        FilePathProposalTestSet(
            video=None,
            nickname="some-nickname",
            expected=MOVIES / "[QC]_untitled_some-nickname.txt",
        ),
        FilePathProposalTestSet(
            video=None,
            nickname=None,
            expected=MOVIES / "[QC]_untitled.txt",
        ),
    ],
)
def test_generates_file_path_proposals(case, make_mock, service):
    make_mock(video=case.video, nickname=case.nickname)
    actual = service.generate_file_path_proposal()
    assert actual == case.expected


def test_exports(service, document_renderer_service_mock, make_spy):
    error_spy = make_spy(service.export_error_occurred)

    template_mock = MagicMock()
    file_mock = MagicMock()

    service.export(file_mock, template_mock)
    assert error_spy.count() == 0
    assert template_mock.read_text.called
    assert file_mock.write_text.called
    assert document_renderer_service_mock.render.called

    document_renderer_service_mock.render.side_effect = TemplateSyntaxError(message="error", lineno=42)
    service.export(file_mock, template_mock)
    assert error_spy.count() == 1
    assert error_spy.at(invocation=0, argument=0) == "error"
    assert error_spy.at(invocation=0, argument=1) == 42

    document_renderer_service_mock.render.side_effect = TemplateError(message="error #2")
    service.export(file_mock, template_mock)
    assert error_spy.count() == 2
    assert error_spy.at(invocation=1, argument=0) == "error #2"
    assert error_spy.at(invocation=1, argument=1) == -1


def test_saves(service, document_renderer_service_mock):
    file_mock = MagicMock()

    service.save(file_mock)

    assert document_renderer_service_mock.render.called
    assert file_mock.write_text.called
