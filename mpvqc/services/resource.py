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


from functools import cache

import inject

from mpvqc.impl import ResourceFileReader


class ResourceService:
    """Access point for all resources in the '/data' directory"""

    _resource_reader = inject.attr(ResourceFileReader)

    @property
    def window_icon_path(self) -> str:
        return ':/data/icon.svg'

    @property
    def build_info_conf_content(self) -> str:
        return self._read_from_resource(path=':/data/build-info.conf')

    @property
    def input_conf_content(self) -> str:
        return self._read_from_resource(path=':/data/config/input.conf')

    @property
    def mpv_conf_content(self) -> str:
        return self._read_from_resource(path=':/data/config/mpv.conf')

    @cache
    def _read_from_resource(self, path: str) -> str:
        return self._resource_reader.read_from(path)
