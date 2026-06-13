# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, override

import inject
from PySide6.QtCore import QAbstractListModel, QByteArray, Qt
from PySide6.QtQml import QmlElement

from mpvqc.services import ThemeService

if TYPE_CHECKING:
    from typing import Any

    from PySide6.QtCore import QModelIndex, QPersistentModelIndex


QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcThemePreviewModel(QAbstractListModel):
    _themes = inject.attr(ThemeService)

    IdentifierRole = Qt.ItemDataRole.UserRole + 1
    PreviewRole = Qt.ItemDataRole.UserRole + 2

    @override
    def rowCount(self, parent: QModelIndex | QPersistentModelIndex | None = None) -> int:
        if parent is not None and parent.isValid():
            return 0
        return len(self._themes.previews)

    @override
    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid() or index.row() >= self.rowCount():
            return None

        preview = self._themes.previews[index.row()]

        match role:
            case self.IdentifierRole:
                return preview.identifier
            case self.PreviewRole:
                return preview.preview

        return None

    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return {
            self.IdentifierRole: QByteArray(b"identifier"),
            self.PreviewRole: QByteArray(b"preview"),
        }
