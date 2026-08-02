# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, override

import inject
from PySide6.QtCore import QAbstractListModel, QByteArray, QModelIndex, Qt
from PySide6.QtQml import QmlElement, QmlUncreatable

from mpvqc.services import PaletteCatalogService

if TYPE_CHECKING:
    from typing import Any

    from PySide6.QtCore import QObject, QPersistentModelIndex

    from mpvqc.appearance import ColorScheme

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
@QmlUncreatable("constructed by MpvqcAppearanceDialogViewModel")
class MpvqcAccentColorModel(QAbstractListModel):
    """The accent colors of one color scheme's palette family, empty while no scheme is set."""

    _catalog = inject.attr(PaletteCatalogService)

    AccentColorRole = Qt.ItemDataRole.UserRole + 1
    DisplayColorRole = Qt.ItemDataRole.UserRole + 2

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._color_scheme: ColorScheme | None = None

    def set_color_scheme(self, color_scheme: ColorScheme | None) -> None:
        if color_scheme == self._color_scheme:
            return

        old_count = self.rowCount()
        new_count = self._palette_count_of(color_scheme)

        if new_count > old_count:
            self.beginInsertRows(QModelIndex(), old_count, new_count - 1)
            self._color_scheme = color_scheme
            self.endInsertRows()
        elif new_count < old_count:
            self.beginRemoveRows(QModelIndex(), new_count, old_count - 1)
            self._color_scheme = color_scheme
            self.endRemoveRows()
        else:
            self._color_scheme = color_scheme

        overlap = min(old_count, new_count)
        if overlap > 0:
            first = self.index(0)
            last = self.index(overlap - 1)
            self.dataChanged.emit(first, last, [self.AccentColorRole, self.DisplayColorRole])

    def _palette_count_of(self, color_scheme: ColorScheme | None) -> int:
        if color_scheme is None:
            return 0
        return self._catalog.palette_family_for(color_scheme).palette_count

    @override
    def rowCount(self, parent: QModelIndex | QPersistentModelIndex | None = None) -> int:
        if parent is not None and parent.isValid():
            return 0
        return self._palette_count_of(self._color_scheme)

    @override
    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid() or index.row() >= self.rowCount() or self._color_scheme is None:
            return None

        palette = self._catalog.palette_family_for(self._color_scheme).palettes[index.row()]

        match role:
            case self.AccentColorRole:
                return palette.accent_color.identifier
            case self.DisplayColorRole:
                return palette.row_selected

        return None

    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return {
            self.AccentColorRole: QByteArray(b"accentColor"),
            self.DisplayColorRole: QByteArray(b"displayColor"),
        }
