# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later


import inject
from PySide6.QtCore import Property, QObject, QUrl, Slot
from PySide6.QtQml import QmlElement

from mpvqc.exporting.services import ExportService
from mpvqc.shared import map_path_to_url, map_url_to_path

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcExportFileDialogViewModel(QObject):
    _exporter = inject.attr(ExportService)

    @Property(QUrl, constant=True, final=True)
    def filenameProposal(self) -> QUrl:
        path = self._exporter.generate_file_path_proposal("json")
        return map_path_to_url(path)

    @Property(QUrl, constant=True, final=True)
    def classicFilenameProposal(self) -> QUrl:
        path = self._exporter.generate_file_path_proposal("txt")
        return map_path_to_url(path)

    @Property(QUrl, constant=True, final=True)
    def customFilenameProposal(self) -> QUrl:
        path = self._exporter.generate_file_path_proposal("txt")
        return map_path_to_url(path)

    @Slot(QUrl)
    def save(self, document: QUrl) -> None:
        path = map_url_to_path(document)
        self._exporter.save(path)

    @Slot(QUrl)
    def exportClassic(self, document: QUrl) -> None:
        path = map_url_to_path(document)
        self._exporter.export_classic(path)

    @Slot(QUrl, QUrl)
    def exportCustom(self, document: QUrl, template: QUrl) -> None:
        self._exporter.export_custom(
            document=map_url_to_path(document),
            template=map_url_to_path(template),
        )
