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

from pathlib import Path

import inject
from PySide6.QtCore import QObject, Slot, QUrl, Signal
from PySide6.QtQml import QmlElement

from mpvqc.services import DocumentExportService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcExtendedDocumentExporterPyObject(QObject):
    _exporter: DocumentExportService = inject.attr(DocumentExportService)

    exportErrorOccurred = Signal(str, int or None)

    @Slot(result=QUrl)
    def generate_file_path_proposal(self) -> QUrl:
        path = self._exporter.generate_file_path_proposal()
        return QUrl.fromLocalFile(str(path))

    @Slot(QUrl, QUrl)
    def export(self, template_path: QUrl, file_url: QUrl):
        file = Path(file_url.toLocalFile())
        template = Path(template_path.toLocalFile())

        error = self._exporter.export(file, template)

        if error:
            self.exportErrorOccurred.emit(error.message, error.line_nr)
