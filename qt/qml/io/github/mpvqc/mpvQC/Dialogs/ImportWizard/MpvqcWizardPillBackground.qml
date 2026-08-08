// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

import io.github.mpvqc.mpvQC.Utility

Rectangle {
    id: root

    required property bool hovered

    readonly property int _tintDuration: 150

    radius: height / 2
    color: root.hovered ? Qt.alpha(MpvqcAppearance.palette.foreground, MpvqcAppearance.isDark ? 0.08 : 0.12) : "transparent"

    Behavior on color {
        ColorAnimation {
            duration: root._tintDuration
        }
    }
}
