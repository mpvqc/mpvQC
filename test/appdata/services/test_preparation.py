# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

import pytest

from mpvqc.appdata.services import ApplicationPathsService, prepare_app_data, read_input_conf, read_mpv_conf


@pytest.fixture
def application_paths(tmp_path: Path) -> ApplicationPathsService:
    (tmp_path / "portable").touch()
    return ApplicationPathsService(tmp_path)


def test_app_data_prepared(application_paths: ApplicationPathsService):
    prepare_app_data(application_paths)

    for directory in (
        application_paths.dir_config,
        application_paths.dir_backup,
        application_paths.dir_screenshots,
        application_paths.dir_export_templates,
    ):
        assert directory.is_dir()
    assert application_paths.file_input_conf.read_bytes() == read_input_conf().encode("utf-8")
    assert application_paths.file_mpv_conf.read_bytes() == read_mpv_conf().encode("utf-8")


def test_existing_player_config_files_preserved(application_paths: ApplicationPathsService):
    application_paths.dir_config.mkdir(parents=True)
    application_paths.file_input_conf.write_bytes(b"SPACE cycle pause\r\n")
    application_paths.file_mpv_conf.write_bytes(b"volume=42\r\n")

    prepare_app_data(application_paths)

    assert application_paths.file_input_conf.read_bytes() == b"SPACE cycle pause\r\n"
    assert application_paths.file_mpv_conf.read_bytes() == b"volume=42\r\n"
