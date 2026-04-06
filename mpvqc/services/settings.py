# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
from enum import IntEnum
from functools import cache
from typing import cast

import inject
from PySide6.QtCore import QT_TRANSLATE_NOOP, QLocale, QObject, QSettings, QStandardPaths, QUrl, Signal, SignalInstance

from .application_paths import ApplicationPathsService
from .type_mapper import TypeMapperService


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


class SettingsService(QObject):
    _paths = inject.attr(ApplicationPathsService)
    _type_mapper = inject.attr(TypeMapperService)

    class TimeFormat(IntEnum):
        EMPTY = 0
        CURRENT_TIME = 1
        REMAINING_TIME = 2
        CURRENT_TOTAL_TIME = 3

    class ImportFoundVideo(IntEnum):
        ALWAYS = 0
        ASK_EVERY_TIME = 1
        NEVER = 2

    # Backup
    backupEnabledChanged = Signal(bool)
    backupIntervalChanged = Signal(int)

    # Common
    languageChanged = Signal(str)
    commentTypesChanged = Signal(list)

    # Export
    nicknameChanged = Signal(str)
    writeHeaderDateChanged = Signal(bool)
    writeHeaderGeneratorChanged = Signal(bool)
    writeHeaderNicknameChanged = Signal(bool)
    writeHeaderVideoPathChanged = Signal(bool)
    writeHeaderSubtitlesChanged = Signal(bool)

    # StatusBar
    statusbarPercentageChanged = Signal(bool)
    timeFormatChanged = Signal(int)

    # Import
    lastDirectoryVideoChanged = Signal(QUrl)
    lastDirectoryDocumentsChanged = Signal(QUrl)
    lastDirectorySubtitlesChanged = Signal(QUrl)
    importFoundVideoChanged = Signal(int)

    # SplitView
    layoutOrientationChanged = Signal(int)

    # Theme
    themeIdentifierChanged = Signal(str)
    themeColorOptionChanged = Signal(int)

    # Window Title
    windowTitleFormatChanged = Signal(int)

    def __init__(self, parent: QObject | None = None, ini_file: str | None = None) -> None:
        super().__init__(parent)
        file = ini_file if ini_file is not None else self._type_mapper.map_path_to_str(self._paths.file_settings)
        self._settings = QSettings(file, QSettings.Format.IniFormat)

    def _get[T](self, key: str, default: T, *, _type: type[T]) -> T:
        # noinspection PyUnnecessaryCast
        return cast("T", self._settings.value(key, default, type=_type))

    def _set[T](self, key: str, current_value: T, new_value: T, signal: SignalInstance) -> None:
        if current_value != new_value:
            self._settings.setValue(key, new_value)
            signal.emit(new_value)

    @staticmethod
    def get_default_comment_types() -> list[str]:
        return get_default_comment_types()

    @property
    def backup_enabled(self) -> bool:
        return self._get("Backup/enabled", True, _type=bool)

    @backup_enabled.setter
    def backup_enabled(self, value: bool) -> None:
        self._set("Backup/enabled", self.backup_enabled, value, self.backupEnabledChanged)

    @property
    def backup_interval(self) -> int:
        return self._get("Backup/interval", 60, _type=int)

    @backup_interval.setter
    def backup_interval(self, value: int) -> None:
        self._set("Backup/interval", self.backup_interval, value, self.backupIntervalChanged)

    @property
    def language(self) -> str:
        return self._get("Common/language", get_default_language(), _type=str)

    @language.setter
    def language(self, value: str) -> None:
        self._set("Common/language", self.language, value, self.languageChanged)

    @property
    def comment_types(self) -> list[str]:
        return self._get("Common/commentTypes", self.get_default_comment_types(), _type=list)

    @comment_types.setter
    def comment_types(self, value: list[str]) -> None:
        self._set("Common/commentTypes", self.comment_types, value, self.commentTypesChanged)

    @property
    def nickname(self) -> str:
        return self._get("Export/nickname", get_default_username(), _type=str)

    @nickname.setter
    def nickname(self, value: str) -> None:
        self._set("Export/nickname", self.nickname, value, self.nicknameChanged)

    @property
    def write_header_date(self) -> bool:
        return self._get("Export/writeHeaderDate", True, _type=bool)

    @write_header_date.setter
    def write_header_date(self, value: bool) -> None:
        self._set("Export/writeHeaderDate", self.write_header_date, value, self.writeHeaderDateChanged)

    @property
    def write_header_generator(self) -> bool:
        return self._get("Export/writeHeaderGenerator", True, _type=bool)

    @write_header_generator.setter
    def write_header_generator(self, value: bool) -> None:
        self._set("Export/writeHeaderGenerator", self.write_header_generator, value, self.writeHeaderGeneratorChanged)

    @property
    def write_header_nickname(self) -> bool:
        return self._get("Export/writeHeaderNickname", False, _type=bool)

    @write_header_nickname.setter
    def write_header_nickname(self, value: bool) -> None:
        self._set("Export/writeHeaderNickname", self.write_header_nickname, value, self.writeHeaderNicknameChanged)

    @property
    def write_header_video_path(self) -> bool:
        return self._get("Export/writeHeaderVideoPath", True, _type=bool)

    @write_header_video_path.setter
    def write_header_video_path(self, value: bool) -> None:
        self._set("Export/writeHeaderVideoPath", self.write_header_video_path, value, self.writeHeaderVideoPathChanged)

    @property
    def write_header_subtitles(self) -> bool:
        return self._get("Export/writeHeaderSubtitles", False, _type=bool)

    @write_header_subtitles.setter
    def write_header_subtitles(self, value: bool) -> None:
        self._set("Export/writeHeaderSubtitles", self.write_header_subtitles, value, self.writeHeaderSubtitlesChanged)

    @property
    def statusbar_percentage(self) -> bool:
        return self._get("StatusBar/statusbarPercentage", True, _type=bool)

    @statusbar_percentage.setter
    def statusbar_percentage(self, value: bool) -> None:
        self._set("StatusBar/statusbarPercentage", self.statusbar_percentage, value, self.statusbarPercentageChanged)

    @property
    def time_format(self) -> int:
        return self._get("StatusBar/timeFormat", 3, _type=int)  # CURRENT_TOTAL_TIME

    @time_format.setter
    def time_format(self, value: int) -> None:
        self._set("StatusBar/timeFormat", self.time_format, value, self.timeFormatChanged)

    @property
    def last_directory_video(self) -> QUrl:
        return self._get("Import/lastDirectoryVideo", get_default_movie_location(), _type=QUrl)

    @last_directory_video.setter
    def last_directory_video(self, value: QUrl) -> None:
        self._set("Import/lastDirectoryVideo", self.last_directory_video, value, self.lastDirectoryVideoChanged)

    @property
    def last_directory_documents(self) -> QUrl:
        return self._get("Import/lastDirectoryDocuments", get_default_documents_location(), _type=QUrl)

    @last_directory_documents.setter
    def last_directory_documents(self, value: QUrl) -> None:
        self._set(
            "Import/lastDirectoryDocuments", self.last_directory_documents, value, self.lastDirectoryDocumentsChanged
        )

    @property
    def last_directory_subtitles(self) -> QUrl:
        return self._get("Import/lastDirectorySubtitles", get_default_documents_location(), _type=QUrl)

    @last_directory_subtitles.setter
    def last_directory_subtitles(self, value: QUrl) -> None:
        self._set(
            "Import/lastDirectorySubtitles", self.last_directory_subtitles, value, self.lastDirectorySubtitlesChanged
        )

    @property
    def import_found_video(self) -> int:
        return self._get("Import/importFoundVideo", 1, _type=int)  # ASK_EVERY_TIME

    @import_found_video.setter
    def import_found_video(self, value: int) -> None:
        self._set("Import/importFoundVideo", self.import_found_video, value, self.importFoundVideoChanged)

    @property
    def layout_orientation(self) -> int:
        return self._get("SplitView/layoutOrientation", 2, _type=int)  # Qt.Vertical

    @layout_orientation.setter
    def layout_orientation(self, value: int) -> None:
        self._set("SplitView/layoutOrientation", self.layout_orientation, value, self.layoutOrientationChanged)

    @property
    def theme_identifier(self) -> str:
        return self._get("Theme/themeIdentifier", "material-you-dark", _type=str)

    @theme_identifier.setter
    def theme_identifier(self, value: str) -> None:
        self._set("Theme/themeIdentifier", self.theme_identifier, value, self.themeIdentifierChanged)

    @property
    def theme_color_option(self) -> int:
        return self._get("Theme/themeColorOption", 4, _type=int)

    @theme_color_option.setter
    def theme_color_option(self, value: int) -> None:
        self._set("Theme/themeColorOption", self.theme_color_option, value, self.themeColorOptionChanged)

    @property
    def window_title_format(self) -> int:
        return self._get("Window/titleFormat", 0, _type=int)

    @window_title_format.setter
    def window_title_format(self, value: int) -> None:
        self._set("Window/titleFormat", self.window_title_format, value, self.windowTitleFormatChanged)
