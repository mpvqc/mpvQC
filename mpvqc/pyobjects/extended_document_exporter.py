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

import inject
from PySide6.QtCore import QObject, Slot, QUrl, Signal
from PySide6.QtQml import QmlElement

from mpvqc.services import DocumentExportService, TypeMapperService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcExtendedDocumentExporterPyObject(QObject):
    _exporter: DocumentExportService = inject.attr(DocumentExportService)
    _type_mapper: TypeMapperService = inject.attr(TypeMapperService)

    exportErrorOccurred = Signal(str, int or None)

    @Slot(result=QUrl)
    def generate_file_path_proposal(self) -> QUrl:
        path = self._exporter.generate_file_path_proposal()
        return self._type_mapper.map_path_to_url(path)

    @Slot(QUrl, QUrl)
    def export(self, template_url: QUrl, file_url: QUrl):
        file = self._type_mapper.map_url_to_path(file_url)
        template = self._type_mapper.map_url_to_path(template_url)

        error = self._exporter.export(file, template)

        if error:
            self.exportErrorOccurred.emit(error.message, error.line_nr)
