# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import os
from dataclasses import dataclass
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

from mpvqc.appearance import (
    AccentColor,
    Appearance,
    ColorScheme,
    ColorSchemePreference,
    Dark,
    Light,
    format_color_scheme,
)
from mpvqc.datamodels import LANGUAGES, ImportFoundVideo
from mpvqc.enums import TimeDisplayMode, WindowTitleFormat

from .application_paths import ApplicationPathsService
from .type_mapper import TypeMapperService

if TYPE_CHECKING:
    from collections.abc import Callable

    from PySide6.QtCore import SignalInstance

_COLOR_SCHEME_PREFERENCE_KEY = "Appearance/colorSchemePreference"


def default_color_scheme_preference() -> ColorSchemePreference:
    return ColorSchemePreference.SYSTEM


def _accent_color_key(color_scheme: ColorScheme) -> str:
    return f"Appearance/accentColor/{format_color_scheme(color_scheme)}"


def _parse_color_scheme_preference(stored: str | None) -> ColorSchemePreference:
    try:
        return ColorSchemePreference(stored)
    except ValueError:
        return default_color_scheme_preference()


def default_username() -> str:
    return os.environ.get("USERNAME", os.environ.get("USER", "nickname"))


def default_documents_location() -> QUrl:
    location = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
    return QUrl.fromLocalFile(location)


def default_movie_location() -> QUrl:
    location = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.MoviesLocation)
    return QUrl.fromLocalFile(location)


def default_language(locale: QLocale | None = None) -> str:
    if locale is None:
        locale = QLocale.system()

    system_languages = locale.uiLanguages()

    for language in LANGUAGES:
        if language.identifier in system_languages:
            return language.identifier

    return "en-US"


def default_comment_types() -> list[str]:
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
    signal: Callable[[SettingsService], SignalInstance]

    @overload
    def __get__(self, obj: None, _owner: type | None = None) -> _Setting[T]: ...

    @overload
    def __get__(self, obj: SettingsService, _owner: type | None = None) -> T: ...

    def __get__(self, obj: SettingsService | None, _owner: type | None = None) -> T | _Setting[T]:
        if obj is None:
            return self
        if obj.qsettings.contains(self.key):
            return cast("T", obj.qsettings.value(self.key, type=self.type_))
        return self.default() if callable(self.default) else self.default

    def __set__(self, obj: SettingsService, value: T) -> None:
        if self.__get__(obj) != value:
            obj.qsettings.setValue(self.key, value)
            self.signal(obj).emit(value)


class SettingsService(QObject):
    _paths = inject.attr(ApplicationPathsService)
    _type_mapper = inject.attr(TypeMapperService)

    backup_enabled_changed = Signal(bool)
    backup_enabled = _Setting(
        "Backup/enabled",
        default=True,
        type_=bool,
        signal=lambda s: s.backup_enabled_changed,
    )

    backup_interval_changed = Signal(int)
    backup_interval = _Setting(
        "Backup/interval",
        default=60,
        type_=int,
        signal=lambda s: s.backup_interval_changed,
    )

    language_changed = Signal(str)
    language = _Setting(
        "Common/language",
        default=default_language,
        type_=str,
        signal=lambda s: s.language_changed,
    )

    comment_types_changed = Signal(list)
    comment_types = _Setting(
        "Common/commentTypes",
        default=default_comment_types,
        type_=list,
        signal=lambda s: s.comment_types_changed,
    )

    nickname_changed = Signal(str)
    nickname = _Setting(
        "Export/nickname",
        default=default_username,
        type_=str,
        signal=lambda s: s.nickname_changed,
    )

    write_header_date_changed = Signal(bool)
    write_header_date = _Setting(
        "Export/writeHeaderDate",
        default=True,
        type_=bool,
        signal=lambda s: s.write_header_date_changed,
    )

    write_header_generator_changed = Signal(bool)
    write_header_generator = _Setting(
        "Export/writeHeaderGenerator",
        default=True,
        type_=bool,
        signal=lambda s: s.write_header_generator_changed,
    )

    write_header_nickname_changed = Signal(bool)
    write_header_nickname = _Setting(
        "Export/writeHeaderNickname",
        default=False,
        type_=bool,
        signal=lambda s: s.write_header_nickname_changed,
    )

    write_header_video_path_changed = Signal(bool)
    write_header_video_path = _Setting(
        "Export/writeHeaderVideoPath",
        default=True,
        type_=bool,
        signal=lambda s: s.write_header_video_path_changed,
    )

    write_header_subtitles_changed = Signal(bool)
    write_header_subtitles = _Setting(
        "Export/writeHeaderSubtitles",
        default=False,
        type_=bool,
        signal=lambda s: s.write_header_subtitles_changed,
    )

    statusbar_percentage_changed = Signal(bool)
    statusbar_percentage = _Setting(
        "StatusBar/statusbarPercentage",
        default=True,
        type_=bool,
        signal=lambda s: s.statusbar_percentage_changed,
    )

    time_display_mode_changed = Signal(int)
    time_display_mode = _Setting(
        "StatusBar/timeFormat",
        default=TimeDisplayMode.CURRENT_TOTAL_TIME.value,
        type_=int,
        signal=lambda s: s.time_display_mode_changed,
    )

    last_directory_video_changed = Signal(QUrl)
    last_directory_video = _Setting(
        "Import/lastDirectoryVideo",
        default=default_movie_location,
        type_=QUrl,
        signal=lambda s: s.last_directory_video_changed,
    )

    last_directory_documents_changed = Signal(QUrl)
    last_directory_documents = _Setting(
        "Import/lastDirectoryDocuments",
        default=default_documents_location,
        type_=QUrl,
        signal=lambda s: s.last_directory_documents_changed,
    )

    last_directory_subtitles_changed = Signal(QUrl)
    last_directory_subtitles = _Setting(
        "Import/lastDirectorySubtitles",
        default=default_documents_location,
        type_=QUrl,
        signal=lambda s: s.last_directory_subtitles_changed,
    )

    import_found_video_changed = Signal(int)
    import_found_video = _Setting(
        "Import/importFoundVideo",
        default=ImportFoundVideo.ASK_EVERY_TIME.value,
        type_=int,
        signal=lambda s: s.import_found_video_changed,
    )

    layout_orientation_changed = Signal(int)
    layout_orientation = _Setting(
        "SplitView/layoutOrientation",
        default=Qt.Orientation.Vertical.value,
        type_=int,
        signal=lambda s: s.layout_orientation_changed,
    )

    color_scheme_preference_changed = Signal(ColorSchemePreference)
    appearance_changed = Signal(Appearance)

    window_title_format_changed = Signal(int)
    window_title_format = _Setting(
        "Window/titleFormat",
        default=WindowTitleFormat.DEFAULT.value,
        type_=int,
        signal=lambda s: s.window_title_format_changed,
    )

    def __init__(self, parent: QObject | None = None, ini_file: str | None = None) -> None:
        super().__init__(parent)
        file = ini_file if ini_file is not None else self._type_mapper.map_path_to_str(self._paths.file_settings)
        self.qsettings = QSettings(file, QSettings.Format.IniFormat)

    @property
    def color_scheme_preference(self) -> ColorSchemePreference:
        stored = self.qsettings.value(_COLOR_SCHEME_PREFERENCE_KEY, type=str)
        return _parse_color_scheme_preference(stored if isinstance(stored, str) else None)

    @color_scheme_preference.setter
    def color_scheme_preference(self, preference: ColorSchemePreference) -> None:
        if self.color_scheme_preference is preference:
            return
        self.qsettings.setValue(_COLOR_SCHEME_PREFERENCE_KEY, preference.value)
        self.color_scheme_preference_changed.emit(preference)
        self.appearance_changed.emit(self.appearance)

    @property
    def appearance(self) -> Appearance:
        return Appearance(
            color_scheme_preference=self.color_scheme_preference,
            light_accent_color=self.accent_color_for(Light()),
            dark_accent_color=self.accent_color_for(Dark()),
        )

    def accent_color_for(self, color_scheme: ColorScheme) -> AccentColor | None:
        return self._stored_accent_color(_accent_color_key(color_scheme))

    def set_accent_color(self, color_scheme: ColorScheme, accent_color: AccentColor | None) -> None:
        if self.accent_color_for(color_scheme) == accent_color:
            return
        self._store_accent_color(_accent_color_key(color_scheme), accent_color)
        self.appearance_changed.emit(self.appearance)

    def _stored_accent_color(self, key: str) -> AccentColor | None:
        if self.qsettings.contains(key):
            value = self.qsettings.value(key, type=str)
            if isinstance(value, str):
                return AccentColor(value)
        return None

    def _store_accent_color(self, key: str, accent_color: AccentColor | None) -> None:
        if accent_color is None:
            self.qsettings.remove(key)
        else:
            self.qsettings.setValue(key, accent_color)

    @staticmethod
    def default_comment_types() -> list[str]:
        return default_comment_types()
