# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.appdata.services import ApplicationPathsService
from mpvqc.exporting.services import ExportTemplateCatalogService


@pytest.fixture
def application_paths_service_mock():
    return MagicMock(spec_set=ApplicationPathsService)


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, application_paths_service_mock):
    def custom_bindings(binder: inject.Binder):
        binder.bind(ApplicationPathsService, application_paths_service_mock)

    common_bindings_with(custom_bindings)


@pytest.fixture
def make_catalog(application_paths_service_mock):
    def _make(mocked_paths: tuple[Path, ...]) -> ExportTemplateCatalogService:
        application_paths_service_mock.files_export_templates = mocked_paths
        return ExportTemplateCatalogService()

    return _make


def test_no_templates(make_catalog):
    catalog = make_catalog(mocked_paths=())
    assert catalog.list_templates() == []


def test_templates_are_sorted_by_name(make_catalog):
    catalog = make_catalog(
        mocked_paths=(
            Path("sub-path/xy.jinja"),
            Path("sub-path/z.jinja"),
            Path("sub-path/a.jinja"),
            Path("sub-path/b.jinja"),
        )
    )

    actual = [template.name for template in catalog.list_templates()]

    assert actual == ["a", "b", "xy", "z"]


def test_template_is_named_after_its_file(make_catalog):
    path = Path("sub-path/my-template.jinja")
    catalog = make_catalog(mocked_paths=(path,))

    [template] = catalog.list_templates()

    assert (template.name, template.path) == ("my-template", path)
