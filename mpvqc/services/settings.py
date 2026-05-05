# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import os
from dataclasses import dataclass
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

from mpvqc.enums import MpvqcImportFoundVideo, MpvqcTimeFormat, MpvqcWindowTitleFormat

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

    backup_enabled_changed = Signal(bool)
    backup_enabled = _Setting(
        "Backup/enabled",
        default=True,
        type_=bool,
        signal=backup_enabled_changed,
    )

    backup_interval_changed = Signal(int)
    backup_interval = _Setting(
        "Backup/interval",
        default=60,
        type_=int,
        signal=backup_interval_changed,
    )

    language_changed = Signal(str)
    language = _Setting(
        "Common/language",
        default=get_default_language,
        type_=str,
        signal=language_changed,
    )

    comment_types_changed = Signal(list)
    comment_types = _Setting(
        "Common/commentTypes",
        default=get_default_comment_types,
        type_=list,
        signal=comment_types_changed,
    )

    nickname_changed = Signal(str)
    nickname = _Setting(
        "Export/nickname",
        default=get_default_username,
        type_=str,
        signal=nickname_changed,
    )

    write_header_date_changed = Signal(bool)
    write_header_date = _Setting(
        "Export/writeHeaderDate",
        default=True,
        type_=bool,
        signal=write_header_date_changed,
    )

    write_header_generator_changed = Signal(bool)
    write_header_generator = _Setting(
        "Export/writeHeaderGenerator",
        default=True,
        type_=bool,
        signal=write_header_generator_changed,
    )

    write_header_nickname_changed = Signal(bool)
    write_header_nickname = _Setting(
        "Export/writeHeaderNickname",
        default=False,
        type_=bool,
        signal=write_header_nickname_changed,
    )

    write_header_video_path_changed = Signal(bool)
    write_header_video_path = _Setting(
        "Export/writeHeaderVideoPath",
        default=True,
        type_=bool,
        signal=write_header_video_path_changed,
    )

    write_header_subtitles_changed = Signal(bool)
    write_header_subtitles = _Setting(
        "Export/writeHeaderSubtitles",
        default=False,
        type_=bool,
        signal=write_header_subtitles_changed,
    )

    statusbar_percentage_changed = Signal(bool)
    statusbar_percentage = _Setting(
        "StatusBar/statusbarPercentage",
        default=True,
        type_=bool,
        signal=statusbar_percentage_changed,
    )

    time_format_changed = Signal(int)
    time_format = _Setting(
        "StatusBar/timeFormat",
        default=MpvqcTimeFormat.TimeFormat.CURRENT_TOTAL_TIME.value,
        type_=int,
        signal=time_format_changed,
    )

    last_directory_video_changed = Signal(QUrl)
    last_directory_video = _Setting(
        "Import/lastDirectoryVideo",
        default=get_default_movie_location,
        type_=QUrl,
        signal=last_directory_video_changed,
    )

    last_directory_documents_changed = Signal(QUrl)
    last_directory_documents = _Setting(
        "Import/lastDirectoryDocuments",
        default=get_default_documents_location,
        type_=QUrl,
        signal=last_directory_documents_changed,
    )

    last_directory_subtitles_changed = Signal(QUrl)
    last_directory_subtitles = _Setting(
        "Import/lastDirectorySubtitles",
        default=get_default_documents_location,
        type_=QUrl,
        signal=last_directory_subtitles_changed,
    )

    import_found_video_changed = Signal(int)
    import_found_video = _Setting(
        "Import/importFoundVideo",
        default=MpvqcImportFoundVideo.ImportFoundVideo.ASK_EVERY_TIME.value,
        type_=int,
        signal=import_found_video_changed,
    )

    layout_orientation_changed = Signal(int)
    layout_orientation = _Setting(
        "SplitView/layoutOrientation",
        default=Qt.Orientation.Vertical.value,
        type_=int,
        signal=layout_orientation_changed,
    )

    theme_identifier_changed = Signal(str)
    theme_identifier = _Setting(
        "Theme/themeIdentifier",
        default="material-you-dark",
        type_=str,
        signal=theme_identifier_changed,
    )

    theme_color_option_changed = Signal(int)
    theme_color_option = _Setting(
        "Theme/themeColorOption",
        default=4,
        type_=int,
        signal=theme_color_option_changed,
    )

    window_title_format_changed = Signal(int)
    window_title_format = _Setting(
        "Window/titleFormat",
        default=MpvqcWindowTitleFormat.WindowTitleFormat.DEFAULT.value,
        type_=int,
        signal=window_title_format_changed,
    )

    def __init__(self, parent: QObject | None = None, ini_file: str | None = None) -> None:
        super().__init__(parent)
        file = ini_file if ini_file is not None else self._type_mapper.map_path_to_str(self._paths.file_settings)
        self.qsettings = QSettings(file, QSettings.Format.IniFormat)

    @staticmethod
    def get_default_comment_types() -> list[str]:
        return get_default_comment_types()
