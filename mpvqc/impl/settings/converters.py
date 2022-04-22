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


from abc import abstractmethod
from typing import TypeVar, Generic

from mpvqc.enums import TimeFormat, TitleFormat

Type = TypeVar('Type')


class Converter(Generic[Type]):

    @abstractmethod
    def marshall(self, value: Type) -> str:
        pass

    @abstractmethod
    def unmarshall(self, value: str) -> Type:
        pass


class BoolConverter(Converter[bool]):

    def marshall(self, value: bool) -> str:
        return str(value)

    def unmarshall(self, value: str) -> bool:
        return value == 'True'


class IntConverter(Converter[int]):

    def marshall(self, value: int) -> str:
        return str(value)

    def unmarshall(self, value: str) -> int:
        return int(value)


class StrConverter(Converter[str]):

    def marshall(self, value: str) -> str:
        return value

    def unmarshall(self, value: str) -> str:
        return value


class ListConverter(Converter[list[Type]], Generic[Type]):

    def __init__(
            self,
            single_value_converter: Converter[Type],
            delimiter_read: str = ",",
            delimiter_write: str = ", "
    ):
        self._single_value_converter = single_value_converter
        self._delimiter_read = delimiter_read
        self._delimiter_write = delimiter_write

    def marshall(self, value: list[Type]) -> str:
        return self._delimiter_write.join([self._single_value_converter.marshall(v) for v in value])

    def unmarshall(self, value: str) -> list[Type]:
        return [self._single_value_converter.unmarshall(v.strip()) for v in value.split(self._delimiter_read)]


class TitleFormatConverter(Converter[TitleFormat]):
    """"""

    MAPPING = {
        'empty': TitleFormat.EMPTY,
        'file-name': TitleFormat.FILE_NAME,
        'file-path': TitleFormat.FILE_PATH,
    }

    MAPPING_REVERSE = {v: k for k, v in MAPPING.items()}

    def marshall(self, value: TitleFormat) -> str:
        return self.MAPPING_REVERSE.get(value)

    def unmarshall(self, value: str) -> TitleFormat:
        return self.MAPPING.get(value)


class TimeFormatConverter(Converter[TimeFormat]):
    """"""

    MAPPING = {
        'empty': TimeFormat.EMPTY,
        'current-time': TimeFormat.CURRENT_TIME,
        'remaining-time': TimeFormat.REMAINING_TIME,
        'current-total-time': TimeFormat.CURRENT_TOTAL_TIME
    }

    MAPPING_REVERSE = {v: k for k, v in MAPPING.items()}

    def marshall(self, value: TimeFormat) -> str:
        return self.MAPPING_REVERSE.get(value)

    def unmarshall(self, value: str) -> TimeFormat:
        return self.MAPPING.get(value)
