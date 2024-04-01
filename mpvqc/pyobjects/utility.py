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
from PySide6.QtCore import QObject, Slot, QUrl, Signal, QPoint, Property
from PySide6.QtGui import QClipboard, QCursor
from PySide6.QtQml import QmlElement

from mpvqc.services import TimeFormatterService, TypeMapperService, ReverseTranslatorService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming, PyMethodMayBeStatic
@QmlElement
class MpvqcUtilityPyObject(QObject):
    """A collection of mostly unrelated utility functions"""

    def get_cursor_position(self) -> QPoint:
        return QCursor.pos()

    cursorPositionChanged = Signal(QPoint)
    cursorPosition = Property(QPoint, get_cursor_position, notify=cursorPositionChanged)

    _time_formatter: TimeFormatterService = inject.attr(TimeFormatterService)
    _type_mapper: TypeMapperService = inject.attr(TypeMapperService)
    _translator: ReverseTranslatorService = inject.attr(ReverseTranslatorService)

    def __init__(self):
        super().__init__()
        self._clipboard = QClipboard()

    @Slot(str)
    def copyToClipboard(self, text: str) -> None:
        self._clipboard.setText(text)

    @Slot(str, result=str or None)
    def getEnviornmentVariable(self, key: str) -> str or None:
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
