# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, assert_never, override

from PySide6.QtCore import Property, QAbstractItemModel, QAbstractListModel, QByteArray, QCoreApplication, QObject, Qt
from PySide6.QtQml import QmlElement, QmlUncreatable

from mpvqc.datamodels import DocumentRejectionReason
from mpvqc.services.importer import errors

if TYPE_CHECKING:
    from typing import Any

    from PySide6.QtCore import QModelIndex, QPersistentModelIndex

    from mpvqc.datamodels import RejectedDocument


QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


class MpvqcImportErrorsModel(QAbstractListModel):
    FilenameRole = Qt.ItemDataRole.UserRole + 1
    FullPathRole = Qt.ItemDataRole.UserRole + 2
    ReasonRole = Qt.ItemDataRole.UserRole + 3

    def __init__(self, documents: tuple[RejectedDocument, ...]) -> None:
        super().__init__()
        self._documents = documents

    @override
    def rowCount(self, parent: QModelIndex | QPersistentModelIndex | None = None) -> int:
        return len(self._documents)

    @override
    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid() or index.row() >= self.rowCount():
            return None

        rejected = self._documents[index.row()]

        match role:
            case self.FilenameRole:
                return rejected.path.name
            case self.FullPathRole:
                return str(rejected.path)
            case self.ReasonRole:
                return _reason_text(rejected.reason)

        return None

    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return {
            self.FilenameRole: QByteArray(b"filename"),
            self.FullPathRole: QByteArray(b"fullPath"),
            self.ReasonRole: QByteArray(b"reason"),
        }


@QmlElement
@QmlUncreatable("constructed by MpvqcImportWizardViewModel")
class MpvqcImportWizardErrorsStepViewModel(QObject):
    def __init__(self, parent: QObject, inputs: errors.Present) -> None:
        super().__init__(parent)
        self._documents = MpvqcImportErrorsModel(inputs.rejected_documents)

    @Property(QAbstractItemModel, constant=True, final=True)
    def documents(self) -> MpvqcImportErrorsModel:
        return self._documents


def build_errors_step(parent: QObject, concern: errors.Concern) -> MpvqcImportWizardErrorsStepViewModel | None:
    if isinstance(concern, errors.Present):
        return MpvqcImportWizardErrorsStepViewModel(parent, concern)
    return None


def _reason_text(reason: DocumentRejectionReason) -> str:
    match reason:
        case DocumentRejectionReason.UNSUPPORTED_VERSION:
            #: Shown beneath a rejected document declaring a format version this mpvQC release does not know
            return QCoreApplication.translate("ImportWizardDialog", "Unsupported document format version")
        case DocumentRejectionReason.INVALID:
            #: Shown beneath a rejected document that does not parse as any known QC document format
            return QCoreApplication.translate("ImportWizardDialog", "Not a valid QC document")
        case _ as unreachable:
            assert_never(unreachable)
