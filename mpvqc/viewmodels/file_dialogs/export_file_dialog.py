# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later


import inject
from PySide6.QtCore import Property, QObject, QRunnable, QThreadPool, QUrl, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import DocumentExportService, ExportService, TypeMapperService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcExportFileDialogViewModel(QObject):
    _exporter: ExportService = inject.attr(ExportService)
    _document_exporter: DocumentExportService = inject.attr(DocumentExportService)
    _type_mapper: TypeMapperService = inject.attr(TypeMapperService)

    @Property(QUrl, constant=True, final=True)
    def filenameProposal(self) -> QUrl:
        path = self._document_exporter.generate_file_path_proposal()
        return self._type_mapper.map_path_to_url(path)

    @Slot(QUrl, QUrl)
    def export(self, document: QUrl, template: QUrl) -> None:
        def _job():
            self._document_exporter.export(
                file=self._type_mapper.map_url_to_path(document),
                template=self._type_mapper.map_url_to_path(template),
            )

        runnable = QRunnable.create(_job)
        QThreadPool.globalInstance().start(runnable)

    @Slot(QUrl)
    def save(self, document: QUrl) -> None:
        path = self._type_mapper.map_url_to_path(document)
        self._exporter.save(path)
