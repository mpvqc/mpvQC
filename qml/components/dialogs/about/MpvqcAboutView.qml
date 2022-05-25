/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import handlers


Column {
    id: aboutTab
    spacing: 8
    width: parent.width
    topPadding: 15

    Image {
        anchors.horizontalCenter: parent.horizontalCenter
        source: "qrc:/data/icon.svg"
        sourceSize.width: 150
        sourceSize.height: 150
        asynchronous: true
    }

    Label {
        anchors.horizontalCenter: parent.horizontalCenter
        text: Qt.application.name
        font.bold: true
        font.pixelSize: Qt.application.font.pixelSize * 1.25
    }

    Row {
        anchors.horizontalCenter: parent.horizontalCenter
        spacing: 2

        Label {
            id: version
            text: '>>>tag<<<'
            font.bold: true
        }

        Label {
            text: "-"
            font.bold: true
            visible: commitId.text !== ""
        }

        Label {
            id: commitId
            text: '>>>commit-id<<<'
            font.bold: true
        }
    }

    Label {
        anchors.horizontalCenter: parent.horizontalCenter
        property url url: "https://github.com/mpvqc/mpvQC"

        text: "<html><style type=\'text/css\'></style><a href=\'" + url + "\'>" + url + "</a></html>"
        onLinkActivated: Qt.openUrlExternally(url)

        MouseArea {
            anchors.fill: parent
            acceptedButtons: Qt.NoButton
            cursorShape: parent.hoveredLink ? Qt.PointingHandCursor : Qt.ArrowCursor
        }
    }

    Label {
        anchors.horizontalCenter: parent.horizontalCenter

        text: "Copyright © mpvQC Developers"
        font.pixelSize: Qt.application.font.pixelSize * 0.75
    }

    Label {
        width: parent.width
        anchors.horizontalCenter: parent.horizontalCenter
        horizontalAlignment: Text.AlignHCenter
        wrapMode: Text.WordWrap

        property url licenceUrl: "https://www.gnu.org/licenses/agpl-3.0.html"
        onLinkActivated: Qt.openUrlExternally(licenceUrl)

        text: "<html><style type=\'text/css\'></style>
        This program comes with absolutely no warranty.
        <br>
        See the
        <a href=\'" + licenceUrl + "\'>
            GNU Affero General Public License, version 3 or later
        </a>
        for details.
        </html>"
        font.pixelSize: Qt.application.font.pixelSize * 0.75

        MouseArea {
            anchors.fill: parent
            acceptedButtons: Qt.NoButton // we don't want to eat clicks on the Text
            cursorShape: parent.hoveredLink ? Qt.PointingHandCursor : Qt.ArrowCursor
        }
    }

    Rectangle { color: "transparent"; height: 15; width: 10 }

    RowLayout {
        width: parent.width

        Label {
            Layout.preferredWidth: parent.width / 2
            horizontalAlignment: Text.AlignRight
            text: "mpv version:"
        }

        Label {
            Layout.fillWidth: true
            text: MpvqcPlayerProperties.mpv_version
        }
    }

    RowLayout {
        width: parent.width

        Label {
            Layout.preferredWidth: parent.width / 2
            horizontalAlignment: Text.AlignRight
            text: "ffmpeg version:"
        }

        Label {
            Layout.fillWidth: true
            text: MpvqcPlayerProperties.ffmpeg_version
        }
    }

}
