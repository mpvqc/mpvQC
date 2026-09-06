# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, Self

from PySide6.QtCore import QStandardPaths, QUrl

from mpvqc.services import Setting, read_member

from .concerns import LoadFoundVideo

if TYPE_CHECKING:
    from collections.abc import Callable

    from PySide6.QtCore import QSettings


def _movies_location() -> QUrl:
    return QUrl.fromLocalFile(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.MoviesLocation))


def _documents_location() -> QUrl:
    return QUrl.fromLocalFile(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation))


def _read_directory(stored: object, default: Callable[[], QUrl]) -> QUrl:
    return stored if isinstance(stored, QUrl) else default()


class ImportSettingsService:
    def __init__(self, qsettings: QSettings) -> None:
        self._qsettings = qsettings

    @property
    def qsettings(self) -> QSettings:
        return self._qsettings

    import_found_video: Setting[Self, LoadFoundVideo] = Setting[Self, LoadFoundVideo](
        "Import/loadFoundVideo",
        default=lambda: LoadFoundVideo.ASK_EVERY_TIME,
        decode=lambda stored, default: read_member(stored, LoadFoundVideo, default),
        encode=lambda setting: setting.value,
    )

    last_directory_video: Setting[Self, QUrl] = Setting[Self, QUrl](
        "Import/lastDirectoryVideo",
        default=_movies_location,
        decode=_read_directory,
    )

    last_directory_documents: Setting[Self, QUrl] = Setting[Self, QUrl](
        "Import/lastDirectoryDocuments",
        default=_documents_location,
        decode=_read_directory,
    )

    last_directory_subtitles: Setting[Self, QUrl] = Setting[Self, QUrl](
        "Import/lastDirectorySubtitles",
        default=_documents_location,
        decode=_read_directory,
    )
