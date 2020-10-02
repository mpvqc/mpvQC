# mpvQC
#
# Copyright (C) 2020 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from typing import Optional, Dict

from PyQt5.QtCore import QFile, QIODevice


class Resources:

    def __init__(self):
        self.__file_contents: Dict[str, Optional[str]] = {}

    def __get_file_content(self, file_path):
        content = self.__file_contents.get(file_path, None)
        if content is None:
            f = QFile(file_path)
            # noinspection PyBroadException
            try:
                f.open(QIODevice.ReadOnly)
                content = f.readAll().data().decode("utf-8")
            except Exception:
                print("Error reading resource file for path '{}'".format(file_path))
                # todo logger
                content = ""
            finally:
                f.close()
            self.__file_contents[file_path] = content
        return content

    @staticmethod
    def get_path_app_icon():
        return ":/data/icon.ico"

    @staticmethod
    def get_path_translation(language: str) -> str:
        return ":/i18n/{}.qm".format(language)

    def get_content_config_file(self, file_name: str):
        return self.__get_file_content(":/data/config/" + file_name)

    def get_content_html_file(self, file_name):
        return self.__get_file_content(":/data/html/" + file_name)

    def get_license(self):
        return self.__get_file_content(":/LICENSE")


class _Holder:
    R = None


def get_resources() -> Resources:
    return _Holder.R


def set_resources() -> None:
    _Holder.R = Resources()
