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
import helpers
import models


ScrollView {

    id: creditsTab
    width: parent.width

    contentWidth: parent.width

    Column {
        width: parent.width
        topPadding: 15

        Label {
            anchors.horizontalCenter: parent.horizontalCenter
            text: qsTranslate("AboutDialog", "Development")
            font.bold: true
            font.pixelSize: MpvqcConstants.fontSizeSmall
        }

        Repeater {
            model: MpvqcDeveloperModel {}
            width: parent.width

            Label {
                anchors.horizontalCenter: parent.horizontalCenter
                text: name
            }
        }

        Rectangle { color: "transparent"; height: 15; width: 10 }

        Label {
            anchors.horizontalCenter: parent.horizontalCenter
            text: qsTranslate("AboutDialog", "Artwork")
            font.bold: true
            font.pixelSize: MpvqcConstants.fontSizeSmall
        }

        Repeater {
            model: MpvqcArtworkModel {}
            width: parent.width

            Label {
                anchors.horizontalCenter: parent.horizontalCenter
                text: name
            }
        }

        Rectangle { color: "transparent"; height: 15; width: 10 }

        Label {
            anchors.horizontalCenter: parent.horizontalCenter
            text: qsTranslate("AboutDialog", "Translation")
            font.bold: true
            font.pixelSize: MpvqcConstants.fontSizeSmall
        }

        Repeater {
            model: MpvqcLanguageModel {}
            width: parent.width

            Label {
                visible: translator
                anchors.horizontalCenter: parent.horizontalCenter
                text: translator + " (" + qsTranslate("Languages", language) + ")"
            }
        }

        Rectangle { color: "transparent"; height: 15; width: 10 }

        Label {
            anchors.horizontalCenter: parent.horizontalCenter
            text: qsTranslate("AboutDialog", "Dependencies")
            font.bold: true
            font.pixelSize: MpvqcConstants.fontSizeSmall
        }

        Repeater {
            model: MpvqcDependencyModel {}
            width: parent.width

            Label {
                anchors.horizontalCenter: parent.horizontalCenter

                text: "<html><style type=\'text/css\'></style>
                <a href=\'" + url + "\'>"
                 + name + " (" + licence + ")
                </a></html>"
                onLinkActivated: Qt.openUrlExternally(url)

                MouseArea {
                    id: mouseArea
                    anchors.fill: parent
                    acceptedButtons: Qt.NoButton
                    cursorShape: Qt.PointingHandCursor
                    hoverEnabled: true
                }

                ToolTip {
                    text: url
                    delay: 500
                    visible: mouseArea.containsMouse
                }
            }
        }
    }

}
