# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

import inject
from PySide6.QtCore import QRunnable, QThreadPool

from .document_exporter import DocumentExportService
from .state import StateService


class ExportService:
    _document_exporter: DocumentExportService = inject.attr(DocumentExportService)
    _state: StateService = inject.attr(StateService)

    def save(self, document: Path) -> None:
        def _job():
            self._document_exporter.save(document)
            self._state.save(document)

        runnable = QRunnable.create(_job)
        QThreadPool.globalInstance().start(runnable)
