# mpvQC
#
# Copyright (C) 2022 mpvQC developers
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

from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.services import ApplicationPathsService, FileStartupService, ResourceService


@pytest.fixture()
def file_startup_service():
    return FileStartupService()


@pytest.fixture()
def application_paths_service_mock():
    return MagicMock()


@pytest.fixture(autouse=True)
def configure_inject(application_paths_service_mock):
    def config(binder: inject.Binder):
        binder.bind(ApplicationPathsService, application_paths_service_mock)
        binder.bind(ResourceService, MagicMock())

    inject.configure(config, clear=True)


@pytest.mark.parametrize(
    "mocked_dir",
    [
        "dir_config",
        "dir_backup",
        "dir_screenshots",
        "dir_export_templates",
    ],
)
def test_directories_created(
    application_paths_service_mock,
    file_startup_service,
    mocked_dir,
):
    file_startup_service.create_missing_directories()
    path_mock = getattr(application_paths_service_mock, mocked_dir)
    path_mock.mkdir.assert_called()


@pytest.mark.parametrize(
    "mocked_file",
    [
        "file_input_conf",
        "file_mpv_conf",
    ],
)
def test_files_created(
    application_paths_service_mock,
    file_startup_service,
    mocked_file,
):
    path_mock = getattr(application_paths_service_mock, mocked_file)
    path_mock.exists.return_value = False

    file_startup_service.create_missing_files()

    path_mock.exists.assert_called()
    path_mock.write_text.assert_called()
