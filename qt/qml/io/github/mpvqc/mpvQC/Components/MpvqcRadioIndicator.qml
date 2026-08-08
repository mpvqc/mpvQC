// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

import io.github.mpvqc.mpvQC.Utility

Rectangle {
    id: root

    property bool selected: false

    property bool _animated: false

    implicitWidth: 20
    implicitHeight: 20
    radius: root.width / 2
    color: root.selected ? MpvqcAppearance.palette.accent : "transparent"
    border.width: root.selected ? 0 : 2
    border.color: MpvqcAppearance.palette.hint

    Component.onCompleted: root._animated = true

    Rectangle {
        objectName: "radioDot"

        anchors.centerIn: parent

        width: root.selected ? 8 : 0
        height: width
        radius: width / 2
        color: MpvqcAppearance.palette.dialogBackground

        Behavior on width {
            enabled: root._animated

            NumberAnimation {
                duration: root.selected ? 240 : 100
                easing.type: root.selected ? Easing.OutBack : Easing.OutCubic
                easing.overshoot: 1.2
            }
        }
    }

    Behavior on color {
        enabled: root._animated

        ColorAnimation {
            duration: 120
        }
    }
}
