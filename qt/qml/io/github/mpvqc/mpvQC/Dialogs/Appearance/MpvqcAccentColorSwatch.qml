// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

Item {
    id: root
    objectName: `accentColorSwatch_${root.index}`

    required property int index
    required property string accentColor
    required property color previewColor
    required property bool selected

    readonly property int frameSize: 52
    readonly property int circleSize: 40
    readonly property int selectedRadius: 15

    signal picked(accentColor: string)

    implicitWidth: root.frameSize
    implicitHeight: root.frameSize
    scale: _tap.pressed ? 1.1 : 1.0

    Rectangle {
        objectName: "swatch"

        anchors.centerIn: parent
        width: root.selected ? root.frameSize : root.circleSize
        height: width
        // the selected swatch grows and morphs toward a rounded square
        radius: root.selected ? root.selectedRadius : width / 2
        color: root.previewColor

        Behavior on width {
            NumberAnimation {
                duration: 150
                easing.type: Easing.OutCubic
            }
        }

        Behavior on radius {
            NumberAnimation {
                duration: 250
                easing.type: Easing.OutCubic
            }
        }
    }

    TapHandler {
        id: _tap

        onTapped: root.picked(root.accentColor)
    }

    Behavior on scale {
        NumberAnimation {
            duration: 125
            easing.type: Easing.InOutQuad
        }
    }

    SequentialAnimation on opacity {
        PropertyAction {
            value: 0
        }
        PauseAnimation {
            duration: Math.max(0, root.index * 15)
        }
        NumberAnimation {
            to: 1
            duration: 180
            easing.type: Easing.OutCubic
        }
    }
}
