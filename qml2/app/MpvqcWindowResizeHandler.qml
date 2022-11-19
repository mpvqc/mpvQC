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


DragHandler {
    required property var mpvqcApplication
    required property int borderWidth

    property int b: borderWidth + 10

    target: null
    grabPermissions: TapHandler.TakeOverForbidden

    onActiveChanged: {
        if (active) {
            const p = centroid.position
            let edges = 0
            if (p.x <= b)
                edges |= Qt.LeftEdge
            if (p.x >= width - b)
                edges |= Qt.RightEdge
            if (p.y <= b)
                edges |= Qt.TopEdge
            if (p.y >= height - b)
                edges |= Qt.BottomEdge
            mpvqcApplication.startSystemResize(edges)
        }
    }

}
