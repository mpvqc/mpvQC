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

import pyobjects
import shared


MpvqcMpvFrameBufferObjectPyObject {
    id: root

    required property var mpvqcApplication

    property var menu: MpvqcNewCommentMenu {
        mpvqcApplication: root.mpvqcApplication
    }

    property point globalCoordinate: Qt.point(0, 0)

    onWidthChanged: {
        globalCoordinate = root.mapToItem(mpvqcApplication.contentItem, x, y)
    }

    onHeightChanged: {
        globalCoordinate = root.mapToItem(mpvqcApplication.contentItem, x, y)
    }

    MpvqcPlayerMouseArea {
        mpvqcApplication: root.mpvqcApplication
        anchors.fill: root

        onRightMouseButtonPressed: {
            root.menu.popupMenu()
        }
    }

}
