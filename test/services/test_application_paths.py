# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from mpvqc.services.application_paths import ApplicationPathsService


def test_portable(tmp_path):
    (tmp_path / "portable").touch()
    service = ApplicationPathsService(tmp_path)

    assert "appdata" in f"{service.dir_config}"
    assert service.dir_backup == tmp_path / "appdata" / "backups"
    assert service.dir_config == tmp_path / "appdata"
    assert service.dir_screenshots == tmp_path / "appdata" / "screenshots"
    assert service.dir_export_templates == tmp_path / "appdata" / "export-templates"
    assert service.file_input_conf == tmp_path / "appdata" / "input.conf"
    assert service.file_mpv_conf == tmp_path / "appdata" / "mpv.conf"
    assert service.file_settings == tmp_path / "appdata" / "settings.ini"


def test_non_portable(tmp_path):
    service = ApplicationPathsService(tmp_path)

    assert "appdata" not in f"{service.dir_config}"
    assert service.dir_backup == service.dir_config / "backups"
    assert service.dir_screenshots == service.dir_config / "screenshots"
