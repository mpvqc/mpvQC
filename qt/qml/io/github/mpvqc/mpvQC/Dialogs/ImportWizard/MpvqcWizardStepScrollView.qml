// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Utility

ScrollView {
    id: root

    default property alias content: _column.data

    readonly property Flickable _viewport: root.contentItem as Flickable

    readonly property int _scrimHeight: 24

    function scrollToTop(): void {
        root._viewport.contentY = 0;
    }

    contentWidth: root.availableWidth
    contentHeight: _column.implicitHeight

    ScrollBar.vertical: ScrollBar {
        policy: ScrollBar.AlwaysOff
    }

    ColumnLayout {
        id: _column

        width: root.availableWidth
    }

    Binding {
        target: root._viewport
        property: "boundsBehavior"
        value: Flickable.StopAtBounds
    }

    // Reparenting both scrims off the flickable content is what keeps them at the edges while it scrolls
    Rectangle {
        objectName: "topScrim"

        parent: root

        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right

        height: root._scrimHeight
        opacity: Math.min(1, Math.max(0, root._viewport.contentY) / root._scrimHeight)

        gradient: Gradient {
            GradientStop {
                position: 0
                color: MpvqcAppearance.palette.dialogBackground
            }

            GradientStop {
                position: 1
                color: "transparent"
            }
        }
    }

    Rectangle {
        objectName: "bottomScrim"

        parent: root

        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right

        height: root._scrimHeight
        opacity: Math.min(1, Math.max(0, root.contentHeight - root._viewport.height - root._viewport.contentY) / root._scrimHeight)

        gradient: Gradient {
            GradientStop {
                position: 0
                color: "transparent"
            }

            GradientStop {
                position: 1
                color: MpvqcAppearance.palette.dialogBackground
            }
        }
    }
}
