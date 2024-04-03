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
        font.weight: Font.DemiBold
        anchors.horizontalCenter: parent.horizontalCenter
    }

    Label {
        readonly property url mpvqcGitHubUrl: "https://mpvqc.github.io"

        text: `<a href="${mpvqcGitHubUrl}">${mpvqcGitHubUrl}</a>`
        anchors.horizontalCenter: parent.horizontalCenter

        onLinkActivated: (link) => {
            Qt.openUrlExternally(link)
        }

        MouseArea {
            anchors.fill: parent
            acceptedButtons: Qt.NoButton
            cursorShape: parent.hoveredLink ? Qt.PointingHandCursor : Qt.ArrowCursor
        }
    }

    Label {
        text: qsTranslate("AboutDialog", "Copyright © mpvQC Developers")
        anchors.horizontalCenter: parent.horizontalCenter
    }

    Label {
        width: parent.width
        anchors.horizontalCenter: parent.horizontalCenter
        horizontalAlignment: Text.AlignHCenter
        wrapMode: Text.WordWrap

        readonly property url licenseUrl: "https://www.gnu.org/licenses/gpl-3.0.html"
        //: This text is part of the software license description. This is the name of the license being used.
        readonly property string licenseText: qsTranslate("AboutDialog", "GNU General Public License, version 3 or later")
        readonly property string anchor: `<a href="${licenseUrl}">${licenseText}</a>`

            //: This text is part of the software license description
        text: qsTranslate("AboutDialog", "This program comes with absolutely no warranty.") + "<br>"
            //: This text is part of the software license description. Argument %1 will be the link to the license
            + qsTranslate("AboutDialog", "See the %1 for details.").arg(anchor)

        onLinkActivated: (link) => {
            Qt.openUrlExternally(link)
        }

        MouseArea {
            anchors.fill: parent
            acceptedButtons: Qt.NoButton
            cursorShape: parent.hoveredLink ? Qt.PointingHandCursor : Qt.ArrowCursor
        }

        ToolTip {
            y: -parent.height + 35
            delay: 500
            visible: parent.hoveredLink
            text: parent.hoveredLink
        }
    }

}
