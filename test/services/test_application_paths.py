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

from pathlib import Path
from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.services import ApplicationEnvironmentService, ApplicationPathsService

EXECUTING_DIRECTORY = Path.home()


@pytest.fixture
def portable_service():
    _configure_injection(portable=True)
    return ApplicationPathsService()


@pytest.fixture
def non_portable_service():
    _configure_injection(portable=False)
    return ApplicationPathsService()


def _configure_injection(portable: bool):
    mock = MagicMock()
    mock.is_portable = portable
    mock.executing_directory = EXECUTING_DIRECTORY

    def config(binder: inject.Binder):
        binder.bind(ApplicationEnvironmentService, mock)

    inject.configure(config, clear=True)


def test_service(non_portable_service, portable_service):
    assert "appdata" in f"{portable_service.dir_config}"
    assert "appdata" not in f"{non_portable_service.dir_config}"

    assert portable_service.dir_backup == EXECUTING_DIRECTORY / "appdata" / "backups"
    assert portable_service.dir_config == EXECUTING_DIRECTORY / "appdata"
    assert portable_service.dir_screenshots == EXECUTING_DIRECTORY / "appdata" / "screenshots"
    assert portable_service.dir_export_templates == EXECUTING_DIRECTORY / "appdata" / "export-templates"
    assert portable_service.file_input_conf == EXECUTING_DIRECTORY / "appdata" / "input.conf"
    assert portable_service.file_mpv_conf == EXECUTING_DIRECTORY / "appdata" / "mpv.conf"
    assert portable_service.file_settings == EXECUTING_DIRECTORY / "appdata" / "settings.ini"
