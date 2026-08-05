# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from PySide6.QtCore import Property, QAbstractItemModel, QObject
from PySide6.QtQml import QmlElement, QmlUncreatable

from mpvqc.importing.domain import errors
from mpvqc.importing.models import MpvqcImportErrorsModel

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


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
