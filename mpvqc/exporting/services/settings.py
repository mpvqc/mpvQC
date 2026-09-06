# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Self

from PySide6.QtCore import QObject, Signal

from mpvqc.services import Setting, read_bool, read_int

if TYPE_CHECKING:
    from PySide6.QtCore import QSettings

_BACKUP_ENABLED_KEY = "Backup/enabled"
_BACKUP_INTERVAL_KEY = "Backup/interval"
_NICKNAME_KEY = "Export/nickname"
_WRITE_HEADER_DATE_KEY = "Export/writeHeaderDate"
_WRITE_HEADER_GENERATOR_KEY = "Export/writeHeaderGenerator"
_WRITE_HEADER_NICKNAME_KEY = "Export/writeHeaderNickname"
_WRITE_HEADER_VIDEO_PATH_KEY = "Export/writeHeaderVideoPath"
_WRITE_HEADER_SUBTITLES_KEY = "Export/writeHeaderSubtitles"


def _default_username() -> str:
    return os.environ.get("USERNAME", os.environ.get("USER", "nickname"))


class ExportSettingsService(QObject):
    backup_enabled_changed = Signal(bool)
    backup_interval_changed = Signal(int)

    def __init__(self, qsettings: QSettings, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.qsettings = qsettings

    def _notify_backup_enabled(self, enabled: bool) -> None:
        self.backup_enabled_changed.emit(enabled)

    def _notify_backup_interval(self, seconds: int) -> None:
        self.backup_interval_changed.emit(seconds)

    backup_enabled: Setting[Self, bool] = Setting[Self, bool](
        _BACKUP_ENABLED_KEY,
        default=lambda: True,
        decode=read_bool,
        notify=_notify_backup_enabled,
    )

    backup_interval: Setting[Self, int] = Setting[Self, int](
        _BACKUP_INTERVAL_KEY,
        default=lambda: 60,
        decode=read_int,
        notify=_notify_backup_interval,
    )

    @property
    def nickname(self) -> str:
        # A cleared nickname stores @Invalid, which an untyped read cannot tell apart from a missing key
        if self.qsettings.contains(_NICKNAME_KEY):
            stored = self.qsettings.value(_NICKNAME_KEY, type=str)
            return stored if isinstance(stored, str) else ""
        return _default_username()

    @nickname.setter
    def nickname(self, nickname: str | None) -> None:
        self.qsettings.setValue(_NICKNAME_KEY, nickname)

    write_header_date: Setting[Self, bool] = Setting[Self, bool](
        _WRITE_HEADER_DATE_KEY,
        default=lambda: True,
        decode=read_bool,
    )

    write_header_generator: Setting[Self, bool] = Setting[Self, bool](
        _WRITE_HEADER_GENERATOR_KEY,
        default=lambda: True,
        decode=read_bool,
    )

    write_header_nickname: Setting[Self, bool] = Setting[Self, bool](
        _WRITE_HEADER_NICKNAME_KEY,
        default=lambda: False,
        decode=read_bool,
    )

    write_header_video_path: Setting[Self, bool] = Setting[Self, bool](
        _WRITE_HEADER_VIDEO_PATH_KEY,
        default=lambda: True,
        decode=read_bool,
    )

    write_header_subtitles: Setting[Self, bool] = Setting[Self, bool](
        _WRITE_HEADER_SUBTITLES_KEY,
        default=lambda: False,
        decode=read_bool,
    )
