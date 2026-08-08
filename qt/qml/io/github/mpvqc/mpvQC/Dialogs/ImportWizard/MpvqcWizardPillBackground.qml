// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

import io.github.mpvqc.mpvQC.Utility

Rectangle {
    id: root

    required property bool hovered

    property bool _animated: false

    // Capped at the shared row height, so a wrapping row keeps its neighbours' corner
    radius: Math.min(height, MpvqcConstants.listRowHeight) / 2
    color: root.hovered ? Qt.alpha(MpvqcAppearance.palette.foreground, MpvqcAppearance.isDark ? 0.08 : 0.12) : "transparent"

    Component.onCompleted: root._animated = true

    Behavior on color {
        enabled: root._animated

        ColorAnimation {
            duration: 120
        }
    }
}
