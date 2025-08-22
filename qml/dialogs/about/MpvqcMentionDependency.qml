/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

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
