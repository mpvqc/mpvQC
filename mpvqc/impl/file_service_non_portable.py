#  mpvQC
#
#  Copyright (C) 2022 mpvQC developers
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


from os import environ
from pathlib import Path

from PySide6.QtCore import QStandardPaths


class NonPortableFileServiceImpl:
    app_name = 'mpvQC'

    def dir_backup(self) -> Path:
        return Path(QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)) / self.app_name / "backups"

    def dir_config(self) -> Path:
        config = environ.get('APPDATA') or environ.get('XDG_CONFIG_HOME')
        config = Path(config) if config else Path.home() / ".config"
        return config / self.app_name

    def dir_screenshots(self) -> Path:
        return Path(QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)) / self.app_name
