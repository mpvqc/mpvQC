// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls

import io.github.mpvqc.mpvQC.Components

ScrollView {
    id: root

    readonly property bool _needsScrollBar: contentHeight > availableHeight

    leftPadding: mirrored && _needsScrollBar ? 20 : 0
    rightPadding: !mirrored && _needsScrollBar ? 20 : 0
    contentWidth: availableWidth

    ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
    ScrollBar.vertical: MpvqcScrollBar {
        parent: root
        x: root.mirrored ? 0 : root.width - width
        y: root.topPadding
        height: root.availableHeight
        policy: root._needsScrollBar ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
    }
}
