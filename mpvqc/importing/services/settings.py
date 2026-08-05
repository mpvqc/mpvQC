# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, QStandardPaths, QUrl, Signal

from mpvqc.importing.domain import ImportFoundVideo

if TYPE_CHECKING:
    from collections.abc import Callable

    from PySide6.QtCore import QSettings

_IMPORT_FOUND_VIDEO_KEY = "Import/importFoundVideo"
_LAST_DIRECTORY_VIDEO_KEY = "Import/lastDirectoryVideo"
_LAST_DIRECTORY_DOCUMENTS_KEY = "Import/lastDirectoryDocuments"
_LAST_DIRECTORY_SUBTITLES_KEY = "Import/lastDirectorySubtitles"


def _movies_location() -> QUrl:
    return QUrl.fromLocalFile(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.MoviesLocation))


def _documents_location() -> QUrl:
    return QUrl.fromLocalFile(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation))


class ImportSettingsService(QObject):
    import_found_video_changed = Signal(ImportFoundVideo)
    last_directory_video_changed = Signal(QUrl)
    last_directory_documents_changed = Signal(QUrl)
    last_directory_subtitles_changed = Signal(QUrl)

    def __init__(self, qsettings: QSettings, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._qsettings = qsettings

    @property
    def import_found_video(self) -> ImportFoundVideo:
        # Reading with type=int would coerce a corrupted value to 0, which means ALWAYS
        stored = self._stored(_IMPORT_FOUND_VIDEO_KEY)
        if isinstance(stored, str | int):
            with suppress(ValueError):
                return ImportFoundVideo(int(stored))
        return ImportFoundVideo.ASK_EVERY_TIME

    @import_found_video.setter
    def import_found_video(self, setting: ImportFoundVideo) -> None:
        if self.import_found_video == setting:
            return
        self._qsettings.setValue(_IMPORT_FOUND_VIDEO_KEY, setting.value)
        self.import_found_video_changed.emit(setting)

    @property
    def last_directory_video(self) -> QUrl:
        return self._stored_directory(_LAST_DIRECTORY_VIDEO_KEY, _movies_location)

    @last_directory_video.setter
    def last_directory_video(self, directory: QUrl) -> None:
        if self.last_directory_video == directory:
            return
        self._qsettings.setValue(_LAST_DIRECTORY_VIDEO_KEY, directory)
        self.last_directory_video_changed.emit(directory)

    @property
    def last_directory_documents(self) -> QUrl:
        return self._stored_directory(_LAST_DIRECTORY_DOCUMENTS_KEY, _documents_location)

    @last_directory_documents.setter
    def last_directory_documents(self, directory: QUrl) -> None:
        if self.last_directory_documents == directory:
            return
        self._qsettings.setValue(_LAST_DIRECTORY_DOCUMENTS_KEY, directory)
        self.last_directory_documents_changed.emit(directory)

    @property
    def last_directory_subtitles(self) -> QUrl:
        return self._stored_directory(_LAST_DIRECTORY_SUBTITLES_KEY, _documents_location)

    @last_directory_subtitles.setter
    def last_directory_subtitles(self, directory: QUrl) -> None:
        if self.last_directory_subtitles == directory:
            return
        self._qsettings.setValue(_LAST_DIRECTORY_SUBTITLES_KEY, directory)
        self.last_directory_subtitles_changed.emit(directory)

    def _stored_directory(self, key: str, default: Callable[[], QUrl]) -> QUrl:
        stored = self._stored(key)
        return stored if isinstance(stored, QUrl) else default()

    def _stored(self, key: str) -> object:
        return self._qsettings.value(key) if self._qsettings.contains(key) else None
