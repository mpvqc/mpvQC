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

import shared


ColumnLayout {
    id: root

    required property var mpvqcApplication
    required property string fileContent

    property var openUrlExternally: Qt.openUrlExternally

    property alias textArea: _textArea

    Label {
        id: label

        property string url: 'https://mpv.io/manual/master/#list-of-input-commands'
        property string text1: qsTranslate("EditInputConf", 'Changes to the input.conf are available after a restart.')
        property string text2: qsTranslate("EditInputConf", 'Learn more')

        Layout.topMargin: 20
        Layout.fillWidth: true
        horizontalAlignment: Text.AlignLeft

        font.pointSize: 11
        font.weight: Font.DemiBold

        text: `<html> ${text1} <a href='${url}'>${text2}</a>. </html>`

        onLinkActivated: root.openUrlExternally(url)

        MouseArea {
            anchors.fill: parent
            acceptedButtons: Qt.NoButton
            cursorShape: label.hoveredLink ? Qt.PointingHandCursor : Qt.ArrowCursor
            hoverEnabled: true
        }

        ToolTip {
            y: label.height + 5
            text: label.url
            delay: 500
            visible: label.hoveredLink
        }
    }

    Rectangle {
        height: 2
        color: Material.primary
        Layout.topMargin: 20
        Layout.fillWidth: true
    }

    ScrollView {
        id: _scrollView

        Layout.fillWidth: true
        Layout.fillHeight: true

        ScrollBar.horizontal.policy: contentWidth > width ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
        ScrollBar.vertical.policy: contentHeight > height ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff

        TextArea {
            id: _textArea

            text: root.fileContent
            background: null
            leftPadding: mirrored ? 22 : 0
            font.family: 'NotoSansMono'
            font.pointSize: 11
        }
    }

    Rectangle {
        height: 2
        color: Material.primary
        Layout.fillWidth: true
    }

}
