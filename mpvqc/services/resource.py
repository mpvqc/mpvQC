# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
from functools import cache

import inject

from .resource_reader import ResourceReaderService


@cache
def _read_from_resource(path: str) -> str:
    return inject.instance(ResourceReaderService).read_from(path)


class ResourceService:
    @property
    def input_conf_content(self) -> str:
        return _read_from_resource(path=":/data/config/input.conf")

    @property
    def mpv_conf_content(self) -> str:
        match sys.platform:
            case "win32":
                return _read_from_resource(path=":/data/config/mpv-windows.conf")
            case _:
                return _read_from_resource(path=":/data/config/mpv-linux.conf")

    @property
    def backup_template(self) -> str:
        return _read_from_resource(path=":/data/config/backup-template.jinja")

    @property
    def default_export_template(self) -> str:
        return _read_from_resource(path=":/data/config/export-template.jinja")
