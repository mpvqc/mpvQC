# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, QUrl, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import ImporterService, MimetypeProviderService, SettingsService, TypeMapperService

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcImportFileDialogViewModel(QObject):
    _importer = inject.attr(ImporterService)
    _mimetype_provider = inject.attr(MimetypeProviderService)
    _settings = inject.attr(SettingsService)
    _type_mapper = inject.attr(TypeMapperService)

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
        self._importer.open([], [self._type_mapper.map_url_to_path(url)], [])

    @Slot(list)
    def openDocuments(self, urls: list[QUrl]) -> None:
        self._importer.open(self._type_mapper.map_urls_to_path(urls), [], [])

    @Slot(list)
    def openSubtitles(self, urls: list[QUrl]) -> None:
        self._importer.open([], [], self._type_mapper.map_urls_to_path(urls))
