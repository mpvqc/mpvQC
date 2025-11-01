# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import typing

import inject
from PySide6.QtCore import QAbstractListModel, QByteArray, Qt, Signal
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
    _themes: ThemeService = inject.attr(ThemeService)
    _settings: SettingsService = inject.attr(SettingsService)

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

    def __init__(self, parent=None):
        super().__init__(parent)
        self._theme_identifier = self._settings.theme_identifier

        self._theme_changed_connection = self._settings.themeIdentifierChanged.connect(self._set_theme_identifier)
        self.destroyed.connect(lambda: self._settings.themeIdentifierChanged.disconnect(self._theme_changed_connection))

    def _set_theme_identifier(self, theme_identifier: str) -> None:
        self._theme_identifier = theme_identifier
        self.aboutToReset.emit()
        self.beginResetModel()
        self.endResetModel()
        self.resetDone.emit()

    def rowCount(self, parent: QModelIndex | QPersistentModelIndex = ...) -> int:  # noqa: ARG002
        return len(self._themes.palette(self._theme_identifier))

    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = ...) -> Any:  # noqa: C901
        theme = self._themes.palette(self._theme_identifier)
        if not index.isValid() or index.row() >= len(theme):
            return None
        palette = theme[index.row()]

        match role:
            case self.BackgroundRole:
                return palette["background"]
            case self.BackgroundAlternateRole:
                return palette["backgroundAlternate"]
            case self.ForegroundRole:
                return palette["foreground"]
            case self.ForegroundAlternateRole:
                return palette["foregroundAlternate"]
            case self.ControlRole:
                return palette["control"]
            case self.RowHighlightRole:
                return palette["rowHighlight"]
            case self.RowHighlightTextRole:
                return palette["rowHighlightText"]
            case self.RowBaseRole:
                return palette["rowBase"]
            case self.RowBaseTextRole:
                return palette["rowBaseText"]
            case self.RowBaseAlternateRole:
                return palette["rowBaseAlternate"]
            case self.RowBaseAlternateTextRole:
                return palette["rowBaseAlternateText"]

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
