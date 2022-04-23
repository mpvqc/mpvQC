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
from typing import TypeVar

import inject

from mpvqc.impl import FileReader, FileWriter
from mpvqc.impl.settings.defaults import Default

Type = TypeVar('Type')


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
