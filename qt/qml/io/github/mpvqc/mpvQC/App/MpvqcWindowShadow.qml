// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Effects

Item {
    id: root

    required property int margin
    required property int radius
    required property bool windowActive

    property real _focus: root.windowActive ? 1 : 0

    visible: root.margin > 0

    RectangularShadow {
        anchors.fill: parent
        radius: root.radius
        blur: 44 + 20 * root._focus
        offset: Qt.vector2d(0, 10 + 8 * root._focus)
        color: Qt.rgba(0, 0, 0, 0.22 + 0.16 * root._focus)
    }

    RectangularShadow {
        anchors.fill: parent
        radius: root.radius
        blur: 14 + 8 * root._focus
        offset: Qt.vector2d(0, 4 + 4 * root._focus)
        color: Qt.rgba(0, 0, 0, 0.28 + 0.16 * root._focus)
    }

    Behavior on _focus {
        NumberAnimation {
            duration: 180
            easing.type: Easing.OutCubic
        }
    }
}
