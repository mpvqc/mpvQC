# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.services.application_paths import ApplicationEnvironment, ApplicationPathsService


@pytest.fixture
def make_app_env(tmp_path):
    def _make(portable: bool) -> ApplicationEnvironment:
        if portable:
            (tmp_path / "portable").touch()
        return ApplicationEnvironment(executing_directory=tmp_path)

    return _make


def test_portable(make_app_env, tmp_path):
    app_environment = make_app_env(portable=True)
    service = ApplicationPathsService(app_environment)

    assert "appdata" in f"{service.dir_config}"
    assert service.dir_backup == tmp_path / "appdata" / "backups"
    assert service.dir_config == tmp_path / "appdata"
    assert service.dir_screenshots == tmp_path / "appdata" / "screenshots"
    assert service.dir_export_templates == tmp_path / "appdata" / "export-templates"
    assert service.file_input_conf == tmp_path / "appdata" / "input.conf"
    assert service.file_mpv_conf == tmp_path / "appdata" / "mpv.conf"
    assert service.file_settings == tmp_path / "appdata" / "settings.ini"


def test_non_portable(make_app_env):
    app_environment = make_app_env(portable=False)
    service = ApplicationPathsService(app_environment)

    assert "appdata" not in f"{service.dir_config}"
    assert service.dir_backup == service.dir_config / "backups"
    assert service.dir_screenshots == service.dir_config / "screenshots"
