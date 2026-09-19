// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material as M

MenuItem {
    id: root

    required property string literalText

    // AbstractButton derives keyboard mnemonics from text even with a custom content item.
    text: literalText.replace(/&/g, "&&")

    contentItem: Label {
        readonly property real indicatorPadding: root.checkable && root.indicator ? root.indicator.width + root.spacing : 0

        text: root.literalText
        textFormat: Text.PlainText
        font: root.font
        color: root.enabled ? root.M.Material.foreground : root.M.Material.hintTextColor
        leftPadding: root.mirrored ? 0 : indicatorPadding
        rightPadding: root.mirrored ? indicatorPadding : 0
        horizontalAlignment: Text.AlignLeft
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }
}
