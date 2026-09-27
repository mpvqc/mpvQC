// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls

import io.github.mpvqc.mpvQC.Utility

ScrollBar {
    id: root

    horizontalPadding: 6
    verticalPadding: 2

    contentItem: Rectangle {
        implicitWidth: 4
        implicitHeight: 4
        radius: width / 2
        color: root.pressed ? MpvqcAppearance.palette.accent : Qt.alpha(MpvqcAppearance.palette.foreground, root.hovered ? 0.5 : 0.3)
    }

    // No track, but Material's state transitions animate the background's opacity, so it has to exist
    background: Item {}
}
