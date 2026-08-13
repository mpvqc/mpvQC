# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import QObject, QUrl, Slot
from PySide6.QtQml import QmlElement

from mpvqc.importing.services import ImportService, classify_paths
from mpvqc.shared import map_urls_to_paths

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcImportDropAreaViewModel(QObject):
    _importer = inject.attr(ImportService)

    _ACCEPTED_FORMAT = "text/uri-list"

    @Slot(list, bool, result=bool)
    def canHandle(self, formats: list[str], has_urls: bool) -> bool:
        return self._ACCEPTED_FORMAT in formats and has_urls

    @Slot(list)
    def open(self, urls: list[QUrl]) -> None:
        paths = map_urls_to_paths(urls)
        classified = classify_paths(paths)
        self._importer.open(classified.documents, classified.videos, classified.subtitles)
