# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging

import inject
from PySide6.QtCore import QObject, Qt, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.dialogs.import_wizard import MpvqcImportWizardViewModel, compute_steps
from mpvqc.services import ImporterService
from mpvqc.services.importer import UnfinishedPlan

logger = logging.getLogger(__name__)

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcDialogLoaderViewModel(QObject):
    _importer = inject.attr(ImporterService)

    importWizardDialogRequested = Signal(QObject)

    def __init__(self) -> None:
        super().__init__()
        self._active_dialog_vm: QObject | None = None
        self._importer.unfinished_plan_ready.connect(self._request_import_wizard, Qt.ConnectionType.QueuedConnection)

    @Slot()
    def releaseActiveDialog(self) -> None:
        if self._active_dialog_vm is not None:
            self._active_dialog_vm.deleteLater()
            self._active_dialog_vm = None
            if self._importer.busy:
                self._importer.cancel_pending()

    @Slot(UnfinishedPlan)
    def _request_import_wizard(self, unfinished_plan: UnfinishedPlan) -> None:
        if not compute_steps(unfinished_plan):
            logger.error("UnfinishedPlan has no steps; unfinished_plan=%r", unfinished_plan)
            self._importer.cancel_pending()
            return

        self._active_dialog_vm = MpvqcImportWizardViewModel(self, unfinished_plan)
        self.importWizardDialogRequested.emit(self._active_dialog_vm)
