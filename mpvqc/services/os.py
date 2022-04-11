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


import platform
from enum import Enum


class SupportedSystems(Enum):
    WINDOWS = 'Windows'
    LINUX = 'Linux'
    MAC = 'Darwin'


class OsService:

    def __init__(self, system=platform.system()):
        try:
            self._os: SupportedSystems = SupportedSystems(system)
        except ValueError:
            raise SystemError(f'Operating system \'{system}\' not supported')

    @property
    def is_linux(self):
        return self._os == SupportedSystems.LINUX

    @property
    def is_not_linux(self):
        return not self.is_linux

    @property
    def is_mac(self):
        return self._os == SupportedSystems.MAC

    @property
    def is_not_mac(self):
        return not self.is_mac

    @property
    def is_windows(self):
        return self._os == SupportedSystems.WINDOWS

    @property
    def is_not_windows(self):
        return not self.is_windows
