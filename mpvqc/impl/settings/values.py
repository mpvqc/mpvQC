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


import inject

from mpvqc.impl.settings.defaults import DefaultValue
from mpvqc.impl.settings.templates import MpvqcSettingsFile
from mpvqc.services import FileService, ResourceService


class MpvqcInputConf(MpvqcSettingsFile):
    _files = inject.attr(FileService)
    _resources = inject.attr(ResourceService)

    def __init__(self):
        file = self._files.file_input_conf
        default = DefaultValue(self._resources.input_conf_content)
        super().__init__(file, default)


class MpvqcMpvConf(MpvqcSettingsFile):
    _files = inject.attr(FileService)
    _resources = inject.attr(ResourceService)

    def __init__(self):
        file = self._files.file_mpv_conf
        default = DefaultValue(self._resources.mpv_conf_content)
        super().__init__(file, default)
