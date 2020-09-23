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


from pathlib import Path


class Files:

    def __init__(self):
        from src import get_metadata
        md = get_metadata()

        dir_program = Path(md.dir_program)
        is_portable = (dir_program / "portable").is_file()

        if is_portable:
            self.__dir_backup = dir_program / "appdata" / "backups"
            self.__dir_config = dir_program / "appdata"
            self.__dir_screenshots = dir_program / "appdata" / "screenshots"
        else:
            from os import environ
            from PyQt5.QtCore import QStandardPaths

            app_name = md.app_name

            config = environ.get('APPDATA') or environ.get('XDG_CONFIG_HOME')
            config = Path(config) if config else Path.home() / ".config"

            documents = Path(QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation))
            pictures = Path(QStandardPaths.writableLocation(QStandardPaths.PicturesLocation))

            self.__dir_backup = documents / app_name / "backup"
            self.__dir_config = config / app_name
            self.__dir_screenshots = pictures / app_name

        self.__dir_backup.mkdir(exist_ok=True, parents=True)
        self.__dir_config.mkdir(exist_ok=True, parents=True)
        self.__dir_screenshots.mkdir(exist_ok=True, parents=True)

        self.__dir_i18n = dir_program / "i18n"

        self.__file_input_conf = self.__dir_config / "input.conf"
        self.__file_mpv_conf = self.__dir_config / "mpv.conf"
        self.__file_settings = self.__dir_config / "settings.json"

    @property
    def dir_backup(self) -> str:
        return str(self.__dir_backup)

    @property
    def dir_config(self) -> str:
        return str(self.__dir_config)

    @property
    def dir_screenshots(self) -> str:
        return str(self.__dir_screenshots)

    @property
    def dir_i18n(self) -> Path:
        return self.__dir_i18n

    @property
    def file_input_conf(self) -> str:
        return str(self.__file_input_conf)

    @property
    def file_mpv_conf(self) -> str:
        return str(self.__file_mpv_conf)

    @property
    def file_settings(self) -> str:
        return str(self.__file_settings)


class _Holder:
    md: Files


def get_files() -> Files:
    return _Holder.md


def set_files():
    _Holder.md = Files()
