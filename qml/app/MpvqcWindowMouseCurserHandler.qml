/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

import QtQuick


MouseArea {
    required property int borderWidth

    property int b: borderWidth + 5

    hoverEnabled: true
    acceptedButtons: Qt.NoButton

    cursorShape: {
        const point = Qt.point(mouseX, mouseY)
        if (isTopLeft(point) || isBottomRight(point)) return Qt.SizeFDiagCursor
        if (isTopRight(point) || isBottomLeft(point)) return Qt.SizeBDiagCursor
        if (isLeftOrRight(point)) return Qt.SizeHorCursor
        if (isTopOrBottom(point)) return Qt.SizeVerCursor
    }

    function isTopLeft(p) { return p.x <= b && p.y <= b }
    function isBottomRight(p) { return p.x >= width - b && p.y >= height - b }
    function isTopRight(p) { return p.x >= width - b && p.y <= b }
    function isBottomLeft(p) { return p.x <= b && p.y >= height - b }
    function isLeftOrRight(p) { return p.x <= b || p.x >= width - b }
    function isTopOrBottom(p) { return p.y <= b || p.y >= height - b }

}
