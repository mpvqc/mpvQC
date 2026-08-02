# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, assert_never, override

import inject
from PySide6.QtCore import QAbstractListModel, QByteArray, QModelIndex, Qt
from PySide6.QtQml import QmlElement, QmlUncreatable

from mpvqc.appearance.domain import Dark, FollowSystem, Light
from mpvqc.appearance.services import PaletteCatalogService

if TYPE_CHECKING:
    from typing import Any

    from PySide6.QtCore import QObject, QPersistentModelIndex

    from mpvqc.appearance.domain import ColorSchemePreference, Palette

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
@QmlUncreatable("constructed by MpvqcAppearanceDialogViewModel")
class MpvqcAccentColorModel(QAbstractListModel):
    """The accent color set belongs to an explicit color scheme preference; following the system owns none."""

    _catalog = inject.attr(PaletteCatalogService)

    AccentColorRole = Qt.ItemDataRole.UserRole + 1
    DisplayColorRole = Qt.ItemDataRole.UserRole + 2

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._preference: ColorSchemePreference = FollowSystem()

    def set_preference(self, preference: ColorSchemePreference) -> None:
        if preference == self._preference:
            return

        old_count = self.rowCount()
        new_count = len(self._palettes_of(preference))

        if new_count > old_count:
            self.beginInsertRows(QModelIndex(), old_count, new_count - 1)
            self._preference = preference
            self.endInsertRows()
        elif new_count < old_count:
            self.beginRemoveRows(QModelIndex(), new_count, old_count - 1)
            self._preference = preference
            self.endRemoveRows()
        else:
            self._preference = preference

        overlap = min(old_count, new_count)
        if overlap > 0:
            first = self.index(0)
            last = self.index(overlap - 1)
            self.dataChanged.emit(first, last, [self.AccentColorRole, self.DisplayColorRole])

    def _palettes_of(self, preference: ColorSchemePreference) -> tuple[Palette, ...]:
        match preference:
            case FollowSystem():
                return ()
            case Light() | Dark():
                return self._catalog.palette_family_for(preference).palettes
            case _:
                assert_never(preference)

    @override
    def rowCount(self, parent: QModelIndex | QPersistentModelIndex | None = None) -> int:
        if parent is not None and parent.isValid():
            return 0
        return len(self._palettes_of(self._preference))

    @override
    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        palettes = self._palettes_of(self._preference)
        if not index.isValid() or index.row() >= len(palettes):
            return None

        palette = palettes[index.row()]

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
