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
def application_paths_service_mock():
    return MagicMock(spec_set=ApplicationPathsService)


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, application_paths_service_mock):
    def custom_bindings(binder: inject.Binder):
        binder.bind(ApplicationPathsService, application_paths_service_mock)

    common_bindings_with(custom_bindings)


@pytest.fixture
def make_model(application_paths_service_mock):
    def _make(mocked_paths: tuple[Path, ...]) -> MpvqcExportTemplateModel:
        application_paths_service_mock.files_export_templates = mocked_paths
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
