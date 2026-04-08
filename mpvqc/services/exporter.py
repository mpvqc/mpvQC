# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

import inject
from PySide6.QtCore import QMutex, QMutexLocker, QThreadPool

from .document_exporter import DocumentExportService
from .state import StateService


class ExportService:
    _document_exporter = inject.attr(DocumentExportService)
    _state = inject.attr(StateService)

    def __init__(self) -> None:
        self._mutex = QMutex()

    def generate_file_path_proposal(self) -> Path:
        return self._document_exporter.generate_file_path_proposal()

    def export(self, document: Path, template: Path) -> None:
        def _job() -> None:
            with QMutexLocker(self._mutex):
                self._document_exporter.export(file=document, template=template)

        QThreadPool.globalInstance().start(_job)

    def save(self, document: Path) -> None:
        def _job() -> None:
            with QMutexLocker(self._mutex):
                self._document_exporter.save(document)
                self._state.save(document)

        QThreadPool.globalInstance().start(_job)
