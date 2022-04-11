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


from functools import cached_property

import inject
from PySide6.QtCore import QSettings

from mpvqc.services.file import FileService


class SettingsInitializerService:
    _files = inject.attr(FileService)

    @cached_property
    def backing_object(self) -> QSettings:
        return QSettings(str(self._files.file_settings), QSettings.IniFormat)
