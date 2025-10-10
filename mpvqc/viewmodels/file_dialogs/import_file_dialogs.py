# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

import inject
from PySide6.QtCore import Property, QObject, QRunnable, QThreadPool, QUrl, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import ImporterService, MimetypeProviderService, SettingsService, TypeMapperService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


class ImportJob(QRunnable):
    _importer: ImporterService = inject.attr(ImporterService)

    def __init__(self, documents: list[Path], videos: list[Path], subtitles: list[Path]):
        super().__init__()
        self._documents = documents
        self._videos = videos
        self._subtitles = subtitles

    def run(self):
        self._importer.open(self._documents, self._videos, self._subtitles)


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcImportFileDialogViewModel(QObject):
    _importer: ImporterService = inject.attr(ImporterService)
    _mimetype_provider: MimetypeProviderService = inject.attr(MimetypeProviderService)
    _settings: SettingsService = inject.attr(SettingsService)
    _type_mapper: TypeMapperService = inject.attr(TypeMapperService)

    lastDirectoryVideoChanged = Signal(QUrl)
    lastDirectoryDocumentsChanged = Signal(QUrl)
    lastDirectorySubtitlesChanged = Signal(QUrl)

    @Property(str, constant=True, final=True)
    def videoFileGlobPattern(self) -> str:
        return self._mimetype_provider.video_file_glob_pattern

    @Property(str, constant=True, final=True)
    def subtitleFileGlobPattern(self) -> str:
        return self._mimetype_provider.subtitle_file_glob_pattern

    @Property(QUrl, notify=lastDirectoryVideoChanged)
    def lastDirectoryVideo(self) -> QUrl:
        return self._settings.last_directory_video

    @lastDirectoryVideo.setter
    def lastDirectoryVideo(self, value: QUrl) -> None:
        self._settings.last_directory_video = value

    @Property(QUrl, notify=lastDirectoryDocumentsChanged)
    def lastDirectoryDocuments(self) -> QUrl:
        return self._settings.last_directory_documents

    @lastDirectoryDocuments.setter
    def lastDirectoryDocuments(self, value: QUrl) -> None:
        self._settings.last_directory_documents = value

    @Property(QUrl, notify=lastDirectorySubtitlesChanged)
    def lastDirectorySubtitles(self) -> QUrl:
        return self._settings.last_directory_subtitles

    @lastDirectorySubtitles.setter
    def lastDirectorySubtitles(self, value: QUrl) -> None:
        self._settings.last_directory_subtitles = value

    @Slot(QUrl)
    def openVideo(self, url: QUrl) -> None:
        video_path = self._type_mapper.map_url_to_path(url)
        job = ImportJob(documents=[], videos=[video_path], subtitles=[])
        QThreadPool.globalInstance().start(job)

    @Slot(list)
    def openDocuments(self, urls: list[QUrl]) -> None:
        document_paths = self._type_mapper.map_urls_to_path(urls)
        job = ImportJob(documents=document_paths, videos=[], subtitles=[])
        QThreadPool.globalInstance().start(job)

    @Slot(list)
    def openSubtitles(self, urls: list[QUrl]) -> None:
        subtitle_paths = self._type_mapper.map_urls_to_path(urls)
        job = ImportJob(documents=[], videos=[], subtitles=subtitle_paths)
        QThreadPool.globalInstance().start(job)
