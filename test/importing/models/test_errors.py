# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

from mpvqc.importing.models import ErrorsModel
from mpvqc.importing.services import DocumentMalformed, DocumentVersionUnsupported, RejectedDocument

REJECTED = (
    RejectedDocument(Path("/work/broken.qc"), DocumentMalformed("broken")),
    RejectedDocument(Path("/work/future.json"), DocumentVersionUnsupported(999)),
)


def test_errors_model_exposes_rejections_with_reasons(qt_app):
    model = ErrorsModel(REJECTED)

    assert model.rowCount() == 2
    assert model.data(model.index(0, 0), ErrorsModel.FilenameRole) == "broken.qc"
    assert model.data(model.index(0, 0), ErrorsModel.FullPathRole) == str(Path("/work/broken.qc"))
    assert model.data(model.index(0, 0), ErrorsModel.ReasonRole) == "Not a valid QC document"
    assert model.data(model.index(1, 0), ErrorsModel.FilenameRole) == "future.json"
    assert model.data(model.index(1, 0), ErrorsModel.ReasonRole) == "Unsupported document format version"
