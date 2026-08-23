// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Effects

Item {
    id: root

    required property bool drawsOwnFrame
    required property int radius
    required property bool windowActive

    property real _focus: root.windowActive ? 1 : 0

    visible: root.drawsOwnFrame

    // libadwaita's window.csd box-shadow, layer for layer; _focus interpolates
    // between its focused and backdrop states.
    RectangularShadow {
        anchors.fill: parent
        radius: root.radius
        blur: 14
        spread: 5
        color: Qt.rgba(0, 0, 0, 0.15 * root._focus)
    }

    RectangularShadow {
        anchors.fill: parent
        radius: root.radius
        blur: 10 - 5 * root._focus
        spread: 5 - 3 * root._focus
        color: Qt.rgba(0, 0, 0, 0.08 + 0.02 * root._focus)
    }

    RectangularShadow {
        anchors.fill: parent
        radius: root.radius
        blur: 0
        spread: 1
        color: Qt.rgba(0, 0, 0, 0.05)
    }

    Behavior on _focus {
        enabled: root.visible

        NumberAnimation {
            duration: 180
            easing.type: Easing.OutCubic
        }
    }
}
