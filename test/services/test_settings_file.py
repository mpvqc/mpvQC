# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.services import ApplicationPathsService, SettingsFileService


@pytest.fixture
def application_paths_service_mock(tmp_path) -> MagicMock:
    mock = MagicMock(spec_set=ApplicationPathsService)
    mock.file_settings = tmp_path.resolve() / "settings.ini"
    return mock


@pytest.fixture(autouse=True)
def bindings(common_bindings_with, application_paths_service_mock):
    def custom_bindings(binder: inject.Binder):
        binder.bind(ApplicationPathsService, application_paths_service_mock)

    common_bindings_with(custom_bindings)


def test_file_defaults_to_the_application_settings_file(application_paths_service_mock):
    service = SettingsFileService()

    assert Path(service.qsettings.fileName()) == application_paths_service_mock.file_settings


def test_ini_file_overrides_the_application_settings_file(tmp_path):
    override = tmp_path.resolve() / "override.ini"

    service = SettingsFileService(ini_file=str(override))

    assert Path(service.qsettings.fileName()) == override
