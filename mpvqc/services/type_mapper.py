# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

from PySide6.QtCore import QUrl


class TypeMapperService:
    @staticmethod
    def map_urls_to_path(urls: list[QUrl]) -> list[Path]:
        return list(map(TypeMapperService.map_url_to_path, urls))

    @staticmethod
    def map_url_to_path(url: QUrl) -> Path:
        return Path(url.toLocalFile()).resolve()

    @staticmethod
    def map_path_to_url(path: Path) -> QUrl:
        return QUrl.fromLocalFile(f"{path.resolve()}")

    @staticmethod
    def map_path_to_str(path: Path) -> str:
        return f"{path.resolve()}"
