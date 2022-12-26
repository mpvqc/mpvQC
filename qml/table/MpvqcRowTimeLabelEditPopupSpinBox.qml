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
import QtQuick.Controls
import QtQuick.Layouts
import shared


SpinBox {
    id: root

    required property var mpvqcApplication
    readonly property var mpvqcMpvPlayerPropertiesPyObject: mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject
    readonly property var mpvqcTimeFormatUtils: mpvqcApplication.mpvqcTimeFormatUtils
    readonly property var duration: mpvqcMpvPlayerPropertiesPyObject.duration

    from: 0
    to: duration > 0 ? duration : 24 * 60 * 60 - 1
    bottomPadding: topPadding
    textFromValue: (value) => mpvqcTimeFormatUtils.formatTimeToString(value)

    contentItem: Label {
        text: root.textFromValue(root.value, root.locale)
        horizontalAlignment: Qt.AlignHCenter
        verticalAlignment: Qt.AlignVCenter

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            acceptedButtons: Qt.NoButton
            cursorShape: Qt.IBeamCursor

            onWheel: (event) => {
                if (event.angleDelta.y > 0) {
                    root.incrementValue()
                } else {
                    root.decrementValue()
                }
            }
        }
    }

    down.indicator: ToolButton {
        readonly property url next: "qrc:/data/icons/navigate_next_black_24dp.svg"
        readonly property url before: "qrc:/data/icons/navigate_before_black_24dp.svg"

        x: root.mirrored ? root.width - width : 0
        height: root.height
        width: height
        icon.source: root.mirrored ? next : before
        icon.width: 28
        icon.height: 28

        onClicked: root.decrementValue()
    }

    up.indicator: ToolButton {
        readonly property url next: "qrc:/data/icons/navigate_next_black_24dp.svg"
        readonly property url before: "qrc:/data/icons/navigate_before_black_24dp.svg"

        x: root.mirrored ? 0 : root.width - width
        height: root.height
        width: height
        icon.source: root.mirrored ? before : next
        icon.width: 28
        icon.height: 28

        onClicked: root.incrementValue()
    }

    background: Rectangle {
        color: 'transparent'
    }

    function decrementValue(): void {
        decrease()
        valueModified()
    }

    function incrementValue(): void {
        increase()
        valueModified()
    }

}
