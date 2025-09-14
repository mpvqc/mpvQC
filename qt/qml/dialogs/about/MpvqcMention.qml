// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

RowLayout {
    id: root

    property string leftContent
    property Item leftItem: Label {
        text: root.leftContent
        horizontalAlignment: Text.AlignRight
        Layout.preferredWidth: root.width / 2
    }

    property string rightContent
    property Item rightItem: Label {
        text: root.rightContent
        font.italic: true
        horizontalAlignment: Text.AlignLeft
        Layout.preferredWidth: root.width / 2
    }

    children: [leftItem, rightItem]

    height: Math.max(leftItem.height, rightItem.height)

    visible: leftContent
    spacing: 10
}
