# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, override

from PySide6.QtCore import QAbstractListModel, QByteArray, QCoreApplication, Qt
from PySide6.QtQml import QmlElement

from mpvqc.enums import ImportFoundVideo

if TYPE_CHECKING:
    from typing import Any

    from PySide6.QtCore import QModelIndex, QPersistentModelIndex


QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class ImportOptionsModel(QAbstractListModel):
    """Model to display in the import settings dialog to let the user choose if found videos should be opened"""

    TextRole = Qt.ItemDataRole.UserRole + 1
    ValueRole = Qt.ItemDataRole.UserRole + 2

    def __init__(self) -> None:
        super().__init__()
        self._items = [
            {
                "text": QCoreApplication.translate("ImportSettingsDialog", "Always"),
                "value": ImportFoundVideo.ALWAYS.value,
            },
            {
                "text": QCoreApplication.translate("ImportSettingsDialog", "Ask every time"),
                "value": ImportFoundVideo.ASK_EVERY_TIME.value,
            },
            {
                "text": QCoreApplication.translate("ImportSettingsDialog", "Never"),
                "value": ImportFoundVideo.NEVER.value,
            },
        ]

    @override
    def rowCount(self, parent: QModelIndex | QPersistentModelIndex | None = None) -> int:
        return len(self._items)

    @override
    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid() or index.row() >= self.rowCount():
            return None

        item = self._items[index.row()]

        match role:
            case self.TextRole:
                return item["text"]
            case self.ValueRole:
                return item["value"]

        return None

    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return {
            self.TextRole: QByteArray(b"text"),
            self.ValueRole: QByteArray(b"value"),
        }
