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
    id: root

    required property var commentTable
    required property var searchBox
    required property int topBottomMargin

    readonly property int minimalY: topBottomMargin
    readonly property int maximalY: commentTable.height - searchBox.height - topBottomMargin

    readonly property var dragStartAnimation: NumberAnimation
    {
        target: searchBox
        property: "scale"
        from: 1
        to: 1.0375
        duration: 75
    }

    readonly property var dragEndAnimation: NumberAnimation
    {
        target: searchBox
        property: "scale"
        from: 1.0375
        to: 1
        duration: 75
    }

    property var handleTransition: transition => {
        switch (transition) {
            case PointerDevice.GrabExclusive:
                dragStartAnimation.start()
                break
            case PointerDevice.UngrabExclusive:
                dragEndAnimation.start()
                break
        }
    }

    target: null
    xAxis.enabled: false
    dragThreshold: 0

    onMaximalYChanged: {
        const tableHeight = root.commentTable.height
        if (tableHeight <= 0) return
        const maximalSearchBoxY = root.searchBox.y + root.searchBox.height + minimalY
        if (tableHeight > 0 && tableHeight < maximalSearchBoxY) {
            searchBox.y = maximalY
        }
    }
    onGrabChanged: transition => root.handleTransition(transition)

    yAxis.onActiveValueChanged: delta => {
        const newPosition = searchBox.y + delta
        if (newPosition >= minimalY && newPosition <= maximalY) {
            searchBox.y = newPosition
        }
    }

}
