# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

from PySide6.QtCore import QObject

from mpvqc.dialogs.import_wizard.steps.errors import build_errors_step
from mpvqc.importing.domain import DocumentRejectionReason, RejectedDocument, errors

REJECTED = (
    RejectedDocument(Path("/work/broken.qc"), DocumentRejectionReason.INVALID),
    RejectedDocument(Path("/work/future.json"), DocumentRejectionReason.UNSUPPORTED_VERSION),
)


def test_build_errors_step_only_for_present_concern(qt_app):
    parent = QObject()

    assert build_errors_step(parent, errors.Present(rejected_documents=REJECTED)) is not None
    assert build_errors_step(parent, errors.Absent()) is None
