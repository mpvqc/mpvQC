# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import typing

import inject
from PySide6.QtCore import QAbstractListModel, QByteArray, Qt, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import SettingsService, ThemeService

if typing.TYPE_CHECKING:
    from typing import Any

    from PySide6.QtCore import QModelIndex, QObject, QPersistentModelIndex

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyTypeChecker,PyPep8Naming
@QmlElement
class MpvqcThemeColorOptionsModel(QAbstractListModel):
    _themes = inject.attr(ThemeService)
    _settings = inject.attr(SettingsService)

    DisplayColorRole = Qt.ItemDataRole.UserRole + 1

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._theme_identifier = self._settings.theme_identifier
        self._settings.theme_identifier_changed.connect(self._set_theme_identifier)

    @Slot(str)
    def _set_theme_identifier(self, theme_identifier: str) -> None:
        self._theme_identifier = theme_identifier
        row_count = self.rowCount()
        if row_count == 0:
            return
        first = self.index(0)
        last = self.index(row_count - 1)
        self.dataChanged.emit(first, last, [self.DisplayColorRole])

    @typing.override
    def rowCount(self, parent: QModelIndex | QPersistentModelIndex | None = None) -> int:
        return self._themes.theme(self._theme_identifier).palette_count

    @typing.override
    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid() or index.row() >= self.rowCount():
            return None

        if role == self.DisplayColorRole:
            return self._themes.palette_at(self._theme_identifier, index.row()).row_highlight

        return None

    @typing.override
    def roleNames(self) -> dict[int, QByteArray]:
        return {
            self.DisplayColorRole: QByteArray(b"displayColor"),
        }
