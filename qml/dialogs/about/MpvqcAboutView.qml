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

import shared


Column {
    id: root

    property var openUrlExternally: Qt.openUrlExternally

    property alias gitHubLabel: _gitHubLabel
    property alias licenceLabel: _licenceLabel

    width: parent.width
    topPadding: 20
    spacing: 8

    Image {
        anchors.horizontalCenter: parent.horizontalCenter
        source: "qrc:/data/icon.svg"
        sourceSize.width: 200
        sourceSize.height: 200
        asynchronous: true
    }

    MpvqcHeader {
        text: Qt.application.name
        anchors.horizontalCenter: parent.horizontalCenter
    }

    Label {
        text: `${Qt.application.version} - >>>commit-id<<<`
        font.bold: true
        anchors.horizontalCenter: parent.horizontalCenter
    }

    Label {
        id: _gitHubLabel

        property url mpvqcGitHubUrl: "https://mpvqc.github.io"

        text: `<html><style type="text/css" title="Tooltip here"></style><a href="${mpvqcGitHubUrl}">${mpvqcGitHubUrl}</a></html>`
        anchors.horizontalCenter: parent.horizontalCenter

        onLinkActivated: {
            root.openUrlExternally(mpvqcGitHubUrl)
        }

        MouseArea {
            anchors.fill: parent
            acceptedButtons: Qt.NoButton
            cursorShape: parent.hoveredLink ? Qt.PointingHandCursor : Qt.ArrowCursor
        }
    }

    Label {
        text: "Copyright © mpvQC Developers"
        anchors.horizontalCenter: parent.horizontalCenter
    }

    Label {
        id: _licenceLabel

        property url gnuLicenceUrl: "https://www.gnu.org/licenses/agpl-3.0.html"

        width: parent.width
        anchors.horizontalCenter: parent.horizontalCenter
        horizontalAlignment: Text.AlignHCenter
        wrapMode: Text.WordWrap

        text: `
        <html>
            <style type="text/css"></style>
            This program comes with absolutely no warranty.<br>
            See the <a href="${gnuLicenceUrl}"> GNU General Public License, version 3 or later</a> for details.
        </html>
        `

        onLinkActivated: {
            root.openUrlExternally(gnuLicenceUrl)
        }

        MouseArea {
            anchors.fill: parent
            acceptedButtons: Qt.NoButton
            cursorShape: _licenceLabel.hoveredLink ? Qt.PointingHandCursor : Qt.ArrowCursor
        }

        ToolTip {
            y: - _licenceLabel.height + 35
            delay: 500
            visible: _licenceLabel.hoveredLink
            text: _licenceLabel.gnuLicenceUrl
        }
    }

}
