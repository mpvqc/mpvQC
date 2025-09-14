# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

import inject

from .application_paths import ApplicationPathsService
from .resource import ResourceService


class FileStartupService:
    _paths: ApplicationPathsService = inject.attr(ApplicationPathsService)
    _resources: ResourceService = inject.attr(ResourceService)

    def create_missing_directories(self) -> None:
        self._paths.dir_config.mkdir(exist_ok=True, parents=True)
        self._paths.dir_backup.mkdir(exist_ok=True, parents=True)
        self._paths.dir_screenshots.mkdir(exist_ok=True, parents=True)
        self._paths.dir_export_templates.mkdir(exist_ok=True, parents=True)

    def create_missing_files(self) -> None:
        self._create_missing_input_conf()
        self._create_missing_mpv_conf()

    def _create_missing_input_conf(self) -> None:
        self._create_missing_file(path=self._paths.file_input_conf, content=self._resources.input_conf_content)

    def _create_missing_mpv_conf(self) -> None:
        self._create_missing_file(path=self._paths.file_mpv_conf, content=self._resources.mpv_conf_content)

    @staticmethod
    def _create_missing_file(path: Path, content: str) -> None:
        if not path.exists():
            path.write_text(content, encoding="utf-8", newline="\n")
