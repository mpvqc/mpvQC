# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
from enum import IntEnum
from functools import cache

import inject
from PySide6.QtCore import QT_TRANSLATE_NOOP, QLocale, QObject, QSettings, QStandardPaths, Signal

from .application_paths import ApplicationPathsService
from .type_mapper import TypeMapperService


def get_default_username() -> str:
    return os.environ.get("USERNAME", os.environ.get("USER", "nickname"))


def get_default_documents_location() -> str:
    return QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)


def get_default_movie_location() -> str:
    return QStandardPaths.writableLocation(QStandardPaths.StandardLocation.MoviesLocation)


@cache
def get_default_language(locale: QLocale = QLocale.system()) -> str:
    system_languages = locale.uiLanguages()

    from mpvqc.models.languages import LANGUAGES

    for language in LANGUAGES:
        if language.identifier in system_languages:
            return language.identifier

    return "en-US"


# noinspection PyTypeChecker
class SettingsService(QObject):
    _paths: ApplicationPathsService = inject.attr(ApplicationPathsService)
    _type_mapper: TypeMapperService = inject.attr(TypeMapperService)

    class TimeFormat(IntEnum):
        EMPTY = 0
        CURRENT_TIME = 1
        REMAINING_TIME = 2
        CURRENT_TOTAL_TIME = 3

    class ImportWhenVideoLinkedInDocument(IntEnum):
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

    # StatusBar
    statusbarPercentageChanged = Signal(bool)
    timeFormatChanged = Signal(int)

    # Import
    lastDirectoryVideoChanged = Signal(str)
    lastDirectoryDocumentsChanged = Signal(str)
    lastDirectorySubtitlesChanged = Signal(str)
    importWhenVideoLinkedInDocumentChanged = Signal(int)

    # SplitView
    layoutOrientationChanged = Signal(int)

    # Theme
    themeIdentifierChanged = Signal(str)
    themeColorOptionChanged = Signal(int)

    # Window Title
    windowTitleFormatChanged = Signal(int)

    def __init__(self, parent=None, ini_file: str = None):
        super().__init__(parent)
        if ini_file is None:
            ini_file = self._type_mapper.map_path_to_str(self._paths.file_settings)
        self._settings = QSettings(ini_file, QSettings.Format.IniFormat)

    @staticmethod
    def get_default_comment_types() -> list[str]:
        return [
            QT_TRANSLATE_NOOP("CommentTypes", "Translation"),
            QT_TRANSLATE_NOOP("CommentTypes", "Spelling"),
            QT_TRANSLATE_NOOP("CommentTypes", "Punctuation"),
            QT_TRANSLATE_NOOP("CommentTypes", "Phrasing"),
            QT_TRANSLATE_NOOP("CommentTypes", "Timing"),
            QT_TRANSLATE_NOOP("CommentTypes", "Typeset"),
            QT_TRANSLATE_NOOP("CommentTypes", "Note"),
        ]

    @property
    def backup_enabled(self) -> bool:
        return self._settings.value("Backup/enabled", True, type=bool)

    @backup_enabled.setter
    def backup_enabled(self, value: bool):
        if self.backup_enabled != value:
            self._settings.setValue("Backup/enabled", value)
            self.backupEnabledChanged.emit(value)

    @property
    def backup_interval(self) -> int:
        return self._settings.value("Backup/interval", 60, type=int)

    @backup_interval.setter
    def backup_interval(self, value: int):
        if self.backup_interval != value:
            self._settings.setValue("Backup/interval", value)
            self.backupIntervalChanged.emit(value)

    @property
    def language(self) -> str:
        return self._settings.value("Common/language", get_default_language(), type=str)

    @language.setter
    def language(self, value: str):
        if self.language != value:
            self._settings.setValue("Common/language", value)
            self.languageChanged.emit(value)

    @property
    def comment_types(self) -> list[str]:
        return self._settings.value("Common/commentTypes", self.get_default_comment_types(), type=list)

    @comment_types.setter
    def comment_types(self, value: list[str]):
        if self.comment_types != value:
            self._settings.setValue("Common/commentTypes", value)
            self.commentTypesChanged.emit(value)

    @property
    def nickname(self) -> str:
        return self._settings.value("Export/nickname", get_default_username(), type=str)

    @nickname.setter
    def nickname(self, value: str):
        if self.nickname != value:
            self._settings.setValue("Export/nickname", value)
            self.nicknameChanged.emit(value)

    @property
    def write_header_date(self) -> bool:
        return self._settings.value("Export/writeHeaderDate", True, type=bool)

    @write_header_date.setter
    def write_header_date(self, value: bool):
        if self.write_header_date != value:
            self._settings.setValue("Export/writeHeaderDate", value)
            self.writeHeaderDateChanged.emit(value)

    @property
    def write_header_generator(self) -> bool:
        return self._settings.value("Export/writeHeaderGenerator", True, type=bool)

    @write_header_generator.setter
    def write_header_generator(self, value: bool):
        if self.write_header_generator != value:
            self._settings.setValue("Export/writeHeaderGenerator", value)
            self.writeHeaderGeneratorChanged.emit(value)

    @property
    def write_header_nickname(self) -> bool:
        return self._settings.value("Export/writeHeaderNickname", False, type=bool)

    @write_header_nickname.setter
    def write_header_nickname(self, value: bool):
        if self.write_header_nickname != value:
            self._settings.setValue("Export/writeHeaderNickname", value)
            self.writeHeaderNicknameChanged.emit(value)

    @property
    def write_header_video_path(self) -> bool:
        return self._settings.value("Export/writeHeaderVideoPath", True, type=bool)

    @write_header_video_path.setter
    def write_header_video_path(self, value: bool):
        if self.write_header_video_path != value:
            self._settings.setValue("Export/writeHeaderVideoPath", value)
            self.writeHeaderVideoPathChanged.emit(value)

    @property
    def statusbar_percentage(self) -> bool:
        return self._settings.value("StatusBar/statusbarPercentage", True, type=bool)

    @statusbar_percentage.setter
    def statusbar_percentage(self, value: bool):
        if self.statusbar_percentage != value:
            self._settings.setValue("StatusBar/statusbarPercentage", value)
            self.statusbarPercentageChanged.emit(value)

    @property
    def time_format(self) -> int:
        return self._settings.value("StatusBar/timeFormat", 3, type=int)  # CURRENT_TOTAL_TIME

    @time_format.setter
    def time_format(self, value: int):
        if self.time_format != value:
            self._settings.setValue("StatusBar/timeFormat", value)
            self.timeFormatChanged.emit(value)

    @property
    def last_directory_video(self) -> str:
        return self._settings.value("Import/lastDirectoryVideo", get_default_movie_location(), type=str)

    @last_directory_video.setter
    def last_directory_video(self, value: str):
        if self.last_directory_video != value:
            self._settings.setValue("Import/lastDirectoryVideo", value)
            self.lastDirectoryVideoChanged.emit(value)

    @property
    def last_directory_documents(self) -> str:
        return self._settings.value("Import/lastDirectoryDocuments", get_default_documents_location(), type=str)

    @last_directory_documents.setter
    def last_directory_documents(self, value: str):
        if self.last_directory_documents != value:
            self._settings.setValue("Import/lastDirectoryDocuments", value)
            self.lastDirectoryDocumentsChanged.emit(value)

    @property
    def last_directory_subtitles(self) -> str:
        return self._settings.value("Import/lastDirectorySubtitles", get_default_documents_location(), type=str)

    @last_directory_subtitles.setter
    def last_directory_subtitles(self, value: str):
        if self.last_directory_subtitles != value:
            self._settings.setValue("Import/lastDirectorySubtitles", value)
            self.lastDirectorySubtitlesChanged.emit(value)

    @property
    def import_when_video_linked_in_document(self) -> int:
        return self._settings.value("Import/importWhenVideoLinkedInDocument", 1, type=int)  # ASK_EVERY_TIME

    @import_when_video_linked_in_document.setter
    def import_when_video_linked_in_document(self, value: int):
        if self.import_when_video_linked_in_document != value:
            self._settings.setValue("Import/importWhenVideoLinkedInDocument", value)
            self.importWhenVideoLinkedInDocumentChanged.emit(value)

    @property
    def layout_orientation(self) -> int:
        return self._settings.value("SplitView/layoutOrientation", 2, type=int)  # Qt.Vertical

    @layout_orientation.setter
    def layout_orientation(self, value: int):
        if self.layout_orientation != value:
            self._settings.setValue("SplitView/layoutOrientation", value)
            self.layoutOrientationChanged.emit(value)

    @property
    def theme_identifier(self) -> str:
        return self._settings.value("Theme/themeIdentifier", "material-you-dark", type=str)

    @theme_identifier.setter
    def theme_identifier(self, value: str):
        if self.theme_identifier != value:
            self._settings.setValue("Theme/themeIdentifier", value)
            self.themeIdentifierChanged.emit(value)

    @property
    def theme_color_option(self) -> int:
        return self._settings.value("Theme/themeColorOption", 4, type=int)

    @theme_color_option.setter
    def theme_color_option(self, value: int):
        if self.theme_color_option != value:
            self._settings.setValue("Theme/themeColorOption", value)
            self.themeColorOptionChanged.emit(value)

    @property
    def window_title_format(self) -> int:
        return self._settings.value("Window/titleFormat", 0, type=int)

    @window_title_format.setter
    def window_title_format(self, value: int):
        if self.window_title_format != value:
            self._settings.setValue("Window/titleFormat", value)
            self.windowTitleFormatChanged.emit(value)
