# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from PySide6.QtCore import QAbstractListModel, QCoreApplication, QModelIndex, Qt
from PySide6.QtQml import QmlElement

from mpvqc.services import SettingsService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class ImportOptionsModel(QAbstractListModel):
    """Model to display in the import settings dialog to let the user choose if found videos should be opened"""

    TextRole = Qt.ItemDataRole.UserRole + 1
    ValueRole = Qt.ItemDataRole.UserRole + 2

    def __init__(self):
        super().__init__()
        self._items = [
            {
                "text": QCoreApplication.translate("ImportSettingsDialog", "Always"),
                "value": SettingsService.ImportFoundVideo.ALWAYS.value,
            },
            {
                "text": QCoreApplication.translate("ImportSettingsDialog", "Ask every time"),
                "value": SettingsService.ImportFoundVideo.ASK_EVERY_TIME.value,
            },
            {
                "text": QCoreApplication.translate("ImportSettingsDialog", "Never"),
                "value": SettingsService.ImportFoundVideo.NEVER.value,
            },
        ]

    def rowCount(self, _=QModelIndex()) -> int:
        return len(self._items)

    def data(self, index: QModelIndex, /, role: int = ...):
        if not index.isValid():
            return None

        item = self._items[index.row()]

        if role == self.TextRole:
            return item["text"]
        if role == self.ValueRole:
            return item["value"]

        return None

    def roleNames(self) -> dict:
        return {self.TextRole: b"text", self.ValueRole: b"value"}
