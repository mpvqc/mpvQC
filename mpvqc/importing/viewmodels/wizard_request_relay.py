# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import inject
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.importing.domain import PendingImport
from mpvqc.importing.services import ImporterService

from .wizard import MpvqcImportWizardViewModel

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcImportWizardRequestRelayViewModel(QObject):
    _importer = inject.attr(ImporterService)

    importWizardRequested = Signal(MpvqcImportWizardViewModel)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._wizard_vm: MpvqcImportWizardViewModel | None = None
        self._importer.pending_import_ready.connect(self._request_import_wizard)

    @Slot()
    def releaseWizardViewModel(self) -> None:
        if self._wizard_vm is not None:
            # The fallback for the one close that reports no outcome: closing
            # the popup's window natively emits neither accepted nor rejected.
            self._wizard_vm.dismiss()
            self._wizard_vm.deleteLater()
            self._wizard_vm = None

    @Slot(PendingImport)
    def _request_import_wizard(self, pending: PendingImport) -> None:
        self._wizard_vm = MpvqcImportWizardViewModel(self, pending)
        self.importWizardRequested.emit(self._wizard_vm)
