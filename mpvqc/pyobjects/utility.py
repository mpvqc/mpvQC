# mpvQC
#
# Copyright (C) 2024 mpvQC developers
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

from os import environ

import inject
from PySide6.QtCore import Property, QObject, QPoint, QUrl, Slot
from PySide6.QtGui import QCursor
from PySide6.QtQml import QmlElement

from mpvqc.services import MimetypeProviderService, ReverseTranslatorService, TimeFormatterService, TypeMapperService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming, PyMethodMayBeStatic
@QmlElement
class MpvqcUtilityPyObject(QObject):
    _time_formatter: TimeFormatterService = inject.attr(TimeFormatterService)
    _type_mapper: TypeMapperService = inject.attr(TypeMapperService)
    _translator: ReverseTranslatorService = inject.attr(ReverseTranslatorService)
    _mimetype_provider: MimetypeProviderService = inject.attr(MimetypeProviderService)

    @Property(QPoint, final=True)
    def cursorPosition(self) -> QPoint:
        return QCursor.pos()

    @Property(str, constant=True, final=True)
    def videoFileGlobPattern(self) -> str:
        return self._mimetype_provider.video_file_glob_pattern

    @Property(str, constant=True, final=True)
    def subtitleFileGlobPattern(self) -> str:
        return self._mimetype_provider.subtitle_file_glob_pattern

    @Property(list, constant=True, final=True)
    def subtitleFileExtensions(self) -> list:
        return self._mimetype_provider.subtitle_file_extensions

    @Slot(str, result=str or None)
    def getEnvironmentVariable(self, key: str) -> str | None:
        return environ.get(key) or None

    @Slot(float, result=str)
    def formatTimeToStringLong(self, seconds: float) -> str:
        return self._time_formatter.format_time_to_string(seconds, long_format=True)

    @Slot(float, result=str)
    def formatTimeToStringShort(self, seconds: float) -> str:
        return self._time_formatter.format_time_to_string(seconds, long_format=False)

    @Slot(QUrl, result=str)
    def urlToAbsolutePath(self, url: QUrl) -> str:
        return self._type_mapper.map_url_to_path_string(url)

    @Slot(str, result=str)
    def reverseLookupCommentType(self, non_english: str) -> str:
        return self._translator.lookup(non_english)
