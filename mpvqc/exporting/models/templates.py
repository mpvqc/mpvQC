# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, override

import inject
from PySide6.QtCore import Property, QAbstractListModel, QByteArray, Qt
from PySide6.QtQml import QmlElement

from mpvqc.exporting.services import ExportTemplateCatalogService
from mpvqc.shared import map_path_to_url

if TYPE_CHECKING:
    from typing import Any

    from PySide6.QtCore import QModelIndex, QPersistentModelIndex, QUrl


QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@dataclass(frozen=True, slots=True)
class _TemplateEntry:
    name: str
    url: QUrl


@QmlElement
class MpvqcExportTemplateModel(QAbstractListModel):
    _catalog = inject.attr(ExportTemplateCatalogService)

    NameRole = Qt.ItemDataRole.UserRole + 1
    PathRole = Qt.ItemDataRole.UserRole + 2

    def __init__(self) -> None:
        super().__init__()
        self._items = [
            _TemplateEntry(name=template.name, url=map_path_to_url(template.path))
            for template in self._catalog.list_templates()
        ]

    @Property(int, constant=True, final=True)
    def count(self) -> int:
        return len(self._items)

    @override
    def rowCount(self, parent: QModelIndex | QPersistentModelIndex | None = None) -> int:
        if parent is not None and parent.isValid():
            return 0
        return len(self._items)

    @override
    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        items = self._items
        if not index.isValid() or index.row() >= len(items):
            return None

        item = items[index.row()]

        match role:
            case self.NameRole:
                return item.name
            case self.PathRole:
                return item.url

        return None

    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return {
            self.NameRole: QByteArray(b"name"),
            self.PathRole: QByteArray(b"path"),
        }
