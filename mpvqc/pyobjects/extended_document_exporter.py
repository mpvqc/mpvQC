#  mpvQC
#
#  Copyright (C) 2022 mpvQC developers
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
