# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

from PySide6.QtCore import QObject

from mpvqc.datamodels import DocumentRejectionReason, RejectedDocument
from mpvqc.dialogs.import_wizard.steps.errors import MpvqcImportErrorsModel, build_errors_step
from mpvqc.services.importer import errors

REJECTED = (
    RejectedDocument(Path("/work/broken.qc"), DocumentRejectionReason.INVALID),
    RejectedDocument(Path("/work/future.json"), DocumentRejectionReason.UNSUPPORTED_VERSION),
)


def test_errors_model_exposes_rejections_with_reasons(qt_app):
    model = MpvqcImportErrorsModel(REJECTED)

    assert model.rowCount() == 2
    assert model.data(model.index(0, 0), MpvqcImportErrorsModel.FilenameRole) == "broken.qc"
    assert model.data(model.index(0, 0), MpvqcImportErrorsModel.FullPathRole) == str(Path("/work/broken.qc"))
    assert model.data(model.index(0, 0), MpvqcImportErrorsModel.ReasonRole) == "Not a valid QC document"
    assert model.data(model.index(1, 0), MpvqcImportErrorsModel.FilenameRole) == "future.json"
    assert model.data(model.index(1, 0), MpvqcImportErrorsModel.ReasonRole) == "Unsupported document format version"


def test_build_errors_step_only_for_present_concern(qt_app):
    parent = QObject()

    assert build_errors_step(parent, errors.Present(rejected_documents=REJECTED)) is not None
    assert build_errors_step(parent, errors.Absent()) is None
