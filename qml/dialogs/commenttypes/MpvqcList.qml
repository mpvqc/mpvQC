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
import QtQuick.Controls.Material


ListView {
    id: root

    required property int itemHeight

    spacing: 0
    highlightMoveDuration: 0
    highlightMoveVelocity: -1
    highlightResizeDuration: 0
    highlightResizeVelocity: -1
    clip: true
    reuseItems: false
    boundsBehavior: Flickable.StopAtBounds

    delegate: Rectangle {
        id: _delegate

        required property string type
        required property int index
        readonly property bool rowSelected: root.currentIndex === index

        width: parent ? parent.width - _scrollBar.visibleWidth : 0
        height: root.itemHeight
        radius: 4

        color: {
            if (rowSelected) {
                return Material.primary
            } if (index % 2 === 1) {
                return 'transparent'
            } else if (Material.theme === Material.Dark) {
                return Qt.lighter(Material.dialogColor, 1.12)
            } else {
                return Qt.darker(Material.dialogColor, 1.04)
            }
        }

        MouseArea {
            anchors.fill: _delegate

            onClicked: {
                root.currentIndex = index
                forceActiveFocus()
            }
        }

        Label {
            width: _delegate.width
            height: _delegate.height
            leftPadding: 5
            rightPadding: 5

            text: qsTranslate('CommentTypes', _delegate.type)
            elide: LayoutMirroring.enabled ? Text.ElideLeft : Text.ElideRight

            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignVCenter
        }
    }

    ScrollBar.vertical: ScrollBar {
        id: _scrollBar

        readonly property var isShown: root.contentHeight > root.height
        readonly property var visibleWidth: isShown ? width : 0

        policy: isShown ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
    }

    onCurrentIndexChanged: {
        _scrollToItemTimer.start()
    }

    Timer {
        id: _scrollToItemTimer

        interval: 0
        repeat: false

        onTriggered: {
            positionViewAtIndex(currentIndex, ListView.Contain)
        }
    }

}
