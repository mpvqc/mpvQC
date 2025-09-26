# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable

import inject
from PySide6.QtCore import QObject, QRunnable, QThreadPool, QUrl, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import DocumentExportService, TypeMapperService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


class ExtendedExportJob(QRunnable):
    _exporter: DocumentExportService = inject.attr(DocumentExportService)
    _type_mapper: TypeMapperService = inject.attr(TypeMapperService)

    def __init__(self, document: QUrl, template: QUrl, error_callback: Callable[[str, int], None]):
        super().__init__()
        self._document = document
        self._template = template
        self._error_callback = error_callback

    @Slot()
    def run(self):
        document = self._type_mapper.map_url_to_path(self._document)
        template = self._type_mapper.map_url_to_path(self._template)

        if error := self._exporter.export(document, template):
            self._error_callback(error.message, error.line_nr)


# noinspection PyPep8Naming
@QmlElement
class MpvqcExtendedDocumentExporterPyObject(QObject):
    errorOccurred = Signal(str, int)  # params: message, line nr

    @Slot(QUrl, QUrl)
    def performExport(self, document: QUrl, template: QUrl) -> None:
        job = ExtendedExportJob(
            document=document,
            template=template,
            error_callback=self.errorOccurred.emit,
        )
        QThreadPool.globalInstance().start(job)
