# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.services import ApplicationPathsService, FileStartupService, ResourceService


@pytest.fixture
def file_startup_service():
    return FileStartupService()


@pytest.fixture
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
    assert path_mock.mkdir.called


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

    assert path_mock.exists.called
    assert path_mock.write_text.called
