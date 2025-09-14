// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

RowLayout {
    id: root

    required property string dependencyName
    property string dependencyVersion: ""
    property string dependencyLicence: ""
    property string dependencyUrl: ""

    property Item leftItem: Label {
        text: `<a href="${root.dependencyUrl}">${root.dependencyName}</a> ${root.dependencyVersion}`
        elide: LayoutMirroring.enabled ? Text.ElideRight : Text.ElideLeft
        horizontalAlignment: Text.AlignRight
        Layout.preferredWidth: root.width / 2

        onLinkActivated: link => {
            Qt.openUrlExternally(link);
        }

        MouseArea {
            anchors.fill: parent
            acceptedButtons: Qt.NoButton
            cursorShape: parent.hoveredLink ? Qt.PointingHandCursor : Qt.ArrowCursor
            hoverEnabled: true
        }

        ToolTip {
            y: -parent.height - 15
            text: root.dependencyUrl
            delay: 500
            visible: parent.hoveredLink
        }
    }

    property Item rightItem: Label {
        text: root.dependencyLicence
        font.italic: true
        horizontalAlignment: Text.AlignLeft
        Layout.preferredWidth: root.width / 2
    }

    children: [leftItem, rightItem]
    spacing: 10
}
