# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from PySide6.QtCore import QFile, QIODevice


class ResourceReaderService:
    def read_from(self, file_path: str) -> str:
        resource_path = self._make_resource_path_from(file_path)
        return self._read_from(resource_path)

    @staticmethod
    def _make_resource_path_from(file_path: str) -> str:
        if file_path.startswith(":/"):
            return file_path
        if file_path.startswith("/"):
            return ":" + file_path
        return ":/" + file_path

    @staticmethod
    def _read_from(resource_path: str) -> str:
        file = QFile(resource_path)
        if not file.exists():
            raise FileNotFoundError(resource_path)
        try:
            if not file.open(QIODevice.OpenModeFlag.ReadOnly):
                msg = f"Can not open file to read: {resource_path}"
                raise ValueError(msg)
            return file.readAll().data().decode("utf-8")
        finally:
            if file.isOpen():
                file.close()
