# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import platform
from functools import cache

import inject

from .resource_reader import ResourceReaderService


class ResourceService:
    _resource_reader = inject.attr(ResourceReaderService)

    @property
    def input_conf_content(self) -> str:
        return self._read_from_resource(path=":/data/config/input.conf")

    @property
    def mpv_conf_content(self) -> str:
        match platform.system():
            case "Windows":
                return self._read_from_resource(path=":/data/config/mpv-windows.conf")
            case _:
                return self._read_from_resource(path=":/data/config/mpv-linux.conf")

    @property
    def backup_template(self) -> str:
        return self._read_from_resource(path=":/data/config/backup-template.jinja")

    @property
    def default_export_template(self) -> str:
        return self._read_from_resource(path=":/data/config/export-template.jinja")

    @cache
    def _read_from_resource(self, path: str) -> str:
        return self._resource_reader.read_from(path)
