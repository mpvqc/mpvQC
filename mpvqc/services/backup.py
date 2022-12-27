#  mpvQC
#
#  Copyright (C) 2022 mpvQC developers
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime
from zipfile import ZipFile, ZIP_DEFLATED

import inject

from .application_paths import ApplicationPathsService


class BackupService:
    _paths = inject.attr(ApplicationPathsService)

    def backup(self, video_name: str, content: str):
        now = datetime.now()

        zip_name = f'{now:%Y-%m}.zip'
        zip_path = self._paths.dir_backup / zip_name
        zip_mode = 'a' if zip_path.exists() else 'w'

        file_name = f'{now:%Y-%m-%d_%H-%M-%S}_{video_name}.txt'

        # noinspection PyTypeChecker
        with ZipFile(zip_path, mode=zip_mode, compression=ZIP_DEFLATED) as file:
            file.writestr(file_name, content)
