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


from pathlib import Path

import inject

from mpvqc.enums import TimeFormat, TitleFormat
from mpvqc.impl.settings.converters import BoolConverter, IntConverter, PathConverter, StrConverter, \
    ListConverter, TimeFormatConverter, TitleFormatConverter
from mpvqc.impl.settings.defaults import DefaultValue, DefaultLanguage, DefaultNickname
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


class MpvqcStr(MpvqcSetting[str]):

    def __init__(self, key: str, default_value: str):
        converter = StrConverter()
        default = DefaultValue(default_value)
        super().__init__(key, converter, default)


class MpvqcPath(MpvqcSetting[Path]):

    def __init__(self, key: str):
        converter = PathConverter()
        self.default = DefaultValue(value=Path.home())
        super().__init__(key, converter, self.default)

    def get(self) -> Path:
        path: Path = super(MpvqcPath, self).get()
        if not path.exists():
            path = self.default.get()
        return path.absolute()


class MpvqcStrList(MpvqcSetting[list[str]]):

    def __init__(self, key: str, default_value: list[str]):
        single = StrConverter()
        converter = ListConverter(single)
        default = DefaultValue(default_value)
        super().__init__(key, converter, default)


class MpvqcCommentTypes(MpvqcStrList):

    def __init__(self, key: str):
        default_value = ["Translation", "Spelling", "Punctuation", "Phrasing", "Timing", "Typeset", "Note"]
        super().__init__(key, default_value)

    # noinspection PyTypeChecker
    @staticmethod
    def _list_for_import_tool():
        from PySide6.QtCore import QCoreApplication
        QCoreApplication.translate("CommentTypes", "Translation")
        QCoreApplication.translate("CommentTypes", "Spelling")
        QCoreApplication.translate("CommentTypes", "Punctuation")
        QCoreApplication.translate("CommentTypes", "Phrasing")
        QCoreApplication.translate("CommentTypes", "Timing")
        QCoreApplication.translate("CommentTypes", "Typeset")
        QCoreApplication.translate("CommentTypes", "Note")


class MpvqcLanguage(MpvqcSetting[str]):

    def __init__(self, key: str):
        converter = StrConverter()
        default = DefaultLanguage()
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
