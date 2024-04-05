# mpvQC
#
# Copyright (C) 2024 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pathlib import Path

from PySide6.QtCore import QUrl


class TypeMapperService:
    """"""

    @staticmethod
    def map_urls_to_path(urls: list[QUrl]) -> list[Path]:
        return list(map(TypeMapperService.map_url_to_path, urls))

    @staticmethod
    def map_url_to_path(url: QUrl) -> Path:
        return Path(url.toLocalFile()).resolve()

    @staticmethod
    def map_urls_to_path_strings(urls: list[QUrl]) -> list[str]:
        return list(map(TypeMapperService.map_url_to_path_string, urls))

    @staticmethod
    def map_url_to_path_string(url: QUrl) -> str:
        return f"{Path(url.toLocalFile()).resolve()}"

    @staticmethod
    def map_path_to_url(path: Path) -> QUrl:
        return QUrl.fromLocalFile(f"{path.resolve()}")

    @staticmethod
    def map_path_to_str(path: Path) -> str:
        return f"{path.resolve()}"

    @staticmethod
    def normalize_path_str(path: str) -> str:
        return f"{Path(path).resolve()}"
