# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, override

import inject
from PySide6.QtCore import QAbstractListModel, QByteArray, QModelIndex, Qt, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import SettingsService, ThemeService

if TYPE_CHECKING:
    from typing import Any

    from PySide6.QtCore import QObject, QPersistentModelIndex

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcPrimaryColorModel(QAbstractListModel):
    _themes = inject.attr(ThemeService)
    _settings = inject.attr(SettingsService)

    IdentifierRole = Qt.ItemDataRole.UserRole + 1
    DisplayColorRole = Qt.ItemDataRole.UserRole + 2

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._theme_identifier = self._settings.theme_identifier
        self._settings.theme_identifier_changed.connect(self._set_theme_identifier)

    @Slot(str)
    def _set_theme_identifier(self, theme_identifier: str) -> None:
        old_count = self.rowCount()
        new_count = self._themes.theme(theme_identifier).palette_count

        if new_count > old_count:
            self.beginInsertRows(QModelIndex(), old_count, new_count - 1)
            self._theme_identifier = theme_identifier
            self.endInsertRows()
        elif new_count < old_count:
            self.beginRemoveRows(QModelIndex(), new_count, old_count - 1)
            self._theme_identifier = theme_identifier
            self.endRemoveRows()
        else:
            self._theme_identifier = theme_identifier

        overlap = min(old_count, new_count)
        if overlap > 0:
            first = self.index(0)
            last = self.index(overlap - 1)
            self.dataChanged.emit(first, last, [self.IdentifierRole, self.DisplayColorRole])

    @override
    def rowCount(self, parent: QModelIndex | QPersistentModelIndex | None = None) -> int:
        if parent is not None and parent.isValid():
            return 0
        return self._themes.theme(self._theme_identifier).palette_count

    @override
    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid() or index.row() >= self.rowCount():
            return None

        palette = self._themes.theme(self._theme_identifier).palettes[index.row()]

        match role:
            case self.IdentifierRole:
                return palette.identifier
            case self.DisplayColorRole:
                return palette.row_selected

        return None

    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return {
            self.IdentifierRole: QByteArray(b"identifier"),
            self.DisplayColorRole: QByteArray(b"displayColor"),
        }
