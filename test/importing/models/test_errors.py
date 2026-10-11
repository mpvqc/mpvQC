# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from typing import NamedTuple

import pytest

from mpvqc.importing.models import ErrorsModel
from mpvqc.importing.services import (
    DocumentMalformed,
    DocumentRejection,
    DocumentUnreadable,
    DocumentVersionUnsupported,
    RejectedDocument,
)

OS_ERROR_TEXT = "os error text in the system language"

REJECTED = (
    RejectedDocument(Path("/work/broken.qc"), DocumentMalformed("broken")),
    RejectedDocument(Path("/work/future.json"), DocumentVersionUnsupported(999)),
)


def test_errors_model_exposes_rejected_documents(qt_app):
    model = ErrorsModel(REJECTED)

    assert model.rowCount() == 2
    assert model.data(model.index(0, 0), ErrorsModel.FilenameRole) == "broken.qc"
    assert model.data(model.index(0, 0), ErrorsModel.FullPathRole) == str(Path("/work/broken.qc"))
    assert model.data(model.index(1, 0), ErrorsModel.FilenameRole) == "future.json"


class ReasonCase(NamedTuple):
    name: str
    rejection: DocumentRejection
    expected: str


REASONS = [
    ReasonCase(
        name="malformed",
        rejection=DocumentMalformed("broken"),
        expected="Not a valid QC document",
    ),
    ReasonCase(
        name="version unsupported",
        rejection=DocumentVersionUnsupported(999),
        expected="Unsupported document format version",
    ),
    ReasonCase(
        name="permission denied",
        rejection=DocumentUnreadable(PermissionError(13, OS_ERROR_TEXT)),
        expected="Permission denied",
    ),
    ReasonCase(
        name="not found",
        rejection=DocumentUnreadable(FileNotFoundError(2, OS_ERROR_TEXT)),
        expected="File not found",
    ),
    ReasonCase(
        name="is a directory",
        rejection=DocumentUnreadable(IsADirectoryError(21, OS_ERROR_TEXT)),
        expected="Could not read file",
    ),
    ReasonCase(
        name="other os error",
        rejection=DocumentUnreadable(OSError(5, OS_ERROR_TEXT)),
        expected="Could not read file",
    ),
]


@pytest.mark.parametrize("case", REASONS, ids=lambda case: case.name)
def test_errors_model_reason_names_the_rejection_cause(qt_app, case: ReasonCase):
    model = ErrorsModel((RejectedDocument(Path("/work/document.qc"), case.rejection),))

    shown = model.data(model.index(0, 0), ErrorsModel.ReasonRole)

    assert shown == case.expected
    assert OS_ERROR_TEXT not in shown
