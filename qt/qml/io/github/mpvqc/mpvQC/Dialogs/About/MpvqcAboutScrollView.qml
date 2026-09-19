// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls

import io.github.mpvqc.mpvQC.Utility

ScrollView {
    id: root

    readonly property bool _needsScrollBar: contentHeight > availableHeight

    leftPadding: mirrored && _needsScrollBar ? 20 : 0
    rightPadding: !mirrored && _needsScrollBar ? 20 : 0
    contentWidth: availableWidth

    ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
    ScrollBar.vertical: ScrollBar {
        id: scrollBar

        parent: root
        x: root.mirrored ? 0 : root.width - width
        y: root.topPadding
        height: root.availableHeight
        horizontalPadding: 6
        verticalPadding: 2
        policy: root._needsScrollBar ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff

        contentItem: Rectangle {
            implicitWidth: 4
            implicitHeight: 4
            radius: width / 2
            color: scrollBar.pressed ? MpvqcAppearance.palette.accent : Qt.alpha(MpvqcAppearance.palette.foreground, scrollBar.hovered ? 0.5 : 0.3)
        }

        background: null
    }
}
