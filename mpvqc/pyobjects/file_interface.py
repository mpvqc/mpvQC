# mpvQC
#
# Copyright (C) 2022 mpvQC developers
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

from pathlib import Path

from PySide6.QtCore import Property, QObject, Signal
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcFileInterfacePyObject(QObject):
    """"""

    def __init__(self):
        super().__init__()
        self._file_path: Path or None = None
        self._file_content = ""

    #

    def get_file_path(self) -> str:
        return self._file_path

    def set_file_path(self, value: str) -> None:
        self._file_path = Path(value)
        self.filePathChanged.emit(value)
        content = self._file_path.read_text(encoding="utf-8")
        self.set_file_content(content)

    #

    filePathChanged = Signal(str)
    filePath = Property(str, get_file_path, set_file_path, notify=filePathChanged)

    def get_file_content(self) -> str:
        return self._file_content

    def set_file_content(self, value: str):
        self._file_content = value
        self.fileContentChanged.emit(value)
        self._file_path.write_text(self._file_content, encoding="utf-8", newline="\n")

    fileContentChanged = Signal(str)
    fileContent = Property(str, get_file_content, set_file_content, notify=fileContentChanged)
