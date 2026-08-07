# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

from PySide6.QtCore import QStandardPaths, QUrl

from mpvqc.importing.domain import LoadFoundVideo

if TYPE_CHECKING:
    from collections.abc import Callable

    from PySide6.QtCore import QSettings

_LOAD_FOUND_VIDEO_KEY = "Import/loadFoundVideo"
_LAST_DIRECTORY_VIDEO_KEY = "Import/lastDirectoryVideo"
_LAST_DIRECTORY_DOCUMENTS_KEY = "Import/lastDirectoryDocuments"
_LAST_DIRECTORY_SUBTITLES_KEY = "Import/lastDirectorySubtitles"


def _movies_location() -> QUrl:
    return QUrl.fromLocalFile(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.MoviesLocation))


def _documents_location() -> QUrl:
    return QUrl.fromLocalFile(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation))


class ImportSettingsService:
    def __init__(self, qsettings: QSettings) -> None:
        self._qsettings = qsettings

    @property
    def import_found_video(self) -> LoadFoundVideo:
        # Reading with type=int would coerce a corrupted value to 0, which means ALWAYS
        stored = self._qsettings.value(_LOAD_FOUND_VIDEO_KEY)
        if isinstance(stored, str | int):
            with suppress(ValueError):
                return LoadFoundVideo(int(stored))
        return LoadFoundVideo.ASK_EVERY_TIME

    @import_found_video.setter
    def import_found_video(self, setting: LoadFoundVideo) -> None:
        self._qsettings.setValue(_LOAD_FOUND_VIDEO_KEY, setting.value)

    @property
    def last_directory_video(self) -> QUrl:
        return self._stored_directory(_LAST_DIRECTORY_VIDEO_KEY, _movies_location)

    @last_directory_video.setter
    def last_directory_video(self, directory: QUrl) -> None:
        self._qsettings.setValue(_LAST_DIRECTORY_VIDEO_KEY, directory)

    @property
    def last_directory_documents(self) -> QUrl:
        return self._stored_directory(_LAST_DIRECTORY_DOCUMENTS_KEY, _documents_location)

    @last_directory_documents.setter
    def last_directory_documents(self, directory: QUrl) -> None:
        self._qsettings.setValue(_LAST_DIRECTORY_DOCUMENTS_KEY, directory)

    @property
    def last_directory_subtitles(self) -> QUrl:
        return self._stored_directory(_LAST_DIRECTORY_SUBTITLES_KEY, _documents_location)

    @last_directory_subtitles.setter
    def last_directory_subtitles(self, directory: QUrl) -> None:
        self._qsettings.setValue(_LAST_DIRECTORY_SUBTITLES_KEY, directory)

    def _stored_directory(self, key: str, default: Callable[[], QUrl]) -> QUrl:
        stored = self._qsettings.value(key)
        return stored if isinstance(stored, QUrl) else default()
