# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, override

from PySide6.QtCore import Property, QAbstractItemModel, QAbstractListModel, QByteArray, QObject, Qt
from PySide6.QtQml import QmlElement, QmlUncreatable

from mpvqc.services.importer import errors

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Any

    from PySide6.QtCore import QModelIndex, QPersistentModelIndex


QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


class MpvqcImportErrorsModel(QAbstractListModel):
    FilenameRole = Qt.ItemDataRole.UserRole + 1
    FullPathRole = Qt.ItemDataRole.UserRole + 2

    def __init__(self, documents: tuple[Path, ...]) -> None:
        super().__init__()
        self._documents = documents

    @override
    def rowCount(self, parent: QModelIndex | QPersistentModelIndex | None = None) -> int:
        return len(self._documents)

    @override
    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid() or index.row() >= self.rowCount():
            return None

        path = self._documents[index.row()]

        match role:
            case self.FilenameRole:
                return path.name
            case self.FullPathRole:
                return str(path)

        return None

    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return {
            self.FilenameRole: QByteArray(b"filename"),
            self.FullPathRole: QByteArray(b"fullPath"),
        }


@QmlElement
@QmlUncreatable("constructed by MpvqcImportWizardViewModel")
class MpvqcImportWizardErrorsStepViewModel(QObject):
    def __init__(self, parent: QObject, inputs: errors.Unresolved) -> None:
        super().__init__(parent)
        self._documents = MpvqcImportErrorsModel(inputs.invalid_documents)

    @Property(QAbstractItemModel, constant=True, final=True)
    def documents(self) -> MpvqcImportErrorsModel:
        return self._documents


def build_errors_step(parent: QObject, concern: errors.Concern) -> MpvqcImportWizardErrorsStepViewModel | None:
    if isinstance(concern, errors.Unresolved):
        return MpvqcImportWizardErrorsStepViewModel(parent, concern)
    return None
