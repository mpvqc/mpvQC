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

from mpvqc.impl import BuildInfoExtractor
from mpvqc.services.resource import ResourceService


class BuildInfoService:
    _resources = inject.attr(ResourceService)
    _build_info = inject.attr(BuildInfoExtractor)

    def __init__(self):
        version_content = self._resources.build_info_conf_content
        self._build_info.extract_from(version_content)

    @cached_property
    def tag(self) -> str:
        return self._build_info.tag

    @cached_property
    def commit(self) -> str:
        return self._build_info.commit_id
