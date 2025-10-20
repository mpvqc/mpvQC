# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt
from PySide6.QtQml import QmlElement

from mpvqc.services import ThemeService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcThemePreviewModel(QAbstractListModel):
    _themes: ThemeService = inject.attr(ThemeService)

    IdentifierRole = Qt.ItemDataRole.UserRole + 1
    NameRole = Qt.ItemDataRole.UserRole + 2
    PreviewRole = Qt.ItemDataRole.UserRole + 3
    IsDarkRole = Qt.ItemDataRole.UserRole + 4

    def rowCount(self, _=QModelIndex()):
        return len(self._themes.previews)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        preview = self._themes.previews[index.row()]

        match role:
            case self.IdentifierRole:
                return preview["identifier"]
            case self.NameRole | Qt.ItemDataRole.DisplayRole:
                return preview["name"]
            case self.PreviewRole:
                return preview["preview"]
            case self.IsDarkRole:
                return preview["isDark"]

    def roleNames(self):
        return {
            self.IdentifierRole: b"identifier",
            self.NameRole: b"name",
            self.PreviewRole: b"preview",
            self.IsDarkRole: b"isDark",
        }
