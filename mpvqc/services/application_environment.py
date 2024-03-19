# mpvQC
#
# Copyright (C) 2022 mpvQC developers
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

import os
import sys
from functools import cached_property
from pathlib import Path


class ApplicationEnvironmentService:

    @property
    def built_by_nuitka(self) -> bool:
        return "__compiled__" in globals()

    @property
    def runs_as_flatpak(self) -> bool:
        return os.getenv("FLATPAK_ID", None) is not None

    @cached_property
    def executing_directory(self) -> Path:
        if self.built_by_nuitka:
            return self._directory_of_mpvqc_exe
        else:
            return self._root_of_repository

    @property
    def _directory_of_mpvqc_exe(self) -> Path:
        return Path(sys.argv[0]).parent

    @property
    def _root_of_repository(self) -> Path:
        return Path(__file__).parent.parent.parent
