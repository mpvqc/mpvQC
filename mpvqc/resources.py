# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from functools import cache

from PySide6.QtCore import QFile, QIODevice


@cache
def read_resource(path: str) -> str:
    file = QFile(path)
    if not file.exists():
        raise FileNotFoundError(path)
    try:
        if not file.open(QIODevice.OpenModeFlag.ReadOnly):
            msg = f"Can not open file to read: {path}"
            raise ValueError(msg)
        return bytes(file.readAll().data()).decode("utf-8")
    finally:
        if file.isOpen():
            file.close()
