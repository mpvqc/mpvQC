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

from PySide6.QtCore import QByteArray


class Role:
    """
    See: https://doc.qt.io/qt-6/qstandarditem.html#ItemType-enum

    Roles above 1000 are user definable roles. We use a role per value.
    In the Qt & Python context the value or role '1020' maps to 'timeStr' in Qml
    """

    TIME = 1010
    TYPE = 1020
    COMMENT = 1030

    MAPPING = {
        TIME: QByteArray(b"time"),
        TYPE: QByteArray(b"commentType"),
        COMMENT: QByteArray(b"comment"),
    }
