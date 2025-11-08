# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import typing

import inject
from PySide6.QtCore import QAbstractListModel, QByteArray, Qt
from PySide6.QtQml import QmlElement

from mpvqc.services import BuildInfoService

if typing.TYPE_CHECKING:
    from typing import Any

    from PySide6.QtCore import QModelIndex, QPersistentModelIndex

    from mpvqc.build_info import Dependency


QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcDependencyModel(QAbstractListModel):
    _build_info: BuildInfoService = inject.attr(BuildInfoService)

    NameRole = Qt.ItemDataRole.UserRole + 1
    PackageRole = Qt.ItemDataRole.UserRole + 2
    VersionRole = Qt.ItemDataRole.UserRole + 3
    UrlRole = Qt.ItemDataRole.UserRole + 4
    LicenceRole = Qt.ItemDataRole.UserRole + 5

    def __init__(self, parent=None):
        super().__init__(parent)
        self._all_dependencies: list[Dependency] = [
            *self._build_info.dependencies,
            *self._build_info.dev_dependencies,
        ]

    def rowCount(self, parent: QModelIndex | QPersistentModelIndex = ...) -> int:  # noqa: ARG002
        return len(self._all_dependencies)

    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = ...) -> Any:
        if not index.isValid() or index.row() >= len(self._all_dependencies):
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
            case _:
                msg = f"Cannot find data to return for: {type(role)} {role}"
                raise ValueError(msg)

    def roleNames(self) -> dict[int, QByteArray]:
        return {
            self.NameRole: QByteArray(b"name"),
            self.PackageRole: QByteArray(b"package"),
            self.VersionRole: QByteArray(b"version"),
            self.UrlRole: QByteArray(b"url"),
            self.LicenceRole: QByteArray(b"licence"),
        }
