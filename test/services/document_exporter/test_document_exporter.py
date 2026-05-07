# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from jinja2 import TemplateError, TemplateSyntaxError
from PySide6.QtCore import QStandardPaths

from mpvqc.services import DocumentExportService


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
def test_generates_file_path_proposals(case, configure_mocks, service):
    configure_mocks(video=case.video, nickname=case.nickname)
    actual = service.generate_file_path_proposal()
    assert actual == case.expected


def test_export_succeeds(service, document_render_service_mock, make_spy):
    error_spy = make_spy(service.export_error_occurred)
    template_mock = MagicMock()
    file_mock = MagicMock()

    service.export(file_mock, template_mock)

    assert error_spy.count() == 0
    assert template_mock.read_text.called
    assert document_render_service_mock.render.called
    assert file_mock.write_text.called


@pytest.mark.parametrize(
    ("render_error", "expected_lineno"),
    [
        (TemplateSyntaxError(message="error", lineno=42), 42),
        (TemplateError(message="error"), -1),
    ],
)
def test_export_signals_on_render_failure(
    service, document_render_service_mock, make_spy, render_error, expected_lineno
):
    error_spy = make_spy(service.export_error_occurred)
    document_render_service_mock.render.side_effect = render_error

    service.export(MagicMock(), MagicMock())

    assert error_spy.count() == 1
    assert error_spy.at(invocation=0, argument=0) == "error"
    assert error_spy.at(invocation=0, argument=1) == expected_lineno


@pytest.mark.parametrize(
    "read_error",
    [
        UnicodeDecodeError("utf-8", b"\xff", 0, 1, "invalid"),
        FileNotFoundError("template gone"),
    ],
)
def test_export_signals_on_template_read_failure(service, make_spy, read_error):
    error_spy = make_spy(service.export_error_occurred)
    template_mock = MagicMock()
    template_mock.read_text.side_effect = read_error

    service.export(MagicMock(), template_mock)

    assert error_spy.count() == 1
    assert error_spy.at(invocation=0, argument=1) == -1


def test_export_signals_on_write_failure(service, document_render_service_mock, make_spy):
    error_spy = make_spy(service.export_error_occurred)
    file_mock = MagicMock()
    file_mock.write_text.side_effect = PermissionError("read-only target")

    service.export(file_mock, MagicMock())

    assert error_spy.count() == 1
    assert error_spy.at(invocation=0, argument=1) == -1
    assert document_render_service_mock.render.called


def test_save_succeeds(service, document_render_service_mock, make_spy):
    error_spy = make_spy(service.export_error_occurred)
    file_mock = MagicMock()

    service.save(file_mock)

    assert document_render_service_mock.render.called
    assert file_mock.write_text.called
    assert error_spy.count() == 0


def test_save_signals_on_write_failure(service, document_render_service_mock, make_spy):
    error_spy = make_spy(service.export_error_occurred)
    file_mock = MagicMock()
    file_mock.write_text.side_effect = PermissionError("read-only target")

    service.save(file_mock)

    assert error_spy.count() == 1
    assert error_spy.at(invocation=0, argument=1) == -1
    assert document_render_service_mock.render.called
