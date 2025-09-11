# mpvQC
#
# Copyright (C) 2025 mpvQC developers
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
from PySide6.QtCore import QThreadPool, QUrl
from PySide6.QtTest import QSignalSpy

from mpvqc.pyobjects import MpvqcManagerBackendPyObject
from mpvqc.services import DocumentExportService, DocumentImporterService, TypeMapperService
from mpvqc.services.document_importer import DocumentImportResult


@pytest.fixture
def comment_model_mock():
    return MagicMock()


@pytest.fixture(autouse=True)
def mock_find_object(qt_app, comment_model_mock):
    with patch.object(qt_app, "find_object", return_value=comment_model_mock):
        yield


@pytest.fixture
def document_exporter_mock():
    return MagicMock(spec=DocumentExportService)


@pytest.fixture
def document_importer_mock():
    import_result = DocumentImportResult(valid_documents=[], invalid_documents=[], comments=[])
    mock = MagicMock(spec=DocumentImporterService)
    mock.read.return_value = import_result
    return mock


@pytest.fixture(autouse=True)
def configure_injections(document_exporter_mock, document_importer_mock, type_mapper):
    def config(binder: inject.Binder):
        binder.bind(DocumentExportService, document_exporter_mock)
        binder.bind(DocumentImporterService, document_importer_mock)
        binder.bind(TypeMapperService, type_mapper)

    inject.configure(config, clear=True)


def test_import(comment_model_mock):
    backend = MpvqcManagerBackendPyObject()
    signal_spy = QSignalSpy(backend.imported)

    backend.performImport(documents=[], videos=[], subtitles=[])
    QThreadPool.globalInstance().waitForDone()

    assert comment_model_mock.import_comments.called
    assert signal_spy.count() == 1


def test_reset(comment_model_mock):
    backend = MpvqcManagerBackendPyObject()
    signal_spy = QSignalSpy(backend.reset)

    backend.performReset()
    QThreadPool.globalInstance().waitForDone()

    assert comment_model_mock.clear_comments.called
    assert signal_spy.count() == 1


def test_save(document_exporter_mock):
    backend = MpvqcManagerBackendPyObject()
    signal_spy = QSignalSpy(backend.saved)

    document = QUrl("save-me-document")

    backend.performSave(document=document)
    QThreadPool.globalInstance().waitForDone()

    assert signal_spy.count() == 1
    assert signal_spy.at(0)[0] == document
