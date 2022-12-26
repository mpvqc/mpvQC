#  mpvQC
#
#  Copyright (C) 2022 mpvQC developers
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PySide6.QtCore import Slot, QObject
from PySide6.QtGui import QClipboard
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcClipboardPyObject(QObject):

    def __init__(self):
        super().__init__()
        self._clipboard = QClipboard()

    @Slot(str)
    def copy_to_clipboard(self, text: str) -> None:
        self._clipboard.setText(text)
