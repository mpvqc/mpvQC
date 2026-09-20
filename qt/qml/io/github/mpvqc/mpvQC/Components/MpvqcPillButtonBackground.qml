// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Templates as T

import io.github.mpvqc.mpvQC.Utility

Rectangle {
    id: root

    required property T.AbstractButton control

    radius: height / 2
    color: root.control.checked ? Qt.alpha(MpvqcAppearance.palette.accent, 0.15) : "transparent"
    border.width: root.control.visualFocus ? 2 : 0
    border.color: MpvqcAppearance.palette.accent

    Rectangle {
        anchors.fill: parent
        radius: parent.radius
        color: Qt.alpha(MpvqcAppearance.palette.foreground, root.control.down ? 0.12 : root.control.hovered ? 0.07 : 0)
    }
}
