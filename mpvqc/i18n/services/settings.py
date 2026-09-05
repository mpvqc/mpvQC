# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal

from .languages import default_language

if TYPE_CHECKING:
    from PySide6.QtCore import QSettings

_LANGUAGE_KEY = "Common/language"


class I18nSettingsService(QObject):
    language_changed = Signal(str)

    def __init__(self, qsettings: QSettings, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._qsettings = qsettings

    @property
    def language(self) -> str:
        # A typed read of a missing key hands back "", never None
        if not self._qsettings.contains(_LANGUAGE_KEY):
            return default_language()
        stored = self._qsettings.value(_LANGUAGE_KEY, type=str)
        return stored if isinstance(stored, str) else default_language()

    @language.setter
    def language(self, language: str) -> None:
        if self.language == language:
            return
        self._qsettings.setValue(_LANGUAGE_KEY, language)
        self.language_changed.emit(language)
