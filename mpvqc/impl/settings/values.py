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

from mpvqc.enums import TimeFormat, TitleFormat
from mpvqc.impl.settings.converters import BoolConverter, IntConverter, StrConverter, TimeFormatConverter, \
    TitleFormatConverter
from mpvqc.impl.settings.defaults import DefaultValue, DefaultNickname
from mpvqc.impl.settings.templates import MpvqcSetting, MpvqcSettingsFile
from mpvqc.services import FileService, ResourceService


class MpvqcBool(MpvqcSetting[bool]):

    def __init__(self, key: str, default_value: bool):
        converter = BoolConverter()
        default = DefaultValue(default_value)
        super(MpvqcBool, self).__init__(key, converter, default)


class MpvqcInt(MpvqcSetting[int]):

    def __init__(self, key: str, default_value: int):
        converter = IntConverter()
        default = DefaultValue(default_value)
        super().__init__(key, converter, default)


class MpvqcNickname(MpvqcSetting[str]):

    def __init__(self, key: str):
        converter = StrConverter()
        default = DefaultNickname()
        super().__init__(key, converter, default)


class MpvqcTimeFormat(MpvqcSetting[TimeFormat]):

    def __init__(self, key: str):
        converter = TimeFormatConverter()
        default = DefaultValue(TimeFormat.CURRENT_TOTAL_TIME)
        super().__init__(key, converter, default)


class MpvqcTitleFormat(MpvqcSetting[TitleFormat]):

    def __init__(self, key: str):
        converter = TitleFormatConverter()
        default = DefaultValue(TitleFormat.FILE_NAME)
        super().__init__(key, converter, default)


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
