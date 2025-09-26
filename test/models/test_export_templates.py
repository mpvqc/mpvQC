# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from unittest.mock import MagicMock

import inject

from mpvqc.models import MpvqcExportTemplateModel
from mpvqc.models.export_templates import Role
from mpvqc.services import ApplicationPathsService


def make_model(mocked_paths: tuple[Path, ...]) -> MpvqcExportTemplateModel:
    mock = MagicMock()
    mock.files_export_templates = mocked_paths

    def config(binder: inject.Binder):
        binder.bind(ApplicationPathsService, mock)

    inject.configure(config, clear=True)
    # noinspection PyCallingNonCallable
    return MpvqcExportTemplateModel()


def test_no_templates():
    model = make_model(mocked_paths=())
    assert model.rowCount() == 0


def test_templates():
    model = make_model(mocked_paths=(Path.home(), Path.cwd()))
    assert model.rowCount() == 2


def test_templates_sorted():
    model = make_model(
        mocked_paths=(
            Path("/xy"),
            Path("/z"),
            Path("/a"),
            Path("/b"),
        )
    )

    expected = ["a", "b", "xy", "z"]
    actual = [
        model.item(0, 0).data(Role.NAME),
        model.item(1, 0).data(Role.NAME),
        model.item(2, 0).data(Role.NAME),
        model.item(3, 0).data(Role.NAME),
    ]
    assert actual == expected
