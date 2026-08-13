# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QMimeDatabase, QObject, QUrl, Slot
from PySide6.QtQml import QmlElement

from mpvqc.importing.domain import DOCUMENT_EXTENSIONS, SUBTITLE_EXTENSIONS
from mpvqc.importing.services import ImportService, ImportSettingsService
from mpvqc.shared import map_path_to_url, map_url_to_path

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1

VIDEO_EXTENSIONS: frozenset[str] = frozenset(
    {
        ".avi",
        ".mkv",
        ".mp4",
    }
)


def _video_file_glob_pattern() -> str:
    patterns = {f"*{ext}" for ext in VIDEO_EXTENSIONS}

    for mime_type in QMimeDatabase().allMimeTypes():
        if mime_type.name().startswith("video/"):
            patterns.update(mime_type.globPatterns())

    return _format_glob_pattern(patterns)


def _subtitle_file_glob_pattern() -> str:
    return _format_glob_pattern({f"*{ext}" for ext in SUBTITLE_EXTENSIONS})


def _document_file_glob_pattern() -> str:
    return _format_glob_pattern({f"*{ext}" for ext in DOCUMENT_EXTENSIONS})


def _format_glob_pattern(patterns: set[str]) -> str:
    return f" ({' '.join(sorted(patterns))})"


@QmlElement
class MpvqcImportFileDialogViewModel(QObject):
    _importer = inject.attr(ImportService)
    _settings = inject.attr(ImportSettingsService)

    @Property(str, constant=True, final=True)
    def videoFileGlobPattern(self) -> str:
        return _video_file_glob_pattern()

    @Property(str, constant=True, final=True)
    def subtitleFileGlobPattern(self) -> str:
        return _subtitle_file_glob_pattern()

    @Property(str, constant=True, final=True)
    def documentFileGlobPattern(self) -> str:
        return _document_file_glob_pattern()

    @Property(QUrl, constant=True, final=True)
    def lastDirectoryVideo(self) -> QUrl:
        return self._settings.last_directory_video

    @Property(QUrl, constant=True, final=True)
    def lastDirectoryDocuments(self) -> QUrl:
        return self._settings.last_directory_documents

    @Property(QUrl, constant=True, final=True)
    def lastDirectorySubtitles(self) -> QUrl:
        return self._settings.last_directory_subtitles

    @Slot(QUrl)
    def openVideo(self, url: QUrl) -> None:
        if url.isEmpty():
            return
        path = map_url_to_path(url)
        self._settings.last_directory_video = map_path_to_url(path.parent)
        self._importer.open((), (path,), ())

    @Slot(list)
    def openDocuments(self, urls: list[QUrl]) -> None:
        if not urls:
            return
        paths = tuple(map_url_to_path(url) for url in urls)
        self._settings.last_directory_documents = map_path_to_url(paths[0].parent)
        self._importer.open(paths, (), ())

    @Slot(list)
    def openSubtitles(self, urls: list[QUrl]) -> None:
        if not urls:
            return
        paths = tuple(map_url_to_path(url) for url in urls)
        self._settings.last_directory_subtitles = map_path_to_url(paths[0].parent)
        self._importer.open((), (), paths)
