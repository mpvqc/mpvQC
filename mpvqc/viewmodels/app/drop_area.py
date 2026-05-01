# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import typing

import inject
from PySide6.QtCore import QObject, QRunnable, QThreadPool, QUrl, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import ImporterService, MimetypeProviderService, TypeMapperService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


class ImportJob(QRunnable):
    _importer = inject.attr(ImporterService)
    _mimetype_provider = inject.attr(MimetypeProviderService)
    _type_mapper = inject.attr(TypeMapperService)

    def __init__(self, urls: list[QUrl]) -> None:
        super().__init__()
        self._urls = urls

    @typing.override
    def run(self) -> None:
        subtitle_extensions = [f".{ext}" for ext in self._mimetype_provider.SUBTITLE_FILE_EXTENSIONS]

        documents = []
        subtitles = []
        videos = []

        for url in self._urls:
            path = self._type_mapper.map_url_to_path(url)
            if path.suffix == ".txt":
                documents.append(path)
            elif path.suffix in subtitle_extensions:
                subtitles.append(path)
            else:
                videos.append(path)

        self._importer.open(documents, videos, subtitles)


# noinspection PyPep8Naming
@QmlElement
class MpvqcDropAreaViewModel(QObject):
    _ACCEPTED_FORMAT = "text/uri-list"

    @Slot(list, bool, result=bool)
    def canHandle(self, formats: list[str], has_urls: bool) -> bool:
        return self._ACCEPTED_FORMAT in formats and has_urls

    @Slot(list)
    def open(self, urls: list[QUrl]) -> None:
        job = ImportJob(urls)
        QThreadPool.globalInstance().start(job)
