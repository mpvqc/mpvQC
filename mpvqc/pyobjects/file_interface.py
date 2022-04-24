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
from PySide6.QtCore import QObject, Signal, Property
from PySide6.QtQml import QmlElement

from mpvqc.impl import FileReader, FileWriter

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcFileInterfacePyObject(QObject):
    _file_reader = inject.attr(FileReader)

    def __init__(self):
        super().__init__()
        self._file_path: Path or None = None
        self._file_content = ""

        self.file_path_changed.connect(self._read)
        self.file_content_changed.connect(self._write)

    def get_file_path(self) -> str:
        return self._file_path

    def set_file_path(self, value: str) -> None:
        self._file_path = Path(value)
        self.file_path_changed.emit(value)

    def _read(self):
        content = self._file_reader.read(self._file_path)
        self.set_file_content(content)

    file_path_changed = Signal(str)
    file_path = Property(str, get_file_path, set_file_path, notify=file_path_changed)

    def get_file_content(self) -> str:
        return self._file_content

    def set_file_content(self, value: str):
        self._file_content = value
        self.file_content_changed.emit(value)

    def _write(self):
        writer = FileWriter(self._file_path)
        writer.write(self._file_content)

    file_content_changed = Signal(str)
    file_content = Property(str, get_file_content, set_file_content, notify=file_content_changed)
