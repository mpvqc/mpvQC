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
import QtQuick.Controls
import QtQuick.Layouts


RowLayout {
    id: root

    readonly property bool displayVersion: version !== ''
    readonly property var columnOneWidth: displayVersion ? (root.width / 3) : (root.width / 2)
    readonly property var columnTwoWidth: root.width / 7
    readonly property var columnThreeWidth: displayVersion ? (root.width / 3) : (root.width / 2)

    property string dependency
    property string version: ''
    property string licence: ''
    property string url: ''

    width: parent.width
    spacing: 24

    Label {
        text: `<a href='${root.url}'>${root.dependency}</a>`

        elide: LayoutMirroring.enabled ? Text.ElideRight : Text.ElideLeft
        horizontalAlignment: Text.AlignRight
        Layout.preferredWidth: root.columnOneWidth

        onLinkActivated: (link) => {
            Qt.openUrlExternally(link)
        }

        MouseArea {
            anchors.fill: parent
            acceptedButtons: Qt.NoButton
            cursorShape: parent.hoveredLink ? Qt.PointingHandCursor : Qt.ArrowCursor
            hoverEnabled: true
        }

        ToolTip {
            y: - parent.height - 15
            text: root.url
            delay: 500
            visible: parent.hoveredLink
        }
    }

    Label {
        id: _versionLabel

        text: root.version
        visible: text
        elide: LayoutMirroring.enabled ? Text.ElideLeft : Text.ElideRight
        horizontalAlignment: Text.AlignLeft
        Layout.preferredWidth: root.columnTwoWidth

        MouseArea {
            id: _mouseArea

            enabled: _versionLabel.truncated
            hoverEnabled: true
            acceptedButtons: Qt.NoButton
            anchors.fill: _versionLabel
        }

        ToolTip {
            y: - _versionLabel.height - 15
            delay: 500
            visible: _mouseArea.containsMouse
            text: root.version
        }
    }

    Label {
        text: root.licence
        elide: LayoutMirroring.enabled ? Text.ElideLeft : Text.ElideRight
        horizontalAlignment: Text.AlignLeft
        Layout.preferredWidth: root.columnThreeWidth
    }

}
