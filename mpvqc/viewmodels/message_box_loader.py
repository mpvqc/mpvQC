# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import QObject, Signal
from PySide6.QtQml import QmlElement

from mpvqc.services import DocumentExportService, ImporterService, QuitService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming
@QmlElement
class MpvqcMessageBoxLoaderViewModel(QObject):
    _document_exporter: DocumentExportService = inject.attr(DocumentExportService)
    _importer: ImporterService = inject.attr(ImporterService)
    _quit: QuitService = inject.attr(QuitService)

    erroneousDocumentsImported = Signal(list)
    exportErrorOccurred = Signal(str, int)
    confirmQuit = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._document_exporter.export_error_occurred.connect(self.exportErrorOccurred)
        self._importer.erroneous_documents_imported.connect(self.erroneousDocumentsImported)
        self._quit.confirmQuit.connect(self.confirmQuit)
