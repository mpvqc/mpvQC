# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import os
from dataclasses import dataclass
from enum import IntEnum
from functools import cache
from typing import TYPE_CHECKING, cast, overload

import inject
from PySide6.QtCore import (
    QT_TRANSLATE_NOOP,
    QLocale,
    QObject,
    QSettings,
    QStandardPaths,
    Qt,
    QUrl,
    Signal,
)

from .application_paths import ApplicationPathsService
from .type_mapper import TypeMapperService

if TYPE_CHECKING:
    from collections.abc import Callable


def get_default_username() -> str:
    return os.environ.get("USERNAME", os.environ.get("USER", "nickname"))


def get_default_documents_location() -> QUrl:
    location = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
    return QUrl.fromLocalFile(location)


def get_default_movie_location() -> QUrl:
    location = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.MoviesLocation)
    return QUrl.fromLocalFile(location)


@cache
def get_default_language(locale: QLocale | None = None) -> str:
    if locale is None:
        locale = QLocale.system()

    system_languages = locale.uiLanguages()

    from mpvqc.models.languages import LANGUAGES

    for language in LANGUAGES:
        if language.identifier in system_languages:
            return language.identifier

    return "en-US"


def get_default_comment_types() -> list[str]:
    return [
        str(QT_TRANSLATE_NOOP("CommentTypes", "Translation")),
        str(QT_TRANSLATE_NOOP("CommentTypes", "Spelling")),
        str(QT_TRANSLATE_NOOP("CommentTypes", "Punctuation")),
        str(QT_TRANSLATE_NOOP("CommentTypes", "Phrasing")),
        str(QT_TRANSLATE_NOOP("CommentTypes", "Timing")),
        str(QT_TRANSLATE_NOOP("CommentTypes", "Typeset")),
        str(QT_TRANSLATE_NOOP("CommentTypes", "Note")),
    ]


@dataclass(eq=False)
class _Setting[T]:
    key: str
    default: T | Callable[[], T]
    type_: type[T]
    signal: Signal

    @overload
    def __get__(self, obj: None, _owner: type | None = None) -> _Setting[T]: ...

    @overload
    def __get__(self, obj: SettingsService, _owner: type | None = None) -> T: ...

    def __get__(self, obj: SettingsService | None, _owner: type | None = None) -> T | _Setting[T]:
        if obj is None:
            return self
        default = self.default() if callable(self.default) else self.default
        return cast("T", obj.qsettings.value(self.key, default, type=self.type_))

    def __set__(self, obj: SettingsService, value: T) -> None:
        if self.__get__(obj) != value:
            obj.qsettings.setValue(self.key, value)
            self.signal.__get__(obj, type(obj)).emit(value)


class SettingsService(QObject):
    _paths = inject.attr(ApplicationPathsService)
    _type_mapper = inject.attr(TypeMapperService)

    class ImportFoundVideo(IntEnum):
        ALWAYS = 0
        ASK_EVERY_TIME = 1
        NEVER = 2

    backupEnabledChanged = Signal(bool)
    backup_enabled = _Setting(
        "Backup/enabled",
        default=True,
        type_=bool,
        signal=backupEnabledChanged,
    )

    backupIntervalChanged = Signal(int)
    backup_interval = _Setting(
        "Backup/interval",
        default=60,
        type_=int,
        signal=backupIntervalChanged,
    )

    languageChanged = Signal(str)
    language = _Setting(
        "Common/language",
        default=get_default_language,
        type_=str,
        signal=languageChanged,
    )

    commentTypesChanged = Signal(list)
    comment_types = _Setting(
        "Common/commentTypes",
        default=get_default_comment_types,
        type_=list,
        signal=commentTypesChanged,
    )

    nicknameChanged = Signal(str)
    nickname = _Setting(
        "Export/nickname",
        default=get_default_username,
        type_=str,
        signal=nicknameChanged,
    )

    writeHeaderDateChanged = Signal(bool)
    write_header_date = _Setting(
        "Export/writeHeaderDate",
        default=True,
        type_=bool,
        signal=writeHeaderDateChanged,
    )

    writeHeaderGeneratorChanged = Signal(bool)
    write_header_generator = _Setting(
        "Export/writeHeaderGenerator",
        default=True,
        type_=bool,
        signal=writeHeaderGeneratorChanged,
    )

    writeHeaderNicknameChanged = Signal(bool)
    write_header_nickname = _Setting(
        "Export/writeHeaderNickname",
        default=False,
        type_=bool,
        signal=writeHeaderNicknameChanged,
    )

    writeHeaderVideoPathChanged = Signal(bool)
    write_header_video_path = _Setting(
        "Export/writeHeaderVideoPath",
        default=True,
        type_=bool,
        signal=writeHeaderVideoPathChanged,
    )

    writeHeaderSubtitlesChanged = Signal(bool)
    write_header_subtitles = _Setting(
        "Export/writeHeaderSubtitles",
        default=False,
        type_=bool,
        signal=writeHeaderSubtitlesChanged,
    )

    statusbarPercentageChanged = Signal(bool)
    statusbar_percentage = _Setting(
        "StatusBar/statusbarPercentage",
        default=True,
        type_=bool,
        signal=statusbarPercentageChanged,
    )

    timeFormatChanged = Signal(int)
    time_format = _Setting(
        "StatusBar/timeFormat",
        default=3,
        type_=int,
        signal=timeFormatChanged,
    )

    lastDirectoryVideoChanged = Signal(QUrl)
    last_directory_video = _Setting(
        "Import/lastDirectoryVideo",
        default=get_default_movie_location,
        type_=QUrl,
        signal=lastDirectoryVideoChanged,
    )

    lastDirectoryDocumentsChanged = Signal(QUrl)
    last_directory_documents = _Setting(
        "Import/lastDirectoryDocuments",
        default=get_default_documents_location,
        type_=QUrl,
        signal=lastDirectoryDocumentsChanged,
    )

    lastDirectorySubtitlesChanged = Signal(QUrl)
    last_directory_subtitles = _Setting(
        "Import/lastDirectorySubtitles",
        default=get_default_documents_location,
        type_=QUrl,
        signal=lastDirectorySubtitlesChanged,
    )

    importFoundVideoChanged = Signal(int)
    import_found_video = _Setting(
        "Import/importFoundVideo",
        default=1,
        type_=int,
        signal=importFoundVideoChanged,
    )

    layoutOrientationChanged = Signal(int)
    layout_orientation = _Setting(
        "SplitView/layoutOrientation",
        default=Qt.Orientation.Vertical.value,
        type_=int,
        signal=layoutOrientationChanged,
    )

    themeIdentifierChanged = Signal(str)
    theme_identifier = _Setting(
        "Theme/themeIdentifier",
        default="material-you-dark",
        type_=str,
        signal=themeIdentifierChanged,
    )

    themeColorOptionChanged = Signal(int)
    theme_color_option = _Setting(
        "Theme/themeColorOption",
        default=4,
        type_=int,
        signal=themeColorOptionChanged,
    )

    windowTitleFormatChanged = Signal(int)
    window_title_format = _Setting(
        "Window/titleFormat",
        default=0,
        type_=int,
        signal=windowTitleFormatChanged,
    )

    def __init__(self, parent: QObject | None = None, ini_file: str | None = None) -> None:
        super().__init__(parent)
        file = ini_file if ini_file is not None else self._type_mapper.map_path_to_str(self._paths.file_settings)
        self.qsettings = QSettings(file, QSettings.Format.IniFormat)

    @staticmethod
    def get_default_comment_types() -> list[str]:
        return get_default_comment_types()
