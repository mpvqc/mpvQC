// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material

Rectangle {
    width: 400
    height: 300

    color: "#121318"

    border {
        color: "#cac8d3"
        width: 1
    }

    Material.theme: Material.Dark

    Column {
        anchors.centerIn: parent
        spacing: 20

        Image {
            source: "qrc:/data/icon.svg"
            sourceSize.width: 120
            sourceSize.height: 120
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Column {
            spacing: 8
            anchors.horizontalCenter: parent.horizontalCenter

            Label {
                text: Qt.application.name
                anchors.horizontalCenter: parent.horizontalCenter
                font {
                    pointSize: 28
                    weight: Font.DemiBold
                }
            }

            Label {
                text: Qt.application.version
                anchors.horizontalCenter: parent.horizontalCenter
                font {
                    pointSize: 11
                }
            }
        }
    }
}
