# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

from PySide6.QtCore import QObject

from mpvqc.importing.domain import DocumentRejectionReason, ErrorsAbsent, ErrorsPresent, RejectedDocument
from mpvqc.importing.viewmodels import build_errors_step

REJECTED = (
    RejectedDocument(Path("/work/broken.qc"), DocumentRejectionReason.INVALID),
    RejectedDocument(Path("/work/future.json"), DocumentRejectionReason.UNSUPPORTED_VERSION),
)


def test_build_errors_step_only_for_present_errors(qt_app):
    parent = QObject()

    assert build_errors_step(parent, ErrorsPresent(rejected_documents=REJECTED)) is not None
    assert build_errors_step(parent, ErrorsAbsent()) is None
