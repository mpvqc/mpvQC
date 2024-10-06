# mpvQC
#
# Copyright (C) 2024 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pathlib import Path
from unittest.mock import MagicMock

import inject

from mpvqc.pyobjects.export_template_model import MpvqcExportTemplateModelPyObject, Role
from mpvqc.services import ApplicationPathsService


def make_model(mocked_paths: tuple[Path, ...]) -> MpvqcExportTemplateModelPyObject:
    mock = MagicMock()
    mock.files_export_templates = mocked_paths

    def config(binder: inject.Binder):
        binder.bind(ApplicationPathsService, mock)

    inject.configure(config, clear=True)
    # noinspection PyCallingNonCallable
    return MpvqcExportTemplateModelPyObject()


def test_no_templates():
    model = make_model(mocked_paths=())
    assert 0 == model.rowCount()


def test_templates():
    model = make_model(mocked_paths=(Path.home(), Path.cwd()))
    assert 2 == model.rowCount()


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
