# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import operator
import typing

import inject
from PySide6.QtCore import Property, QAbstractListModel, QByteArray, Qt
from PySide6.QtQml import QmlElement

from mpvqc.services import ApplicationPathsService, TypeMapperService

if typing.TYPE_CHECKING:
    from typing import Any

    from PySide6.QtCore import QModelIndex, QPersistentModelIndex


QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcExportTemplateModel(QAbstractListModel):
    _app_paths: ApplicationPathsService = inject.attr(ApplicationPathsService)
    _type_mapper: TypeMapperService = inject.attr(TypeMapperService)

    NameRole = Qt.ItemDataRole.UserRole + 1
    PathRole = Qt.ItemDataRole.UserRole + 2

    def __init__(self) -> None:
        super().__init__()
        self._items = []

        for template in self._app_paths.files_export_templates:
            url = self._type_mapper.map_path_to_url(template)
            self._items.append(
                {
                    "name": template.stem,
                    "path": url,
                }
            )

        self._items.sort(key=operator.itemgetter("name"))

    @Property(int, constant=True, final=True)
    def count(self) -> int:
        return len(self._items)

    def rowCount(self, parent: QModelIndex | QPersistentModelIndex | None = None) -> int:  # noqa: ARG002
        return len(self._items)

    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid() or index.row() >= len(self._items):
            return None

        item = self._items[index.row()]

        if role == self.NameRole:
            return item["name"]
        if role == self.PathRole:
            return item["path"]

        return None

    def roleNames(self) -> dict[int, QByteArray]:
        return {
            self.NameRole: QByteArray(b"name"),
            self.PathRole: QByteArray(b"path"),
        }
