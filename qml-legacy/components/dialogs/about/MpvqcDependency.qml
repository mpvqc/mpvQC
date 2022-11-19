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
    id: row
    width: parent.width
    spacing: 24

    property string dependency
    property string version: ''
    property string licence: ''
    property string url: ''

    readonly property bool displayVersion: version !== ''
    readonly property var columnOneWidth: displayVersion ? (row.width / 3) : (row.width / 2)
    readonly property var columnTwoWidth: row.width / 7
    readonly property var columnThreeWidth: displayVersion ? (row.width / 3) : (row.width / 2)

    Label {
        property string aUrl: "<a href='" + row.url + "'>" + row.dependency + "</a>"

        text: `<html><style type='text/css'></style>${aUrl}</html>`

        onLinkActivated: Qt.openUrlExternally(row.url)

        elide: LayoutMirroring.enabled ? Text.ElideRight : Text.ElideLeft
        horizontalAlignment: Text.AlignRight
        Layout.preferredWidth: columnOneWidth

        MouseArea {
            id: mouseArea
            anchors.fill: parent
            acceptedButtons: Qt.NoButton
            cursorShape: Qt.PointingHandCursor
            hoverEnabled: true
        }

        ToolTip {
            text: row.url
            delay: 500
            visible: mouseArea.containsMouse
        }
    }

    Label {
        Layout.preferredWidth: columnTwoWidth
        text: row.version
        visible: text
        elide: LayoutMirroring.enabled ? Text.ElideLeft : Text.ElideRight
        horizontalAlignment: Text.AlignLeft
    }

    Label {
        Layout.preferredWidth: columnThreeWidth
        text: row.licence
        elide: LayoutMirroring.enabled ? Text.ElideLeft : Text.ElideRight
        horizontalAlignment: Text.AlignLeft
    }
}
