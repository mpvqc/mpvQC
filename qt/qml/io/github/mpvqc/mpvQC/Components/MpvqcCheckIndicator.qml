// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

import io.github.mpvqc.mpvQC.Utility

Rectangle {
    id: root

    property bool checked: false
    property bool partial: false

    property bool _animated: false

    readonly property int _morphDuration: 260

    implicitWidth: 20
    implicitHeight: 20
    radius: root.checked ? root.width / 2 : 6
    color: root.checked || root.partial ? MpvqcAppearance.palette.accent : "transparent"
    border.width: root.checked || root.partial ? 0 : 2
    border.color: MpvqcAppearance.palette.hint

    onCheckedChanged: if (root._animated)
        _pop.restart()
    onPartialChanged: if (root._animated)
        _pop.restart()

    Component.onCompleted: root._animated = true

    MpvqcIconLabel {
        objectName: "checkMark"

        anchors.centerIn: parent

        scale: root.checked ? 1 : 0
        iconColor: MpvqcAppearance.palette.dialogBackground
        icon.source: MpvqcIcons.check
        icon.width: 14
        icon.height: 14

        Behavior on scale {
            enabled: root._animated

            NumberAnimation {
                duration: root._morphDuration
                easing.type: Easing.OutBack
            }
        }
    }

    Rectangle {
        objectName: "partialDash"

        anchors.centerIn: parent

        width: 10
        height: 2.5
        radius: height / 2
        scale: !root.checked && root.partial ? 1 : 0
        color: MpvqcAppearance.palette.dialogBackground

        Behavior on scale {
            enabled: root._animated

            NumberAnimation {
                duration: root._morphDuration
                easing.type: Easing.OutBack
            }
        }
    }

    SequentialAnimation {
        id: _pop
        objectName: "popAnimation"

        NumberAnimation {
            target: root
            property: "scale"
            to: 0.8
            duration: 70
            easing.type: Easing.InOutQuad
        }

        NumberAnimation {
            target: root
            property: "scale"
            to: 1
            duration: 240
            easing.type: Easing.OutBack
        }
    }

    Behavior on radius {
        enabled: root._animated

        NumberAnimation {
            duration: root._morphDuration
            easing.type: Easing.OutBack
        }
    }

    Behavior on color {
        enabled: root._animated

        ColorAnimation {
            duration: 150
        }
    }
}
