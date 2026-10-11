# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, assert_never, override

from PySide6.QtCore import QAbstractListModel, QByteArray, QCoreApplication, Qt

from mpvqc.importing.services import DocumentMalformed, DocumentUnreadable, DocumentVersionUnsupported

if TYPE_CHECKING:
    from typing import Any

    from PySide6.QtCore import QModelIndex, QPersistentModelIndex

    from mpvqc.importing.services import DocumentRejection, RejectedDocument


class ErrorsModel(QAbstractListModel):
    FilenameRole = Qt.ItemDataRole.UserRole + 1
    FullPathRole = Qt.ItemDataRole.UserRole + 2
    ReasonRole = Qt.ItemDataRole.UserRole + 3

    def __init__(self, documents: tuple[RejectedDocument, ...]) -> None:
        super().__init__()
        self._documents = documents

    @override
    def rowCount(self, parent: QModelIndex | QPersistentModelIndex | None = None) -> int:
        if parent is not None and parent.isValid():
            return 0
        return len(self._documents)

    @override
    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        documents = self._documents
        if not index.isValid() or index.row() >= len(documents):
            return None

        rejected = documents[index.row()]

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


def _reason_text(reason: DocumentRejection) -> str:
    match reason:
        case DocumentVersionUnsupported():
            #: Shown beneath a rejected document declaring a format version this mpvQC release does not know
            return QCoreApplication.translate("ImportWizardDialog", "Unsupported document format version")
        case DocumentMalformed():
            #: Shown beneath a rejected document that does not parse as any known QC document format
            return QCoreApplication.translate("ImportWizardDialog", "Not a valid QC document")
        case DocumentUnreadable(error=PermissionError()):
            #: Shown beneath a rejected document mpvQC is not allowed to open
            return QCoreApplication.translate("ImportWizardDialog", "Permission denied")
        case DocumentUnreadable(error=FileNotFoundError()):
            #: Shown beneath a rejected document that no longer exists, e.g. deleted after it was picked
            return QCoreApplication.translate("ImportWizardDialog", "File not found")
        case DocumentUnreadable():
            #: Shown beneath a rejected document that could not be read for any other reason, e.g. a network share went away
            return QCoreApplication.translate("ImportWizardDialog", "Could not read file")
        case _ as unreachable:
            assert_never(unreachable)
