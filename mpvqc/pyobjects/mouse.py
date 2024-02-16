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

from PySide6.QtCore import QObject, Signal, QPoint, Property
from PySide6.QtGui import QCursor
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcMouseCursorPyObject(QObject):

    # noinspection PyMethodMayBeStatic
    def get_cursor_position(self) -> QPoint:
        return QCursor.pos()

    cursor_pos_changed = Signal(QPoint)
    cursor_pos = Property(QPoint, get_cursor_position, notify=cursor_pos_changed)
