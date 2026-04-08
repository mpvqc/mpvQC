# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later


import inject
from PySide6.QtCore import Property, QObject, QUrl, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import ExportService, TypeMapperService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcExportFileDialogViewModel(QObject):
    _exporter = inject.attr(ExportService)
    _type_mapper = inject.attr(TypeMapperService)

    @Property(QUrl, constant=True, final=True)
    def filenameProposal(self) -> QUrl:
        path = self._exporter.generate_file_path_proposal()
        return self._type_mapper.map_path_to_url(path)

    @Slot(QUrl, QUrl)
    def export(self, document: QUrl, template: QUrl) -> None:
        self._exporter.export(
            document=self._type_mapper.map_url_to_path(document),
            template=self._type_mapper.map_url_to_path(template),
        )

    @Slot(QUrl)
    def save(self, document: QUrl) -> None:
        path = self._type_mapper.map_url_to_path(document)
        self._exporter.save(path)
