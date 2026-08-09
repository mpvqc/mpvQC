// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Shapes

import io.github.mpvqc.mpvQC.Utility

Rectangle {
    id: root

    property bool checked: false
    property bool partial: false

    property bool _animated: false

    readonly property int _markDuration: 260

    implicitWidth: 20
    implicitHeight: 20
    radius: 6
    // No disabled look: the mark keeps its full colors while the holding control is disabled.
    color: root.checked || root.partial ? MpvqcAppearance.palette.accent : "transparent"
    border.width: root.checked || root.partial ? 0 : 2
    border.color: MpvqcAppearance.palette.hint

    onCheckedChanged: {
        if (root._animated) {
            _pop.restart();
        }
    }

    onPartialChanged: {
        if (root._animated) {
            _pop.restart();
        }
    }

    Component.onCompleted: root._animated = true

    Shape {
        objectName: "checkMark"

        anchors.centerIn: parent

        width: 16
        height: 16
        scale: root.checked ? 1 : 0
        preferredRendererType: Shape.CurveRenderer

        ShapePath {
            strokeColor: MpvqcAppearance.palette.dialogBackground
            strokeWidth: 3
            fillColor: "transparent"
            capStyle: ShapePath.RoundCap
            joinStyle: ShapePath.RoundJoin
            startX: 3.4
            startY: 7.8

            PathLine {
                x: 6.6
                y: 11
            }
            PathLine {
                x: 12.6
                y: 4.4
            }
        }

        Behavior on scale {
            enabled: root._animated

            NumberAnimation {
                duration: root._markDuration
                easing.type: Easing.OutBack
            }
        }
    }

    Rectangle {
        objectName: "partialDash"

        anchors.centerIn: parent

        width: 10
        height: 3
        radius: height / 2
        scale: !root.checked && root.partial ? 1 : 0
        color: MpvqcAppearance.palette.dialogBackground

        Behavior on scale {
            enabled: root._animated

            NumberAnimation {
                duration: root._markDuration
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

    Behavior on color {
        enabled: root._animated

        ColorAnimation {
            duration: 120
        }
    }
}
