# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later


import inject
from PySide6.QtCore import Property, QObject, QRunnable, QThreadPool, QUrl, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import DocumentExportService, TypeMapperService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


class ExtendedExportJob(QRunnable):
    _exporter: DocumentExportService = inject.attr(DocumentExportService)
    _type_mapper: TypeMapperService = inject.attr(TypeMapperService)

    def __init__(self, document: QUrl, template: QUrl):
        super().__init__()
        self._document = document
        self._template = template

    @Slot()
    def run(self):
        document = self._type_mapper.map_url_to_path(self._document)
        template = self._type_mapper.map_url_to_path(self._template)
        self._exporter.export(document, template)


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcExportFileDialogViewModel(QObject):
    _exporter: DocumentExportService = inject.attr(DocumentExportService)
    _type_mapper: TypeMapperService = inject.attr(TypeMapperService)

    @Property(QUrl, constant=True, final=True)
    def filenameProposal(self) -> QUrl:
        path = self._exporter.generate_file_path_proposal()
        return self._type_mapper.map_path_to_url(path)

    @Slot(QUrl, QUrl)
    def export(self, document: QUrl, template: QUrl) -> None:
        job = ExtendedExportJob(
            document=document,
            template=template,
        )
        QThreadPool.globalInstance().start(job)
