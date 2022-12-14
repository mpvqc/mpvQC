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

import sys
from functools import cached_property
from pathlib import Path


class ApplicationEnvironmentService:

    @cached_property
    def executing_directory(self) -> Path:
        if self._build_by_pyinstaller:
            # noinspection PyUnresolvedReferences,PyProtectedMember
            return Path(sys._MEIPASS)
        else:
            # Return root directory of repository
            return Path(__file__).parent.parent.parent

    @cached_property
    def is_portable(self) -> bool:
        return (self.executing_directory / 'portable').is_file()

    @property
    def _build_by_pyinstaller(self) -> bool:
        return getattr(sys, 'frozen', False)
