# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging

import inject
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.importing.domain import UnfinishedPlan, compute_steps
from mpvqc.importing.services import ImporterService

from .wizard_viewmodel import MpvqcImportWizardViewModel

logger = logging.getLogger(__name__)

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcImportWizardRequestRelayViewModel(QObject):
    _importer = inject.attr(ImporterService)

    importWizardRequested = Signal(QObject)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._wizard_vm: QObject | None = None
        self._importer.unfinished_plan_ready.connect(self._request_import_wizard)

    @Slot()
    def releaseWizardViewModel(self) -> None:
        if self._wizard_vm is not None:
            self._wizard_vm.deleteLater()
            self._wizard_vm = None
            if self._importer.busy:
                self._importer.cancel_pending()

    @Slot(UnfinishedPlan)
    def _request_import_wizard(self, unfinished_plan: UnfinishedPlan) -> None:
        if not compute_steps(unfinished_plan):
            logger.error("UnfinishedPlan has no steps; unfinished_plan=%r", unfinished_plan)
            self._importer.cancel_pending()
            return

        self._wizard_vm = MpvqcImportWizardViewModel(self, unfinished_plan)
        self.importWizardRequested.emit(self._wizard_vm)
