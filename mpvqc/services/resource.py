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

from functools import cache

import inject

from .resource_reader import ResourceReaderService


class ResourceService:
    _resource_reader = inject.attr(ResourceReaderService)

    @property
    def input_conf_content(self) -> str:
        return self._read_from_resource(path=':/data/config/input.conf')

    @property
    def mpv_conf_content(self) -> str:
        return self._read_from_resource(path=':/data/config/mpv.conf')

    @property
    def mpvqc_export_template_content(self) -> str:
        return self._read_from_resource(path=':/data/config/mpvQC-export.template')

    @cache
    def _read_from_resource(self, path: str) -> str:
        return self._resource_reader.read_from(path)
