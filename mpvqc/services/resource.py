# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
from functools import cached_property

from PySide6.QtCore import QFile, QIODevice


class ResourceService:
    @cached_property
    def input_conf_content(self) -> str:
        return _read_resource(":/data/config/input.conf")

    @cached_property
    def mpv_conf_content(self) -> str:
        match sys.platform:
            case "win32":
                return _read_resource(":/data/config/mpv-windows.conf")
            case _:
                return _read_resource(":/data/config/mpv-linux.conf")

    @cached_property
    def themes_json(self) -> str:
        return _read_resource(":/data/themes.json")

    @cached_property
    def backup_template(self) -> str:
        return _read_resource(":/data/config/backup-template.jinja")

    @cached_property
    def default_export_template(self) -> str:
        return _read_resource(":/data/config/export-template.jinja")


def _read_resource(resource_path: str) -> str:
    file = QFile(resource_path)
    if not file.exists():
        raise FileNotFoundError(resource_path)
    try:
        if not file.open(QIODevice.OpenModeFlag.ReadOnly):
            msg = f"Can not open file to read: {resource_path}"
            raise ValueError(msg)
        return bytes(file.readAll().data()).decode("utf-8")
    finally:
        if file.isOpen():
            file.close()
