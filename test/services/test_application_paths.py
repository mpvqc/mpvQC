# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.services import ApplicationEnvironmentService, ApplicationPathsService

EXECUTING_DIRECTORY = Path.home()


@pytest.fixture
def application_environment_service_mock():
    return MagicMock(spec_set=ApplicationEnvironmentService)


@pytest.fixture(autouse=True)
def configure_injections(
    common_bindings_with,
    application_environment_service_mock,
):
    def custom_bindings(binder: inject.Binder):
        binder.bind(ApplicationEnvironmentService, application_environment_service_mock)

    common_bindings_with(custom_bindings)


@pytest.fixture
def configure_mocks(application_environment_service_mock):
    def _configure(portable: bool):
        application_environment_service_mock.is_portable = portable
        application_environment_service_mock.executing_directory = EXECUTING_DIRECTORY

    return _configure


def test_portable(configure_mocks):
    configure_mocks(portable=True)

    service = ApplicationPathsService()

    assert "appdata" in f"{service.dir_config}"
    assert service.dir_backup == EXECUTING_DIRECTORY / "appdata" / "backups"
    assert service.dir_config == EXECUTING_DIRECTORY / "appdata"
    assert service.dir_screenshots == EXECUTING_DIRECTORY / "appdata" / "screenshots"
    assert service.dir_export_templates == EXECUTING_DIRECTORY / "appdata" / "export-templates"
    assert service.file_input_conf == EXECUTING_DIRECTORY / "appdata" / "input.conf"
    assert service.file_mpv_conf == EXECUTING_DIRECTORY / "appdata" / "mpv.conf"
    assert service.file_settings == EXECUTING_DIRECTORY / "appdata" / "settings.ini"


def test_non_portable(configure_mocks):
    configure_mocks(portable=False)

    service = ApplicationPathsService()

    assert "appdata" not in f"{service.dir_config}"
