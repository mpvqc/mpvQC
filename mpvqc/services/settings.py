# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, cast, overload

from PySide6.QtCore import (
    QLocale,
    QObject,
    QSettings,
    Qt,
    Signal,
)

from mpvqc.enums import TimeDisplayMode, WindowTitleFormat
from mpvqc.languages import LANGUAGES

if TYPE_CHECKING:
    from collections.abc import Callable

    from PySide6.QtCore import SignalInstance


def default_language(locale: QLocale | None = None) -> str:
    if locale is None:
        locale = QLocale.system()

    system_languages = locale.uiLanguages()

    for language in LANGUAGES:
        if language.identifier in system_languages:
            return language.identifier

    return "en-US"


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
    language_changed = Signal(str)
    language = _Setting(
        "Common/language",
        default=default_language,
        type_=str,
        signal=lambda s: s.language_changed,
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

    layout_orientation_changed = Signal(int)
    layout_orientation = _Setting(
        "SplitView/layoutOrientation",
        default=Qt.Orientation.Vertical.value,
        type_=int,
        signal=lambda s: s.layout_orientation_changed,
    )

    window_title_format_changed = Signal(int)
    window_title_format = _Setting(
        "Window/titleFormat",
        default=WindowTitleFormat.DEFAULT.value,
        type_=int,
        signal=lambda s: s.window_title_format_changed,
    )

    def __init__(self, qsettings: QSettings, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.qsettings = qsettings
