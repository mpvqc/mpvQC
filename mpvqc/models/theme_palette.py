# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import typing

import inject
from PySide6.QtCore import QAbstractListModel, QByteArray, Qt, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import SettingsService, ThemeService

if typing.TYPE_CHECKING:
    from typing import Any

    from PySide6.QtCore import QModelIndex, QPersistentModelIndex

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyTypeChecker,PyPep8Naming
@QmlElement
class MpvqcThemePaletteModel(QAbstractListModel):
    _themes = inject.attr(ThemeService)
    _settings = inject.attr(SettingsService)

    BackgroundRole = Qt.ItemDataRole.UserRole + 1
    BackgroundAlternateRole = Qt.ItemDataRole.UserRole + 2
    ForegroundRole = Qt.ItemDataRole.UserRole + 3
    ForegroundAlternateRole = Qt.ItemDataRole.UserRole + 4
    ControlRole = Qt.ItemDataRole.UserRole + 5
    RowHighlightRole = Qt.ItemDataRole.UserRole + 6
    RowHighlightTextRole = Qt.ItemDataRole.UserRole + 7
    RowBaseRole = Qt.ItemDataRole.UserRole + 8
    RowBaseTextRole = Qt.ItemDataRole.UserRole + 9
    RowBaseAlternateRole = Qt.ItemDataRole.UserRole + 10
    RowBaseAlternateTextRole = Qt.ItemDataRole.UserRole + 11

    aboutToReset = Signal()
    resetDone = Signal()

    themeIdentifierChanged = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._theme_identifier = self._settings.theme_identifier

        self._theme_changed_connection = self._settings.themeIdentifierChanged.connect(self._set_theme_identifier)
        self.destroyed.connect(lambda: self._settings.themeIdentifierChanged.disconnect(self._theme_changed_connection))

    @Slot(str)
    def _set_theme_identifier(self, theme_identifier: str) -> None:
        self._theme_identifier = theme_identifier
        self.aboutToReset.emit()
        self.beginResetModel()
        self.endResetModel()
        self.resetDone.emit()

    @typing.override
    def rowCount(self, parent: QModelIndex | QPersistentModelIndex | None = None) -> int:
        return self._themes.theme(self._theme_identifier).palette_count

    @typing.override
    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:  # noqa: C901
        if not index.isValid() or index.row() >= self.rowCount():
            return None

        palette = self._themes.palette_at(self._theme_identifier, index.row())

        match role:
            case self.BackgroundRole:
                return palette.background
            case self.BackgroundAlternateRole:
                return palette.background_alternate
            case self.ForegroundRole:
                return palette.foreground
            case self.ForegroundAlternateRole:
                return palette.foreground_alternate
            case self.ControlRole:
                return palette.control
            case self.RowHighlightRole:
                return palette.row_highlight
            case self.RowHighlightTextRole:
                return palette.row_highlight_text
            case self.RowBaseRole:
                return palette.row_base
            case self.RowBaseTextRole:
                return palette.row_base_text
            case self.RowBaseAlternateRole:
                return palette.row_base_alternate
            case self.RowBaseAlternateTextRole:
                return palette.row_base_alternate_text

    @typing.override
    def roleNames(self) -> dict[int, QByteArray]:
        return {
            self.BackgroundRole: QByteArray(b"background"),
            self.BackgroundAlternateRole: QByteArray(b"backgroundAlternate"),
            self.ForegroundRole: QByteArray(b"foreground"),
            self.ForegroundAlternateRole: QByteArray(b"foregroundAlternate"),
            self.ControlRole: QByteArray(b"control"),
            self.RowHighlightRole: QByteArray(b"rowHighlight"),
            self.RowHighlightTextRole: QByteArray(b"rowHighlightText"),
            self.RowBaseRole: QByteArray(b"rowBase"),
            self.RowBaseTextRole: QByteArray(b"rowBaseText"),
            self.RowBaseAlternateRole: QByteArray(b"rowBaseAlternate"),
            self.RowBaseAlternateTextRole: QByteArray(b"rowBaseAlternateText"),
        }
