# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import typing

import inject
from PySide6.QtCore import QAbstractListModel, QByteArray, Qt
from PySide6.QtQml import QmlElement

from mpvqc.services import ThemeService

if typing.TYPE_CHECKING:
    from typing import Any

    from PySide6.QtCore import QModelIndex, QPersistentModelIndex


QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcThemePreviewModel(QAbstractListModel):
    _themes = inject.attr(ThemeService)

    IdentifierRole = Qt.ItemDataRole.UserRole + 1
    PreviewRole = Qt.ItemDataRole.UserRole + 2

    @typing.override
    def rowCount(self, parent: QModelIndex | QPersistentModelIndex | None = None) -> int:
        return len(self._themes.previews)

    @typing.override
    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        preview = self._themes.previews[index.row()]

        match role:
            case self.IdentifierRole:
                return preview.identifier
            case self.PreviewRole:
                return preview.preview

        return None

    @typing.override
    def roleNames(self) -> dict[int, QByteArray]:
        return {
            self.IdentifierRole: QByteArray(b"identifier"),
            self.PreviewRole: QByteArray(b"preview"),
        }
