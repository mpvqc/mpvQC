# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import os
from contextlib import suppress
from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal

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


# Until something writes the key this run, an untyped read hands back the ini text, never the type that was stored
def _read_bool(stored: object, default: bool) -> bool:
    if isinstance(stored, bool):
        return stored
    if isinstance(stored, str) and stored.lower() in {"true", "false"}:
        return stored.lower() == "true"
    return default


def _read_int(stored: object, default: int) -> int:
    if isinstance(stored, bool):
        return default
    if isinstance(stored, int):
        return stored
    if isinstance(stored, str):
        with suppress(ValueError):
            return int(stored)
    return default


class ExportSettingsService(QObject):
    backup_enabled_changed = Signal(bool)
    backup_interval_changed = Signal(int)

    def __init__(self, qsettings: QSettings, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._qsettings = qsettings

    @property
    def backup_enabled(self) -> bool:
        return _read_bool(self._qsettings.value(_BACKUP_ENABLED_KEY), default=True)

    @backup_enabled.setter
    def backup_enabled(self, enabled: bool) -> None:
        if self.backup_enabled == enabled:
            return
        self._qsettings.setValue(_BACKUP_ENABLED_KEY, enabled)
        self.backup_enabled_changed.emit(enabled)

    @property
    def backup_interval(self) -> int:
        return _read_int(self._qsettings.value(_BACKUP_INTERVAL_KEY), default=60)

    @backup_interval.setter
    def backup_interval(self, seconds: int) -> None:
        if self.backup_interval == seconds:
            return
        self._qsettings.setValue(_BACKUP_INTERVAL_KEY, seconds)
        self.backup_interval_changed.emit(seconds)

    @property
    def nickname(self) -> str:
        # A cleared nickname stores @Invalid, which an untyped read cannot tell apart from a missing key
        if self._qsettings.contains(_NICKNAME_KEY):
            stored = self._qsettings.value(_NICKNAME_KEY, type=str)
            return stored if isinstance(stored, str) else ""
        return _default_username()

    @nickname.setter
    def nickname(self, nickname: str | None) -> None:
        self._qsettings.setValue(_NICKNAME_KEY, nickname)

    @property
    def write_header_date(self) -> bool:
        return _read_bool(self._qsettings.value(_WRITE_HEADER_DATE_KEY), default=True)

    @write_header_date.setter
    def write_header_date(self, write: bool) -> None:
        self._qsettings.setValue(_WRITE_HEADER_DATE_KEY, write)

    @property
    def write_header_generator(self) -> bool:
        return _read_bool(self._qsettings.value(_WRITE_HEADER_GENERATOR_KEY), default=True)

    @write_header_generator.setter
    def write_header_generator(self, write: bool) -> None:
        self._qsettings.setValue(_WRITE_HEADER_GENERATOR_KEY, write)

    @property
    def write_header_nickname(self) -> bool:
        return _read_bool(self._qsettings.value(_WRITE_HEADER_NICKNAME_KEY), default=False)

    @write_header_nickname.setter
    def write_header_nickname(self, write: bool) -> None:
        self._qsettings.setValue(_WRITE_HEADER_NICKNAME_KEY, write)

    @property
    def write_header_video_path(self) -> bool:
        return _read_bool(self._qsettings.value(_WRITE_HEADER_VIDEO_PATH_KEY), default=True)

    @write_header_video_path.setter
    def write_header_video_path(self, write: bool) -> None:
        self._qsettings.setValue(_WRITE_HEADER_VIDEO_PATH_KEY, write)

    @property
    def write_header_subtitles(self) -> bool:
        return _read_bool(self._qsettings.value(_WRITE_HEADER_SUBTITLES_KEY), default=False)

    @write_header_subtitles.setter
    def write_header_subtitles(self, write: bool) -> None:
        self._qsettings.setValue(_WRITE_HEADER_SUBTITLES_KEY, write)
