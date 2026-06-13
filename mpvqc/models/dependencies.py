# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, override

import inject
from PySide6.QtCore import QAbstractListModel, QByteArray, Qt
from PySide6.QtQml import QmlElement

from mpvqc.services import BuildInfoService

if TYPE_CHECKING:
    from typing import Any

    from PySide6.QtCore import QModelIndex, QObject, QPersistentModelIndex

    from mpvqc.build import Dependency


QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcDependencyModel(QAbstractListModel):
    _build_info = inject.attr(BuildInfoService)

    NameRole = Qt.ItemDataRole.UserRole + 1
    PackageRole = Qt.ItemDataRole.UserRole + 2
    VersionRole = Qt.ItemDataRole.UserRole + 3
    UrlRole = Qt.ItemDataRole.UserRole + 4
    LicenceRole = Qt.ItemDataRole.UserRole + 5

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._all_dependencies: list[Dependency] = [
            *self._build_info.dependencies,
            *self._build_info.dev_dependencies,
        ]

    @override
    def rowCount(self, parent: QModelIndex | QPersistentModelIndex | None = None) -> int:
        if parent is not None and parent.isValid():
            return 0
        return len(self._all_dependencies)

    @override
    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid() or index.row() >= self.rowCount():
            return None

        dependency = self._all_dependencies[index.row()]

        match role:
            case self.NameRole:
                return dependency.name
            case self.PackageRole:
                return dependency.package
            case self.VersionRole:
                return dependency.version
            case self.UrlRole:
                return dependency.url
            case self.LicenceRole:
                return dependency.licence

        return None

    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return {
            self.NameRole: QByteArray(b"name"),
            self.PackageRole: QByteArray(b"package"),
            self.VersionRole: QByteArray(b"version"),
            self.UrlRole: QByteArray(b"url"),
            self.LicenceRole: QByteArray(b"licence"),
        }
