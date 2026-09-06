# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from .application_paths import ApplicationPathsService
from .resource import read_input_conf, read_mpv_conf


def prepare_app_data(paths: ApplicationPathsService) -> None:
    for directory in (paths.dir_config, paths.dir_backup, paths.dir_screenshots, paths.dir_export_templates):
        directory.mkdir(exist_ok=True, parents=True)

    for path, read_default in ((paths.file_input_conf, read_input_conf), (paths.file_mpv_conf, read_mpv_conf)):
        if not path.exists():
            path.write_text(read_default(), encoding="utf-8", newline="\n")
