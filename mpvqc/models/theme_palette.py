# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt, Signal
from PySide6.QtQml import QmlElement

from mpvqc.services import SettingsService, ThemeService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyTypeChecker,PyPep8Naming
@QmlElement
class MpvqcThemePaletteModel(QAbstractListModel):
    _themes: ThemeService = inject.attr(ThemeService)
    _settings: SettingsService = inject.attr(SettingsService)

    BackgroundRole = Qt.ItemDataRole.UserRole + 1
    ForegroundRole = Qt.ItemDataRole.UserRole + 2
    ControlRole = Qt.ItemDataRole.UserRole + 3
    RowHighlightRole = Qt.ItemDataRole.UserRole + 4
    RowHighlightTextRole = Qt.ItemDataRole.UserRole + 5
    RowBaseRole = Qt.ItemDataRole.UserRole + 6
    RowBaseTextRole = Qt.ItemDataRole.UserRole + 7
    RowBaseAlternateRole = Qt.ItemDataRole.UserRole + 8
    RowBaseAlternateTextRole = Qt.ItemDataRole.UserRole + 9

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

    def rowCount(self, _=QModelIndex()):
        return len(self._themes.palette(self._theme_identifier))

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):  # noqa: C901
        theme = self._themes.palette(self._theme_identifier)
        if not index.isValid() or index.row() >= len(theme):
            return None
        palette = theme[index.row()]

        match role:
            case self.BackgroundRole:
                return palette["background"]
            case self.ForegroundRole:
                return palette["foreground"]
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

    def roleNames(self):
        return {
            self.BackgroundRole: b"background",
            self.ForegroundRole: b"foreground",
            self.ControlRole: b"control",
            self.RowHighlightRole: b"rowHighlight",
            self.RowHighlightTextRole: b"rowHighlightText",
            self.RowBaseRole: b"rowBase",
            self.RowBaseTextRole: b"rowBaseText",
            self.RowBaseAlternateRole: b"rowBaseAlternate",
            self.RowBaseAlternateTextRole: b"rowBaseAlternateText",
        }
