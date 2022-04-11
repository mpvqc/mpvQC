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
from typing import TypeVar, Generic

import inject

from mpvqc.impl import FileReader, FileWriter
from mpvqc.impl.settings.converters import Converter
from mpvqc.impl.settings.defaults import Default
from mpvqc.services import SettingsInitializerService

Type = TypeVar('Type')


class MpvqcSetting(Generic[Type]):
    _settings = inject.attr(SettingsInitializerService)

    def __init__(
            self,
            key: str,
            converter: Converter[Type],
            default: Default[Type],
    ):
        self._key = key
        self._converter = converter
        self._default_value = default.get()

    def get(self) -> Type:
        """Gets a user setting"""
        if self._dont_have_key():
            return self._default_value
        value = self._retrieve()
        if value is None:
            return self._default_value
        value = self._converter.unmarshall(value)
        if value is None:
            return self._default_value
        return value

    def _dont_have_key(self) -> bool:
        return not self._have_key()

    def _have_key(self) -> bool:
        return self._settings.backing_object.contains(self._key)

    def _retrieve(self) -> Type:
        return self._settings.backing_object.value(self._key)

    def set(self, value: Type) -> None:
        """Sets a user setting"""
        value = self._converter.marshall(value)
        self._store(value)

    def _store(self, value: Type):
        self._settings.backing_object.setValue(self._key, value)

    def reset(self) -> None:
        """Resets a user setting"""
        self._store(self._default_value)


class MpvqcSettingsFile:
    _file_reader = inject.attr(FileReader)

    def __init__(self, file: Path, default: Default[str]):
        self._file = file
        self._default_value = default.get()

    def get(self) -> str:
        return self._file_reader.read(self._file)

    def set(self, value: str) -> None:
        writer = FileWriter(self._file)
        writer.write(value)

    def reset(self) -> None:
        self.set(self._default_value)
