# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.models import MpvqcExportTemplateModel
from mpvqc.services import ApplicationPathsService


@pytest.fixture
def make_model(ubiquitous_bindings):
    def _make(mocked_paths: tuple[Path, ...]) -> MpvqcExportTemplateModel:
        mock = MagicMock()
        mock.files_export_templates = mocked_paths

        def config(binder: inject.Binder):
            binder.install(ubiquitous_bindings)
            binder.bind(ApplicationPathsService, mock)

        inject.configure(config, bind_in_runtime=False, clear=True)
        # noinspection PyCallingNonCallable
        return MpvqcExportTemplateModel()

    return _make


def test_no_templates(make_model):
    model = make_model(mocked_paths=())
    assert model.rowCount() == 0


def test_templates(make_model):
    model = make_model(mocked_paths=(Path.home(), Path.cwd()))
    assert model.rowCount() == 2


def test_templates_sorted(make_model):
    model = make_model(
        mocked_paths=(
            Path("sub-path/xy"),
            Path("sub-path/z"),
            Path("sub-path/a"),
            Path("sub-path/b"),
        )
    )

    expected = ["a", "b", "xy", "z"]
    actual = [
        model.data(model.index(0), MpvqcExportTemplateModel.NameRole),
        model.data(model.index(1), MpvqcExportTemplateModel.NameRole),
        model.data(model.index(2), MpvqcExportTemplateModel.NameRole),
        model.data(model.index(3), MpvqcExportTemplateModel.NameRole),
    ]
    assert actual == expected
