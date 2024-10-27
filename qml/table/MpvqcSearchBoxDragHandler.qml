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

    readonly property var _currentYBinding: Binding
    {
        when: root.searchBox.visible
        target: root.searchBox
        property: "y"
        value: currentY
    }

    readonly property int minimalY: topBottomMargin
    readonly property int maximalY: commentTable.height - searchBox.height - topBottomMargin

    property int currentY: maximalY
    property int transistionStartedY: -1
    property bool stickToBottom: true

    function recalculateCurrentY(newPosition: int) {
        if (!root.active && stickToBottom) {
            currentY = maximalY
            return
        }

        if (newPosition >= maximalY) {
            currentY = maximalY
            stickToBottom = true
            return;
        }

        if (newPosition >= minimalY) {
            currentY = newPosition
            stickToBottom = newPosition >= maximalY - 15
            return;
        }

        currentY = topBottomMargin
        stickToBottom = false
    }

    function handleTransition(transition) {
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

    onGrabChanged: transition => root.handleTransition(transition)

    onActiveChanged: {
        transistionStartedY = active ? searchBox.y : -1
    }

    onMaximalYChanged: {
        if (maximalY <= 0) return
        root.recalculateCurrentY(root.currentY)
    }

    yAxis.onActiveValueChanged: {
        const possiblePosition = transistionStartedY + yAxis.activeValue
        root.recalculateCurrentY(possiblePosition)
    }

}
