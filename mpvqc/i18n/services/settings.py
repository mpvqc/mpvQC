# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, Self

from PySide6.QtCore import QObject, Signal

from mpvqc.services import Setting, stored_text

from .languages import default_language

if TYPE_CHECKING:
    from PySide6.QtCore import QSettings


class I18nSettingsService(QObject):
    language_changed = Signal(str)

    def __init__(self, qsettings: QSettings, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.qsettings = qsettings

    def _notify_language(self, language: str) -> None:
        self.language_changed.emit(language)

    language: Setting[Self, str] = Setting[Self, str](
        "Common/language",
        default=default_language,
        read=stored_text,
        decode=lambda stored, default: stored if isinstance(stored, str) else default(),
        notify=_notify_language,
    )
